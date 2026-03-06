#!/usr/bin/env python3
# =============================================================================
# Lumen Project — Wobbly effect prototype
# File: /$OS_ROOT/system/effects/wobbly/wobbly-demo.py
# Simulates jelly/wobbly window using mass-spring grid + Verlet integration
# Drag with left mouse button; wobble propagates like gelatin
# Dependencies: python3-gi gir1.2-clutter-1.0 gir1.2-cogl-1.0 gir1.2-gtk-3.0
# =============================================================================

import sys
import math
import gi
gi.require_version('Clutter', '1.0')
from gi.repository import Clutter, GLib, Gdk

# Physics constants (tweak these!)
GRID_W = 9          # horizontal points (more = smoother but slower)
GRID_H = 7          # vertical points
SPRING_K = 0.85     # spring stiffness (higher = stiffer)
FRICTION = 0.92     # velocity damping per frame (\~0.85-0.98)
DRAG_FORCE = 0.18   # how strongly mouse pulls the grabbed point
BASE_WOBBLE = 0.0008  # tiny idle jiggle

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ox = x          # original/rest position
        self.oy = y
        self.vx = 0.0
        self.vy = 0.0

class WobblyPanel:
    def __init__(self, parent, width, height):
        self.width = width
        self.height = height
        self.points = []
        self.mesh_actor = None
        self.grabbed_idx = -1
        self.mouse_x = 0
        self.mouse_y = 0
        self.dragging = False

        # Create grid of points
        for j in range(GRID_H):
            row = []
            for i in range(GRID_W):
                px = i / (GRID_W - 1) * width
                py = j / (GRID_H - 1) * height
                row.append(Point(px, py))
            self.points.append(row)

        # Canvas for drawing the deformed mesh
        self.canvas = Clutter.Canvas()
        self.canvas.connect("draw", self.on_draw)

        self.mesh_actor = Clutter.Actor()
        self.mesh_actor.set_size(width, height)
        self.mesh_actor.set_content(self.canvas)
        self.mesh_actor.set_content_gravity(Clutter.ContentGravity.CENTER)
        parent.add_child(self.mesh_actor)

        # Make draggable
        self.mesh_actor.set_reactive(True)
        self.mesh_actor.connect("button-press-event", self.on_button_press)
        self.mesh_actor.connect("button-release-event", self.on_button_release)
        self.mesh_actor.connect("motion-event", self.on_motion)

    def get_point(self, i, j):
        return self.points[j][i]

    def on_draw(self, canvas, cr, width, height):
        cr.set_source_rgba(0.12, 0.45, 0.94, 0.88)  # Lumen blue-ish jelly
        cr.set_line_width(1.5)

        # Draw horizontal lines
        for j in range(GRID_H):
            cr.move_to(self.get_point(0, j).x, self.get_point(0, j).y)
            for i in range(1, GRID_W):
                p = self.get_point(i, j)
                cr.line_to(p.x, p.y)
            cr.stroke()

        # Draw vertical lines
        for i in range(GRID_W):
            cr.move_to(self.get_point(i, 0).x, self.get_point(i, 0).y)
            for j in range(1, GRID_H):
                p = self.get_point(i, j)
                cr.line_to(p.x, p.y)
            cr.stroke()

        # Optional: draw grab point highlight
        if self.grabbed_idx >= 0:
            gx = self.grabbed_idx % GRID_W
            gy = self.grabbed_idx // GRID_W
            p = self.get_point(gx, gy)
            cr.set_source_rgba(1.0, 0.3, 0.3, 0.9)
            cr.arc(p.x, p.y, 6, 0, math.tau)
            cr.fill()

        return True

    def on_button_press(self, actor, event):
        if event.button != Clutter.BUTTON_PRIMARY:
            return False
        self.dragging = True
        self.mouse_x, self.mouse_y = event.x, event.y

        # Find closest grid point to grab
        min_dist = float('inf')
        self.grabbed_idx = -1
        for j in range(GRID_H):
            for i in range(GRID_W):
                p = self.get_point(i, j)
                dx = p.x - event.x
                dy = p.y - event.y
                dist = dx*dx + dy*dy
                if dist < min_dist:
                    min_dist = dist
                    self.grabbed_idx = j * GRID_W + i
        return True

    def on_button_release(self, actor, event):
        self.dragging = False
        self.grabbed_idx = -1
        return True

    def on_motion(self, actor, event):
        if not self.dragging:
            return False
        self.mouse_x, self.mouse_y = event.x, event.y
        return True

    def update_physics(self):
        # Pull grabbed point toward mouse if dragging
        if self.dragging and self.grabbed_idx >= 0:
            gx = self.grabbed_idx % GRID_W
            gy = self.grabbed_idx // GRID_W
            p = self.get_point(gx, gy)
            p.vx += (self.mouse_x - p.x) * DRAG_FORCE
            p.vy += (self.mouse_y - p.y) * DRAG_FORCE

        # Spring forces + damping
        for j in range(GRID_H):
            for i in range(GRID_W):
                p = self.get_point(i, j)

                # Horizontal springs
                if i > 0:
                    q = self.get_point(i-1, j)
                    dx = p.x - q.x
                    dy = p.y - q.y
                    dist = math.sqrt(dx*dx + dy*dy)
                    if dist > 0.001:
                        force = (dist - (self.width / (GRID_W-1))) * SPRING_K
                        fx = dx / dist * force
                        fy = dy / dist * force
                        p.vx -= fx
                        p.vy -= fy
                        q.vx += fx
                        q.vy += fy

                # Vertical springs
                if j > 0:
                    q = self.get_point(i, j-1)
                    dx = p.x - q.x
                    dy = p.y - q.y
                    dist = math.sqrt(dx*dx + dy*dy)
                    if dist > 0.001:
                        force = (dist - (self.height / (GRID_H-1))) * SPRING_K
                        fx = dx / dist * force
                        fy = dy / dist * force
                        p.vx -= fx
                        p.vy -= fy
                        q.vx += fx
                        q.vy += fy

                # Friction / damping
                p.vx *= FRICTION
                p.vy *= FRICTION

                # Tiny base wobble (optional, comment out if unwanted)
                p.vx += math.sin(GLib.get_monotonic_time() / 800000.0 + i*0.7 + j*1.1) * BASE_WOBBLE
                p.vy += math.cos(GLib.get_monotonic_time() / 900000.0 + i*0.9 + j*0.6) * BASE_WOBBLE

        # Verlet step: integrate velocity → position
        for j in range(GRID_H):
            for i in range(GRID_W):
                p = self.get_point(i, j)
                p.x += p.vx
                p.y += p.vy

        # Redraw
        self.canvas.invalidate()


