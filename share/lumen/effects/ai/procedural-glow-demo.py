#!/usr/bin/env python3
# =============================================================================
# Lumen Project — AI-themed effects prototype
# File: /$OS_ROOT/system/effects/ai/procedural-glow-demo.py
# A standalone Clutter window with organic, "AI-like" pulsing glow particles
# Gives impression of intelligent / adaptive visual effect
# Dependencies: python3-gi gir1.2-clutter-1.0 gir1.2-cogl-1.0 gir1.2-gtk-3.0
# Run on your build host or proot env
# =============================================================================

import sys
import math
import random
import gi
gi.require_version('Clutter', '1.0')
gi.require_version('Cogl', '1.0')

from gi.repository import Clutter, GLib, Cogl

# Simple easing function (cubic in-out)
def ease_cubic(t):
    if t < 0.5:
        return 4 * t * t * t
    p = 2 * t - 2
    return 0.5 * p * p * p + 1

class Particle:
    def __init__(self, parent):
        self.actor = Clutter.Actor()
        size = random.uniform(8, 24)
        self.actor.set_size(size, size)
        self.actor.set_background_color(Clutter.color_from_string("#58a6ff88")[1])  # soft blue glow
        self.actor.set_opacity(0)

        # Make it circular
        self.actor.set_pivot_point(0.5, 0.5)
        self.shape = Clutter.Canvas()
        self.shape.connect("draw", self.on_draw)
        self.actor.set_content(self.shape)
        self.actor.set_content_gravity(Clutter.ContentGravity.CENTER)

        parent.add_child(self.actor)

        self.x = random.uniform(0, 880)
        self.y = random.uniform(0, 560)
        self.phase = random.uniform(0, math.tau)
        self.speed = random.uniform(0.4, 1.2)
        self.radius = random.uniform(60, 180)

        self.actor.set_position(self.x, self.y)

    def on_draw(self, canvas, cr, width, height):
        cr.set_source_rgba(0.35, 0.65, 1.0, 0.6)
        cr.arc(width/2, height/2, width/2 - 2, 0, math.tau)
        cr.fill_preserve()
        cr.set_source_rgba(0.35, 0.65, 1.0, 0.9)
        cr.set_line_width(2)
        cr.stroke()
        return True

    def update(self, ms):
        t = (ms / 1000.0 * self.speed + self.phase) % math.tau
        norm = (math.sin(t) + 1) / 2
        eased = ease_cubic(norm)

        opacity = int(40 + 215 * eased)
        scale = 0.6 + 1.4 * eased

        self.actor.set_opacity(opacity)
        self.actor.set_scale(scale, scale)

        # Gentle orbital motion
        angle = t * 0.3
        offset_x = math.cos(angle) * self.radius * 0.4
        offset_y = math.sin(angle * 1.3) * self.radius * 0.3
        self.actor.set_position(self.x + offset_x, self.y + offset_y)


def on_frame(clock, particles):
    ms = clock.get_time()
    for p in particles:
        p.update(ms)


def create_ai_glow_stage():
    stage = Clutter.Stage()
    stage.set_title("Lumen AI Visual Prototype — Procedural Glow")
    stage.set_size(880, 560)
    stage.set_background_color(Clutter.color_from_string("#0d1117")[1])
    stage.connect("destroy", lambda _: Clutter.main_quit())

    # Fake depth/perspective
    perspective = Clutter.Perspective()
    perspective.fovy = 50
    perspective.aspect = 880 / 560
    perspective.z_near = 0.1
    perspective.z_far = 1000
    stage.set_perspective(perspective)

    # Container for particles
    container = Clutter.Actor()
    container.set_size(880, 560)
    stage.add_child(container)

    particles = [Particle(container) for _ in range(40)]

    # Animation loop
    timeline = Clutter.Timeline.new(0)
    timeline.set_loop(True)
    timeline.connect("new-frame", on_frame, particles)
    timeline.start()

    # Central "core" glow
    core = Clutter.Actor()
    core.set_size(180, 180)
    core.set_position(880/2 - 90, 560/2 - 90)
    core.set_background_color(Clutter.color_from_string("#1f6feb")[1])
    core.set_opacity(140)
    core.set_pivot_point(0.5, 0.5)

    core_shape = Clutter.Canvas()
    core_shape.connect("draw", lambda c, cr, w, h: (
        cr.set_source_rgba(0.12, 0.42, 0.94, 0.7),
        cr.arc(w/2, h/2, w/2 - 10, 0, math.tau),
        cr.fill(),
        True
    ))
    core.set_content(core_shape)

    stage.add_child(core)

    # Pulse the core
    def pulse_core():
        angle = GLib.get_monotonic_time() / 1000000.0 * 1.2
        scale = 0.9 + 0.2 * (math.sin(angle) + 1)/2
        core.set_scale(scale, scale)
        return True

    GLib.timeout_add(16, pulse_core)

    return stage


def main():
    Clutter.init(sys.argv)
    stage = create_ai_glow_stage()
    stage.show()
    Clutter.main()


if __name__ == "__main__":
    main()
