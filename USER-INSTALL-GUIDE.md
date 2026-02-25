# Qube TX 300 Series — User Install Guide

This guide helps you install the Qube TX tools on your computer. **No internet connection required** — everything you need is already in this folder.

There are three tools available:

| Tool | What It Does | Version |
|------|-------------|---------|
| **TR300** | Machine reporting | v3.6.0 |
| **ND300** | Network diagnostics | v2.6.0 |
| **SD300** | System diagnostics | v1.2.1 |

---

## Quick Start (if you already know your setup)

| I have a... | Grab this file |
|-------------|---------------|
| Mac (2021 or newer, Apple chip) | `*-aarch64-apple-darwin.dmg` from the `macos/` folder |
| Mac (older, Intel chip) | `*-x86_64-apple-darwin.dmg` from the `macos/` folder |
| Windows PC (any) | `*-x86_64-pc-windows-msvc.msi` from the `windows/` folder |
| Linux PC (most distros) | `*-x86_64-unknown-linux-gnu.tar.xz` from the `linux/` folder |

Not sure? Keep reading — Step 1 will walk you through it.

---

## Step 1: Figure Out What Kind of Computer You Have

You need to know two things: **your operating system** (Mac, Windows, or Linux) and **what type of processor** (the chip inside your computer that runs programs). Different processors need different versions of the same tool — kind of like how a car manual is different for automatic vs. manual transmission, even though it's the same car model.

Here's how to check what you have:

### Mac

1. Click the **Apple menu** () in the top-left corner of your screen.
2. Click **"About This Mac"**.
3. Look for one of the following:
   - **"Chip: Apple M1"** (or M2, M3, M4) — this means you have an **Apple Silicon** Mac. These are Apple's own processors, used in Macs from late 2020 onward (MacBook Air, MacBook Pro, iMac, Mac Mini, Mac Studio, Mac Pro).
   - **"Processor: Intel"** — this means you have an **Intel** Mac. These are older Macs (generally 2020 and earlier) that use Intel's processors.

> **Shortcut:** If you bought your Mac in **2021 or later**, you almost certainly have Apple Silicon. If you bought it **2019 or earlier**, it's Intel. 2020 models could be either — check "About This Mac" to be sure.

### Windows

1. Open **Settings** (press the Windows key, then type "Settings").
2. Go to **System** → **About**.
3. Look at **"System type"**:
   - **"64-bit operating system, x64-based processor"** — this is by far the most common type. It means you have a standard Intel or AMD processor (the kind in most desktops and laptops). Use the standard Windows files below.
   - **"64-bit operating system, ARM-based processor"** — this is a newer ARM-based laptop (like the Surface Pro X or laptops with Qualcomm Snapdragon chips). Don't worry — the standard Windows files still work fine on these. Windows automatically translates the program to run on your ARM chip.

> **Shortcut:** Unless you specifically bought a Surface Pro X or a Snapdragon-powered laptop, you're almost certainly `x64`. Either way, the same Windows file works for both.

### Linux

1. Open a **Terminal**.
2. Type `uname -m` and press Enter.
3. You'll see one of:
   - **`x86_64`** — this means you have a standard Intel or AMD processor. This is what most desktops, laptops, and cloud servers use.
   - **`aarch64`** — this means you have an ARM processor. Common on Raspberry Pi boards, AWS Graviton cloud servers, and Oracle Ampere instances.

> **Shortcut:** If you're on a regular desktop or laptop, it's `x86_64`. If you're on a Raspberry Pi or you specifically set up an ARM cloud server, it's `aarch64`.

---

## Step 2: Pick the Right File

Find your tool in the tables below, then match your computer type to the correct file.

**A note about the file types you'll see:**
- **`.dmg`** (Mac) — a "disk image" file. Double-click it and it opens like a virtual USB drive. This is the standard way to distribute Mac apps.
- **`.msi`** (Windows) — a standard Windows installer. Double-click it and follow the prompts, just like installing any other program.
- **`.zip`** (Windows) — a compressed folder. Right-click and "Extract All" to unpack it. No installation needed — just run the program inside.
- **`.tar.xz`** (Linux) — a compressed archive (like a `.zip` for Linux). You unpack it with the `tar` command in a terminal.

