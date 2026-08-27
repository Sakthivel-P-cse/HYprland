#!/usr/bin/env zsh

set -euo pipefail

readonly external_output="DP-2"
readonly laptop_output="eDP-1"
readonly external_rule='hl.monitor({ output = "DP-2", mode = "2560x1440@200", position = "0x0", scale = 1, disabled = false })'

if ! hyprctl monitors all -j | jq -e --arg output "$external_output" \
    'any(.[]; .name == $output)' >/dev/null; then
    print -u2 -- "${0:t}: $external_output is not connected; display layout was not changed."
    exit 1
fi

case "${0:t}" in
    lid-close)
        hyprctl eval "$external_rule"
        hyprctl eval 'hl.monitor({ output = "eDP-1", disabled = true })'
        print -- "$external_output is now the only display."
        ;;
    lid-open)
        hyprctl eval "$external_rule"
        hyprctl eval 'hl.monitor({ output = "eDP-1", mode = "preferred", position = "2560x0", scale = 1, disabled = false })'
        print -- "$external_output is first; $laptop_output is restored on the right."
        ;;
    *)
        print -u2 -- "Run this script as lid-close or lid-open."
        exit 2
        ;;
esac
