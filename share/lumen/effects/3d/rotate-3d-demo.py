#!/usr/bin/env python3
# =============================================================================
# Lumen Project — 3D effect prototype
# File: /$OS_ROOT/system/effects/3d/rotate-3d-demo.py
# Runs a small Clutter window with fake 3D rotating panel
# Dependencies: python3-gi + gir1.2-clutter-1.0 gir1.2-cogl-1.0 gir1.2-gtk-3.0
# =============================================================================

import sys
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Clutter', '1.0')
gi.require_version('Cogl', '1.0')

from gi.repository import Gtk, Clutter, Gdk, GLib, Cogl

def on_key_press(actor, event):
    if event.keyval == Clutter.KEY_Escape:
        Clutter.main_quit()
    return False

def on_frame(clock, actor):
    # Simple Y-axis rotation + fake perspective tilt
    angle = clock.get_time() / 20.0 % 360
    actor.set_rotation_angle(Clutter.RotateAxis.Y_AXIS, angle)

    # Gentle X tilt to fake perspective
    tilt = 15 * (angle % 180 - 90) / 90
    actor.set_rotation_angle(Clutter.RotateAxis.X_AXIS, tilt)

def create_3d_panel():
    stage = Clutter.Stage()
    stage.set_title("Lumen 3D Effect Prototype")
    stage.set_size(880, 560)
    stage.set_user_resizable(True)
    stage.set_background_color(Clutter.color_from_string("#0d111780")[1])
    stage.connect("destroy", lambda _: Clutter.main_quit())
    stage.connect("key-press-event", on_key_press)

    # Fake perspective
    perspective = Clutter.Perspective()
    perspective.fovy = 45
    perspective.aspect = 880 / 560
    perspective.z_near = 0.1
    perspective.z_far = 1000
    stage.set_perspective(perspective)

    # Main rotating group
    group = Clutter.Actor()
    group.set_size(800, 480)
    group.set_position(40, 40)
    group.set_pivot_point(0.5, 0.5)
    group.set_depth(-200)           # push back a bit
    stage.add_child(group)

    # Front panel (main content)
    front = Clutter.Actor()
    front.set_size(800, 480)
    front.set_background_color(Clutter.color_from_string("#1f6feb")[1])
    front.set_opacity(220)
    front.set_pivot_point(0.5, 0.5)
    group.add_child(front)

    # Add some fake "content"
    label = Clutter.Text()
    label.set_text("Lumen — Next-gen PC support distro")
    label.set_color(Clutter.Color.get_static(Clutter.StaticColor.WHITE))
    label.set_font_name("Sans Bold 28")
    label.set_position(60, 180)
    front.add_child(label)

    sub = Clutter.Text()
    sub.set_text("Flashable • Serious • Modern • 2026 ready")
    sub.set_color(Clutter.Color.get_static(Clutter.StaticColor.WHITE))
    sub.set_font_name("Sans 18")
    sub.set_position(60, 240)
    front.add_child(sub)

    # Simple back face (different color)
    back = Clutter.Actor()
    back.set_size(800, 480)
    back.set_background_color(Clutter.color_from_string("#2ea44f")[1])
    back.set_opacity(200)
    back.set_pivot_point(0.5, 0.5)
    back.set_rotation_angle(Clutter.RotateAxis.Y_AXIS, 180)
    back.set_depth(-10)
    group.add_child(back)

    back_label = Clutter.Text()
    back_label.set_text("Juiz de Fora → Belo Horizonte → World")
    back_label.set_color(Clutter.Color.get_static(Clutter.StaticColor.WHITE))
    back_label.set_font_name("Monospace Bold 22")
    back_label.set_position(80, 220)
    back.add_child(back_label)

    # Timeline / frame hook for animation
    timeline = Clutter.Timeline.new(0)  # loop forever
    timeline.set_loop(True)
    timeline.connect("new-frame", on_frame, group)
    timeline.start()

    return stage

def main():
    Clutter.init(sys.argv)

    stage = create_3d_panel()
    stage.show()

    # Optional: embed in GTK if you want later
    # But for shell-like feel → pure Clutter is better

    Clutter.main()

if __name__ == "__main__":
    main()