### TR300 — Machine Report Tool (v3.6.0)

All TR300 files are inside the **`TR300-qube-machine-report/`** folder.

| Your Computer | File to Download | Location in Folder |
|---------------|------------------|--------------------|
| **Mac** with Apple M1, M2, M3, or M4 chip | `tr300-aarch64-apple-darwin.dmg` | `macos/` |
| **Mac** with Intel processor | `tr300-x86_64-apple-darwin.dmg` | `macos/` |
| **Windows** PC (installer — recommended) | `tr-300-x86_64-pc-windows-msvc.msi` | `windows/` |
| **Windows** PC (portable — no install needed) | `tr-300-x86_64-pc-windows-msvc.zip` | `windows/` |
| **Linux** PC (Ubuntu, Fedora, Debian, etc.) | `tr-300-x86_64-unknown-linux-gnu.tar.xz` | `linux/` |
| **Linux** on Raspberry Pi or ARM server | `tr-300-aarch64-unknown-linux-gnu.tar.xz` | `linux/` |
| **Linux** on Alpine or in a Docker container | `tr-300-x86_64-unknown-linux-musl.tar.xz` | `linux/` |

### ND300 — Network Diagnostics Tool (v2.6.0)

All ND300 files are inside the **`ND300-qube-network-diagnostics/`** folder.

| Your Computer | File to Download | Location in Folder |
|---------------|------------------|--------------------|
| **Mac** with Apple M1, M2, M3, or M4 chip | `nd300-aarch64-apple-darwin.dmg` | `macos/` |
| **Mac** with Intel processor | `nd300-x86_64-apple-darwin.dmg` | `macos/` |
| **Windows** PC (installer — recommended) | `nd-300-x86_64-pc-windows-msvc.msi` | `windows/` |
| **Windows** PC (portable — no install needed) | `nd-300-x86_64-pc-windows-msvc.zip` | `windows/` |
| **Linux** PC (Ubuntu, Fedora, Debian, etc.) | `nd-300-x86_64-unknown-linux-gnu.tar.xz` | `linux/` |
| **Linux** on Raspberry Pi or ARM server | `nd-300-aarch64-unknown-linux-gnu.tar.xz` | `linux/` |
| **Linux** on Alpine or in a Docker container | `nd-300-x86_64-unknown-linux-musl.tar.xz` | `linux/` |

### SD300 — System Diagnostics Tool (v1.2.1)

All SD300 files are inside the **`SD300-qube-system-diagnostics/`** folder.

| Your Computer | File to Download | Location in Folder |
|---------------|------------------|--------------------|
| **Mac** with Apple M1, M2, M3, or M4 chip | `sd300-aarch64-apple-darwin.dmg` | `macos/` |
| **Mac** with Intel processor | `sd300-x86_64-apple-darwin.dmg` | `macos/` |
| **Windows** PC (installer — recommended) | `sd-300-x86_64-pc-windows-msvc.msi` | `windows/` |
| **Windows** PC (portable — no install needed) | `sd-300-x86_64-pc-windows-msvc.zip` | `windows/` |
| **Linux** PC (Ubuntu, Fedora, Debian, etc.) | `sd-300-x86_64-unknown-linux-gnu.tar.xz` | `linux/` |
| **Linux** on Raspberry Pi or ARM server | `sd-300-aarch64-unknown-linux-gnu.tar.xz` | `linux/` |
| **Linux** on Alpine or in a Docker container | `sd-300-x86_64-unknown-linux-musl.tar.xz` | `linux/` |

---

## Step 3: Install It

Follow the instructions for your operating system below. The steps are the same for all three tools (TR300, ND300, and SD300) — just use the file you picked in Step 2.

### Mac

1. **Double-click** the `.dmg` file. A small window (disk image) will open showing the tool inside.