def create_wobbly_stage():
    stage = Clutter.Stage()
    stage.set_title("Lumen Wobbly Effect Prototype")
    stage.set_size(920, 620)
    stage.set_background_color(Clutter.color_from_string("#0d1117")[1])
    stage.connect("destroy", lambda _: Clutter.main_quit())

    # Fake perspective
    perspective = Clutter.Perspective()
    perspective.fovy = 45
    perspective.aspect = 920 / 620
    perspective.z_near = 0.1
    perspective.z_far = 1000
    stage.set_perspective(perspective)

    panel = WobblyPanel(stage, 800, 480)
    panel.mesh_actor.set_position(60, 70)

    # Add fake content on top (not deformed, just for looks)
    label = Clutter.Text.new_full("Sans Bold 48", "LUMEN")
    label.set_color(Clutter.Color.get_static(Clutter.StaticColor.WHITE))
    label.set_position(280, 180)
    stage.add_child(label)

    sub = Clutter.Text.new_full("Sans 24", "Flashable Serious PC-support Distro")
    sub.set_color(Clutter.Color.get_static(Clutter.StaticColor.WHITE))
    sub.set_position(220, 280)
    stage.add_child(sub)

    # Physics + redraw loop (\~60 fps target)
    def physics_tick():
        panel.update_physics()
        return True

    GLib.timeout_add(16, physics_tick)

    # Exit on ESC
    def on_key(actor, event):
        if event.keyval == Clutter.KEY_Escape:
            Clutter.main_quit()
    stage.connect("key-press-event", on_key)

    return stage


def main():
    Clutter.init(sys.argv)
    stage = create_wobbly_stage()
    stage.show()
    Clutter.main()


if __name__ == "__main__":
    main()
