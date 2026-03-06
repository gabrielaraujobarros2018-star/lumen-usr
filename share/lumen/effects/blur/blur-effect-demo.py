#!/usr/bin/env python3
# =============================================================================
# Lumen Project — Blur effect prototype
# File: /$OS_ROOT/system/effects/blur/blur-effect-demo.py
# Demonstrates native Clutter.BlurEffect (Gaussian blur) on a glass-like panel
# Shows how blur would look on semi-transparent UI elements in GNOME Shell
# Dependencies: python3-gi gir1.2-clutter-1.0 gir1.2-cogl-1.0 gir1.2-gtk-3.0
# =============================================================================

import sys
import math
import gi
gi.require_version('Clutter', '1.0')
gi.require_version('Cogl', '1.0')

from gi.repository import Clutter, GLib

def create_blur_demo_stage():
    stage = Clutter.Stage()
    stage.set_title("Lumen Blur Effect Prototype — Clutter.BlurEffect")
    stage.set_size(920, 620)
    stage.set_background_color(Clutter.color_from_string("#0d1117")[1])
    stage.connect("destroy", lambda _: Clutter.main_quit())

    # Fake background content (to see blur working)
    bg_actor = Clutter.Actor()
    bg_actor.set_size(920, 620)
    bg_actor.set_background_color(Clutter.color_from_string("#1a2338")[1])
    stage.add_child(bg_actor)

    # Some noisy/random "wallpaper-like" elements to blur meaningfully
    for i in range(80):
        dot = Clutter.Actor()
        dot.set_size(12, 12)
        dot.set_position(
            i * 11.5 % 920,
            (i * 17.3) % 620
        )
        hue = (i * 13) % 360
        col_str = f"hsl({hue}, 70%, 60%)"
        dot.set_background_color(Clutter.color_from_string(col_str)[1])
        dot.set_opacity(140 + (i % 100))
        stage.add_child(dot)

    # Text behind the blur layer
    title_bg = Clutter.Text()
    title_bg.set_text("LUMEN")
    title_bg.set_color(Clutter.Color.get_static(Clutter.StaticColor.WHITE))
    title_bg.set_font_name("Sans Bold 120")
    title_bg.set_position(140, 140)
    title_bg.set_opacity(60)
    stage.add_child(title_bg)

    # Main glass panel that will be blurred
    glass = Clutter.Actor()
    glass.set_size(820, 520)
    glass.set_position(50, 50)
    glass.set_background_color(Clutter.color_from_string("#2a3b5acc")[1])  # semi-transparent
    glass.set_opacity(220)
    glass.set_pivot_point(0.5, 0.5)
    stage.add_child(glass)

    # Apply native Clutter blur effect
    blur_effect = Clutter.BlurEffect()
    blur_effect.set_radius(0)          # we'll animate this
    glass.add_effect(blur_effect)

    # Content on the glass panel (sharp, not blurred)
    label = Clutter.Text()
    label.set_text("Blur Prototype")
    label.set_color(Clutter.Color.get_static(Clutter.StaticColor.WHITE))
    label.set_font_name("Sans Bold 48")
    label.set_position(220, 180)
    glass.add_child(label)

    sub = Clutter.Text()
    sub.set_text("Serious • Flashable • PC-support Distro\nBackground elements blurred in real-time")
    sub.set_color(Clutter.Color.get_static(Clutter.StaticColor.WHITE))
    sub.set_font_name("Sans 22")
    sub.set_position(140, 260)
    sub.set_line_alignment(Clutter.TextAlign.CENTER)
    sub.set_justify(True)
    glass.add_child(sub)

    # Animate blur radius gently (0 → 28 → 0 loop, like dynamic blur strength)
    def animate_blur():
        ms = GLib.get_monotonic_time() / 1000000.0
        strength = (math.sin(ms * 0.8) + 1) / 2          # 0..1
        radius = 4 + 24 * strength                       # 4..28
        blur_effect.set_radius(int(radius))
        return True

    GLib.timeout_add(33, animate_blur)  # \~30 fps updates

    # Gentle rotation for demo flair
    def on_frame(clock):
        angle = clock.get_time() / 30000.0 % 360
        glass.set_rotation_angle(Clutter.RotateAxis.Z_AXIS, math.sin(angle * 0.1) * 4)

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
    stage = create_blur_demo_stage()
    stage.show()
    Clutter.main()


if __name__ == "__main__":
    main()
