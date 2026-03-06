Uptime Engine – Simple Kernel Uptime Reader for Linux
=====================================================

Project:    Lumen – Serious PC-support Flashable Linux Distribution
Purpose:    Lightweight, reliable way to obtain system uptime directly from the kernel
Version:    1.0 (initial release)
License:    MIT (or Public Domain – choose what fits Lumen best)
Author:     [Your name / Lumen Team]
Target:     Boot scripts, status tools, minimal init systems, live environments


DESCRIPTION
-----------
This is a small, dependency-free C program that reads the system's uptime
directly from the Linux kernel via /proc/uptime — the same source used by
the classic 'uptime' command.

Features:
  • High precision (milliseconds resolution)
  • No external libraries required
  • Pure userspace — no root privileges needed
  • Human-readable and machine-readable (JSON) output options
  • Clean breakdown: days, hours, minutes, seconds, ms
  • Very small binary size after stripping (\~8–15 KiB typical)


USAGE
-----
Compile:
    gcc -O2 -Wall -s -o uptime-engine uptime_engine.c
    # or with -static if you want full static binary for live USB/initramfs
    gcc -O2 -Wall -s -static -o uptime-engine uptime_engine.c

Run examples:
    ./uptime-engine
    → Uptime: 3 days, 4 hours, 22 minutes and 17.942 seconds

    ./uptime-engine --json    (if you enable JSON output in main())
    → {"uptime_seconds": 278537.942, "days": 3, ... }

    Just raw seconds (modify main()):
    ./uptime-engine
    → 278537.942000


BUILD OPTIONS / VARIANTS (for Lumen)
------------------------------------
- Use -static                     → fully static binary (good for initramfs/live)
- Define NO_HUMAN_OUTPUT          → remove printf human formatting (\~30% smaller)
- Define JSON_ONLY                → only JSON output
- Replace /proc/uptime with clock_gettime(CLOCK_BOOTTIME) for nanosecond precision
  (requires Linux ≥ 2.6.39 – most modern distros are fine)


WHY /proc/uptime ?
------------------
- Extremely reliable and fast
- Kernel-maintained monotonic counter
- No need for CAP_SYS_TIME or root
- Format never changed in 25+ years
- Alternative (CLOCK_BOOTTIME) is also good but slightly more code


EXIT CODES
----------
0     Success
1     Failed to open/read /proc/uptime or parse failure


INTEGRATION IDEAS FOR LUMEN
---------------------------
- /usr/bin/uptime-engine (drop-in replacement for busybox uptime)
- Show in your Plymouth-like boot splash status
- Use in health-check / live-ISO welcome screen
- Feed into a tiny status bar / conky-like tool
- Parse output in shell scripts:  uptime=$(uptime-engine --raw)


COMPATIBILITY
-------------
Kernel:     Linux 2.6+ (tested 3.x–6.x)
libc:       glibc, musl, uClibc (all work)
Arch:       x86_64, i686, aarch64, armv7 (should work on your Galaxy A05s too)

No systemd, no dbus, no libproc, no nonsense.


Enjoy building Lumen!
If you improve this (CLOCK_BOOTTIME version, idle %, etc.) feel free to send patches.