2. **Copy the tool** to your Desktop: drag the file from the disk image window to your Desktop (or any folder you'd like to keep it in).

3. **First time running it:** Since these tools aren't downloaded from the Mac App Store, macOS will show a security warning the first time you open one. To get past it:
   - **Right-click** (or Control-click) the tool on your Desktop.
   - Click **"Open"** from the menu.
   - In the dialog that appears, click **"Open"** again to confirm.
   - You only need to do this once per tool — after that it will open normally.

4. **Run the tool:** Open **Terminal** (search for "Terminal" in Spotlight, or find it in Applications → Utilities) and type:
   ```
   ~/Desktop/tr300
   ```
   (Replace `tr300` with `nd300` or `sd300` depending on which tool you're using.)

5. **Eject the disk image** when you're done: right-click the disk image on your Desktop and choose **"Eject"**.

### Windows

#### Using the Installer (`.msi` file — recommended)

1. **Double-click** the `.msi` file.

2. **Follow the installation wizard.** Click "Next" through the prompts and then "Install". The tool will be installed and added to your system automatically.

3. **Run the tool:** Open **Command Prompt** (press the Windows key, type `cmd`, and press Enter) and type the tool name:
   ```
   tr300
   ```
   (Replace `tr300` with `nd300` or `sd300` depending on which tool you installed.)

> **If you see a "Windows protected your PC" warning:** Click **"More info"**, then click **"Run anyway"**. This appears because the installer isn't from the Microsoft Store — it's safe to proceed.

#### Using the Portable Zip (no installation needed)

1. **Right-click** the `.zip` file and choose **"Extract All..."**, then click **"Extract"**.

2. **Open the extracted folder.** You'll see a file called `tr300.exe` (or `nd300.exe` / `sd300.exe`).

3. **Run it:** Open **Command Prompt** in that folder (type `cmd` in the folder's address bar and press Enter), then type:
   ```
   .\tr300.exe
   ```

### Linux

1. **Extract the archive.** Open a terminal in the folder where you saved the file, then run:
   ```bash
   tar -xf tr-300-x86_64-unknown-linux-gnu.tar.xz
   ```
   (Use the exact filename you downloaded — it will differ based on your architecture.)

2. **Make it executable and run it:**
   ```bash
   chmod +x tr300
   ./tr300
   ```
   (Replace `tr300` with `nd300` or `sd300` depending on which tool you're using.)

3. **Optional — install it system-wide** so you can run it from anywhere:
   ```bash
   sudo cp tr300 /usr/local/bin/
   tr300
   ```

---

## Troubleshooting

### Mac: "macOS cannot verify that this app is free from malware"

This appears because the tools are signed by a developer but not submitted to Apple's review service. It's safe to proceed.

**Fix:** Right-click the tool → click **"Open"** → click **"Open"** again in the dialog. You only need to do this once.

**Alternative fix (for Terminal users):** Run this command to remove the quarantine flag:
```bash
xattr -d com.apple.quarantine ~/Desktop/tr300
```

### Windows: "Windows protected your PC" (SmartScreen)

This appears because the installer is from an independent developer, not the Microsoft Store.

**Fix:** Click **"More info"** → click **"Run anyway"**.

### Linux: "Permission denied"

This means the file isn't marked as executable yet.

**Fix:** Run `chmod +x tr300` (replacing `tr300` with the tool name), then try again.

### Windows on ARM Laptop (Surface Pro X, Snapdragon, etc.)

The standard Windows files work on ARM laptops too — Windows automatically translates them. Just use the regular Windows `.msi` or `.zip` file from the tables above.

### "I don't know which file to pick"

- **Mac users:** If your Mac was made in **2021 or later**, it almost certainly has an Apple chip (M1/M2/M3/M4). Use the first Mac option in the table. Older Macs use Intel — use the second Mac option.
- **Windows users:** Almost all Windows PCs use the same file. Just grab the `.msi` (installer) option.
- **Linux users:** If you're not sure, try the first Linux option in the table (`x86_64-unknown-linux-gnu`). It works on the vast majority of Linux desktops and servers.

---

## Need More Help?

For detailed technical documentation, see the [README.md](./README.md) in this same folder. It covers SHA256 checksum verification, code signing details, and platform support notes.
