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

Razer device manager for Linux

## Installing

To install this software the first thing you need is to install `razer_drivers`. You can find installation instructions on the [project page](https://github.com/terrycain/razer-drivers).

You need 3 packages provided in the `razer-drivers`:
- `razer-driver-dkms`: the actual driver, best if installed using DKMS
- `razer-daemon`: a daemon that interfaces with the driver, providing a higher level interface for it
- `python3-razer`: a python library that interfaces with the daemon, it's used by razerCommander, thus it's a direct dependency.

### Installing on Arch Linux (or derivates: Antergos, Manjaro...)

You can find razerCommander on AUR, as `razercommander-git` ([AUR page](https://aur.archlinux.org/packages/razercommander-git)).
If you use an AUR helper, it should automatically pull `razer-driver-dkms`, `razer-daemon` and `python-razer` as dependencies.
Alternativelly you can install these packages manually, or even opt for the git version of the driver stack (`razer-driver-dkms-git`, `razer-daemon-git`, `python-razer-git`).

### Installing on Ubuntu or Debian

Go to the [releases page](https://github.com/GabMus/razerCommander/releases) and download the latest release available for your platform.

### Other distros

You'll need the following libraries to make razerCommander work:
- `GTK+>=3.14`
- `python3`
- `razer-driver-dkms`
- `razer-daemon`
- `python-razer`

Download razerCommander by following these steps:
- `mkdir git && cd git` (optional, but avoids cluttering your home folder)
- `git clone https://github.com/gabmus/razercommander`
- `cd razercommander`
- `chmod +x main.py`

## Running

Just run `./main.py` from the razerCommander directory. You can also make a .desktop file to launch it from your DE/WM (an easy way to do it is using [mlauncher](https://github.com/gabmus/mlauncher)).

## Supported hardware

- Keyboards
- Macro keypads (Tartarus, Orbweaver)
- Mice ***(only lighting effects, most macro features)***
- Laptops ***(keyboards only)***
- Headsets ***(possibly, untested)***
- Mousepads (Firefly)

## How can you help?

Please, fill up issues and help me test this little piece of software with as much hardware as possible.
