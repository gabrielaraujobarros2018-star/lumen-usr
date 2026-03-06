#!/usr/bin/env python3
# =============================================================================
# Lumen Project — Prism effect prototype
# File: /$OS_ROOT/system/effects/prism/prism-aberration-demo.py
# Simulates chromatic aberration + prism-like rainbow edges in Clutter
# Looks like light dispersion / lens imperfection — modern/cinematic feel
# Dependencies: python3-gi gir1.2-clutter-1.0 gir1.2-cogl-1.0 gir1.2-gtk-3.0
# =============================================================================

import sys
import math
import gi
gi.require_version('Clutter', '1.0')
gi.require_version('Cogl', '1.0')

from gi.repository import Clutter, GLib

def create_prism_content():
    stage = Clutter.Stage()
    stage.set_title("Lumen Prism Effect Prototype")
    stage.set_size(920, 620)
    stage.set_background_color(Clutter.color_from_string("#0a0e14")[1])  # deep dark bg
    stage.connect("destroy", lambda _: Clutter.main_quit())

    # Enable fake perspective for depth feel
    perspective = Clutter.Perspective()
    perspective.fovy = 60
    perspective.aspect = 920 / 620
    perspective.z_near = 0.1
    perspective.z_far = 2000
    stage.set_perspective(perspective)

    # Main prism group (will rotate slowly)
    prism_group = Clutter.Actor()
    prism_group.set_size(840, 540)
    prism_group.set_position(40, 40)
    prism_group.set_pivot_point(0.5, 0.5)
    prism_group.set_depth(-120)
    stage.add_child(prism_group)

    # Base panel (semi-transparent glass-like)
    base = Clutter.Actor()
    base.set_size(840, 540)
    base.set_background_color(Clutter.color_from_string("#1e2a44cc")[1])  # glassy blue-purple
    base.set_opacity(180)
    prism_group.add_child(base)

    # Add some fake "content" to aberrate
    title = Clutter.Text()
    title.set_text("LUMEN")
    title.set_color(Clutter.Color.get_static(Clutter.StaticColor.WHITE))
    title.set_font_name("Sans Bold 72")
    title.set_position(180, 140)
    prism_group.add_child(title)

    subtitle = Clutter.Text()
    subtitle.set_text("Flashable • Serious • Prism-powered")
    subtitle.set_color(Clutter.Color.get_static(Clutter.StaticColor.WHITE))
    subtitle.set_font_name("Sans 28")
    subtitle.set_position(140, 260)
    prism_group.add_child(subtitle)

    # Simulate chromatic aberration with 3 offset layers (R/G/B)
    def create_channel_layer(color_str, offset_x, offset_y, opacity):
        layer = Clutter.Actor()
        layer.set_size(840, 540)
        layer.set_position(offset_x, offset_y)
        layer.set_opacity(opacity)
        layer.set_background_color(Clutter.color_from_string(color_str)[1])
        layer.set_content_gravity(Clutter.ContentGravity.CENTER)
        # We clip to text/content shape roughly via opacity mask later if needed
        prism_group.add_child(layer)
        return layer

    r_layer = create_channel_layer("#ff4d4dcc",  -4,  -2, 140)   # red shift left-up
    g_layer = create_channel_layer("#4dff4dcc",   0,   0, 180)   # green center
    b_layer = create_channel_layer("#4d4dffcc",   4,   2, 140)   # blue shift right-down

    # Rainbow edge glow (simple outer fringe simulation)
    edge = Clutter.Actor()
    edge.set_size(860, 560)
    edge.set_position(-10, -10)
    edge.set_opacity(90)
    
    # Gradient-like rainbow via canvas (simple approximation)
    canvas = Clutter.Canvas()
    canvas.connect("draw", lambda _, cr, w, h: (
        # Radial-ish rainbow gradient
        pat := cr.create_radial_gradient(w/2, h/2, 0, w/2, h/2, max(w,h)/1.4),
        pat.add_color_stop_rgba(0.0, 1.0, 0.3, 0.3, 0.4),
        pat.add_color_stop_rgba(0.25, 1.0, 1.0, 0.3, 0.4),
        pat.add_color_stop_rgba(0.5, 0.3, 1.0, 0.3, 0.4),
        pat.add_color_stop_rgba(0.75, 0.3, 0.3, 1.0, 0.4),
        pat.add_color_stop_rgba(1.0, 0.6, 0.3, 1.0, 0.2),
        cr.set_source(pat),
        cr.rectangle(0, 0, w, h),
        cr.fill(),
        True
    ))
    edge.set_content(canvas)
    edge.set_content_repeat(Clutter.ContentRepeat.NONE)
    prism_group.add_child(edge)

    # Gentle animation: slow rotation + aberration pulse
    def on_frame(clock):
        ms = clock.get_time() / 1000.0
        angle = ms * 4.0   # \~4 deg/sec
        prism_group.set_rotation_angle(Clutter.RotateAxis.Z_AXIS, angle % 360)

        # Pulse aberration strength
        pulse = (math.sin(ms * 1.2) + 1) / 2 * 0.8 + 0.2
        r_layer.set_position(-4 * pulse, -2 * pulse)
        b_layer.set_position( 4 * pulse,  2 * pulse)
        edge.set_opacity(int(70 + 60 * pulse))

    timeline = Clutter.Timeline.new(0)
    timeline.set_loop(True)
    timeline.connect("new-frame", on_frame)
    timeline.start()

    # Exit on ESC
    def on_key(actor, event):
        if event.keyval == Clutter.KEY_Escape:
            Clutter.main_quit()
    stage.connect("key-press-event", on_key)

    return stage


def main():
    Clutter.init(sys.argv)
    stage = create_prism_content()
    stage.show()
    Clutter.main()


if __name__ == "__main__":
    main()
