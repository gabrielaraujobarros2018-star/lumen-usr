# Installing Lumen

This guide explains how to install the latest Lumen build on your computer.

Lumen is distributed as prebuilt binary images through the official GitHub repository.

---

# 1. Download the Latest Build

1. Go to the official Lumen GitHub repository.
2. Navigate to the "Releases" section.
3. Download the latest available build image (usually provided as an `.iso` file).
4. Download the corresponding checksum file (if provided).

---

# 2. Verify the Download (Recommended)

Before flashing the image, verify its integrity.

On Linux or macOS:

```bash
sha256sum Lumen.iso
```

Compare the output with the published checksum in the release page.

If the checksums do not match, do not proceed.

---

# 3. Flash the Image to USB

You will need:

* A USB drive (8GB or larger recommended)
* A flashing tool

On Linux:

```bash
sudo dd if=Lumen.iso of=/dev/sdX bs=4M status=progress oflag=sync
```

Replace `/dev/sdX` with your USB device.

On Windows:

* Use a tool such as Rufus or Balena Etcher.
* Select the Lumen ISO.
* Select your USB device.
* Start the flashing process.

On macOS:

Use Balena Etcher or similar graphical flashing tools.

---

# 4. Boot Into the Installer

1. Insert the USB drive into the target PC.
2. Reboot the machine.
3. Enter the boot menu (usually F2, F12, ESC, or DEL depending on hardware).
4. Select the USB device.

If Secure Boot is enabled and unsupported, you may need to disable it in firmware settings.

---

# 5. Installation Process

Once booted:

* Select "Install Lumen".
* Choose language and region.
* Configure disk partitioning (automatic or manual).
* Set up user account and password.
* Confirm installation.

The installer will:

* Partition the disk (if selected)
* Install the base system
* Configure GNOME + Wayland + Phosh
* Install core packages
* Set up bootloader

After installation completes:

* Reboot the system.
* Remove the USB drive.

---

# 6. First Boot

On first boot:

* Log into your new Lumen system.
* Confirm network connectivity.
* Run initial system updates if available.

Example:

```bash
sudo lumen-pkg update
```

(Use the official package manager command provided by your build.)

---

# Minimum Requirements

Recommended minimum specifications:

* 64-bit CPU
* 4GB RAM (8GB recommended)
* 20GB free disk space
* UEFI firmware support

---

# Notes

* Installing Lumen may erase existing data depending on partitioning choices.
* Always back up important data before installation.
* Developer Preview builds are intended for testing and may not be fully stable.

---

Lumen is built for freedom, privacy, and stability.
Install intentionally.