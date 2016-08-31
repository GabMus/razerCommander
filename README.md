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

# razerCommander

![screenshot](preview.gif)

A simple GTK control center for managing razer peripherals on Linux.

## Installing

To install this software the first thing you need is to install `razer_drivers`: an unofficial driver for razer peripherals for Linux. Go to the [project page](https://github.com/terrycain/razer-drivers) to find out more about it and how to install it. (There are different packages available, as well as PKGBUILDs if you're using Arch)

You need 3 packages provided in the `razer-drivers`:
- `razer-driver-dkms`: the actual driver, best if installed using DKMS
- `razer-daemon`: a daemon that interfaces with the driver, providing a higher level interface with it
- `python3-razer`: a python library that interfaces with the daemon, it's used by razerCommander, thus it's needed to use it

### Installing on Arch Linux (or derivates: Antergos, Manjaro...)

You can find razerCommander on AUR, as `razercommander-git` ([AUR page](https://aur.archlinux.org/packages/razercommander-git)).
You still need to install `razer-drivers` manually, as it's still not available on AUR.

### Installing on Ubuntu or Debian

Go to the [releases page](https://github.com/GabMus/razerCommander/releases) and download the latest release available for your platform.

### Other distros

You'll need the following libraries to make razerCommander work:
- GTK+ >=3.18 (could work with previous versions, but I'm not sure)
- python3

To download razerCommander you have to follow these steps:
- Clone this repo (`git clone https://github.com/gabmus/razercommander`)
- `cd` into the newly cloned folder (`cd razercommander`)
- Run `chmod +x main.py`

## Running

Just run `./main.py` from the razerCommander directory. You can also make a .desktop file to launch it from your DE/WM (an easy way to do it is using [mlauncher](https://github.com/gabmus/mlauncher)).

## Supported hardware

As far as support goes, in theory this software should support every device supported by the `razer-drivers` package.

razerCommander has been created to work with keyboards, but may work with mice and firefly mousepads, too.

## How can you help?

Please, fill up issues and help me test this little piece of software with as much hardware as possible.
