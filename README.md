# Hyprland UI Configuration

Personal Hyprland desktop configuration for a Wayland session. The setup is
modular, Lua-based, and centered around a small set of external desktop tools.
It is tailored to the author's hardware and installed applications, so it is
not a drop-in configuration for another machine.

## What is included

- `hyprland.lua` — main Lua configuration and module loader.
- `conf/` — appearance, autostart, input, keybindings, and window rules.
- `themes/` — Macchiato and Matrix Hyprland/Hyprlock themes.
- `hypridle.conf` — idle, lock, display power, and suspend timers.
- `hyprpaper.conf` — wallpaper configuration.
- `scripts/` — local OSD, connectivity, Bluetooth, keybinding, and display-resume helpers.
- `system/` — source for the charger-dependent AMD power-mode service.
- `hyprland.conf` — small generated/stub configuration retained for compatibility.

The active `theme.lua` and `hyprlock.conf` entries are symbolic links to the
currently selected files in `themes/`. Their current targets contain absolute
paths and must be recreated when this repository is installed elsewhere.

## Desktop components

The configuration expects these components to be installed separately:

- Hyprland with Lua configuration support
- Kitty, Nemo/Yazi, Firefox, Brave, VS Code or Code, Cursor, Obsidian, and Rofi/Hyprlauncher
- Waybar, Swaync, Hypridle, Hyprlock, Wlogout, Awww, and Hyprpaper
- `wl-clipboard`, `cliphist`, `grim`, `slurp`, `grimblast`, and `swappy`
- `playerctl`, `brightnessctl`, `hyprpicker`, and a PolicyKit authentication agent

Some commands are provided by related configurations outside this repository,
including Waybar theme and idle-toggle scripts. Missing optional applications
will make only their corresponding keybindings unavailable.

## Main controls

`SUPER` is the main modifier.

| Shortcut | Action |
| --- | --- |
| `SUPER + T` / `SUPER + RETURN` | Open Kitty |
| `SUPER + E` | Open the file manager |
| `SUPER + R` | Open the application launcher |
| `SUPER + Q` | Close the focused window |
| `SUPER + W` | Toggle floating |
| `SUPER + F` | Open Firefox |
| `SUPER + L` | Lock the session |
| `SUPER + ESCAPE` | Open the logout menu |
| `SUPER + 1-0` | Switch workspace |
| `SUPER + SHIFT + 1-0` | Move the window to a workspace |
| `SUPER + arrows` | Change focus |
| `SUPER + SHIFT + arrows` | Move the window |
| `SUPER + CTRL + arrows` | Resize the window |
| `SUPER + I` | Open the keybinding cheat sheet |
| `SUPER + SHIFT + I` | Select the Matrix theme |
| `SUPER + CTRL + I` | Select the Macchiato theme |
| `Print` | Capture the full screen |

The complete binding definitions are in `conf/keybinds.lua`.

## Themes

- **Macchiato** — soft Catppuccin-inspired colors, rounded corners, and lower inactive-window opacity.
- **Matrix** — dark black borders, tighter styling, and higher inactive-window opacity.

Theme switching is configured through external Waybar scripts. If those
scripts are unavailable, switch the `theme.lua` and `hyprlock.conf` symlinks
manually to matching files in `themes/`, then reload Hyprland.

## Adapting the configuration

Before using this on another system, review:

1. Monitor names and layouts in `hyprland.lua`.
2. Application names and launcher paths in `hyprland.lua` and `conf/keybinds.lua`.
3. Startup commands and wallpaper paths in `conf/autostart.lua` and `hyprpaper.conf`.
4. Device-specific input rules in `conf/input.lua`.
5. Absolute paths in the tracked symbolic links.

Reload Hyprland only after checking that each referenced command and file
exists on the target system.

## Repository safety

This repository describes a personal system configuration. Keep it private
unless host-specific paths, usernames, secrets, and other identifying details
have been removed.
