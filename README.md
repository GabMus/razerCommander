# NOTICE: repo moved to <https://gitlab.com/gabmus/razercommander>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# <img src="data/icons/org.gabmus.razercommander.svg" align="left" height="48" width="48" >[razerCommander](https://gabmus.github.io/razerCommander)

- [Website](https://gabmus.github.io/razerCommander)
- [GitHub](https://github.com/gabmus/razercommander)
- [GNOME GitLab](https://gitlab.gnome.org/GabMus/razercommander)

![screenshot](preview.gif)

Razer device manager for Linux

## Supported hardware

Any of the devices supported by the driver stack should work fine in razerCommander.

For a detailed list of supported devices refer to [this page](https://openrazer.github.io/)

-   Keyboards
-   Macro keypads (Tartarus, Orbweaver)
-   Mice
-   Laptops ***(keyboards only)***
-   Headsets ***(possibly, untested)***
-   Mousepads (Firefly)

## Requirements

To install this software the first thing you need is to install the Openrazer driver. You can find installation instructions on the [Openrazer website](https://openrazer.github.io/).

You need 3 packages provided by `openrazer-drivers`:
-   `openrazer-driver-dkms`: the actual driver, best if installed using DKMS
-   `openrazer-daemon`: a daemon that interfaces with the driver, providing a higher level interface for it
-   `python3-openrazer`: a python library that interfaces with the daemon, it's used by razerCommander, thus it's a direct dependency.

## Installing

### Installing on Arch Linux/Antergos/Manjaro

You can find razerCommander on AUR, as `razercommander-git` ([AUR page](https://aur.archlinux.org/packages/razercommander-git)).
If you use an AUR helper, it should automatically pull `openrazer-driver-dkms`, `openrazer-daemon` and `python-openrazer` as dependencies.

Alternatively you can install these packages manually, or even opt for the git version of the driver stack (`openrazer-driver-dkms-git`, `openrazer-daemon-git`, `python-openrazer-git`).

### Installing on Ubuntu/Debian

**Note**: you will need python 3.6+ to run razerCommander. Here's [how to install python 3.6 on Ubuntu 16.04](https://askubuntu.com/questions/865554/how-do-i-install-python-3-6-using-apt-get/865569#865569)

Go to the [releases page](https://github.com/GabMus/razerCommander/releases) and download the latest release available for your platform.

Alternatively you can build a .deb package following the instructions below.

### Installing on Fedora/RHEL/CentOS

Go to the [releases page](https://github.com/GabMus/razerCommander/releases) and download the latest release available for your platform.

Alternatively you can build a .rpm package following the instructions below.

### Other distros

You can either run razerCommander without installing it (refer to the [Building for testing section](#building-for-testing)), or install it in your system (refer to the [Installing systemwide directly section](#build-and-install-systemwide-directly)).

## Building

### Building for testing

This is the best practice to test razerCommander without installing using meson and ninja.

#### First time

```bash
git clone https://github.com/gabmus/razercommander
cd razercommander
mkdir builddir
cd builddir
meson ..
meson configure -Dprefix=$(pwd)/testdir
ninja install # This will actually install in razercommander/builddir/testdir
ninja run
```

#### Later on

```bash
cd razercommander/builddir
ninja install # This will actually install in razercommander/builddir/testdir
ninja run
```

### Building for Debian/Ubuntu

Build dependencies: `libglib2.0-dev pkg-config libappstream-glib-dev`

WIP

### Building for Fedora/RHEL/CentOS

WIP

### Building for Flatpak

First install `flatpak` and `flatpak-builder` from your distro repository. Although it's not necessary, you may also want to install `gnome-software`.

Create a directory somewhere in your home, I suggest something like `~/razercommanderflatpak`.

Either clone the whole razerCommander repo (`git clone https://github.com/gabmus/razercommander`) or just download the flatpak manifest file from this repo in `dist/flatpak/org.gabmus.razercommander.json`. In either case, put the files inside the directory you created before.

Run the following: `flatpak-builder --repo=repo razercommander $PATH_TO_MANIFEST` where `$PATH_TO_MANIFEST` is the path to the `org.gabmus.razercommander.json` flatpak manifest. If everything works correctly, this command should create two directories `repo` and `razercommander` with flatpak stuff inside of your present working directory (again, I suggest to run everything inside a specifically designated directory).

Now you'll be creating a flatpak bundle, so that you can install it and distribute it without messing with flatpak repos. To do this you run `flatpak build-bundle repo razercommander.flatpak org.gabmus.razercommander`. This will give you a razercommander.flatpak file inside your present working directory. To install it, either open it with `gnome-software` or run `flatpak install razercommander.flatpak`.

*Note: I am a just a beginner with flatpak, and probably some of the instructions I gave in this section of the readme are wrong or could be done better. If you know a better way of doing this, please don't hesitate to make a pull request or open an issue.*

### Build and install systemwide directly

This approach is discouraged, since it will manually copy all the files in your system. Uninstalling could be difficult and/or dangerous.

But if you know what you're doing, here you go:

```bash
git clone https://github.com/gabmus/razercommander
cd razercommander
mkdir builddir
cd builddir
meson ..
ninja install
```

## How can you help?

Please, fill up issues and help me test this little piece of software with as much hardware as possible.
