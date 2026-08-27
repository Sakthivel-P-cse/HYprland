#!/usr/bin/env zsh

set -euo pipefail

readonly external_output="DP-2"
readonly external_rule='hl.monitor({ output = "DP-2", mode = "2560x1440@200", position = "0x0", scale = 1, disabled = false })'
readonly max_attempts=20
readonly retry_delay=1

integer attempt=1
while (( attempt <= max_attempts )); do
    if hyprctl monitors all -j 2>/dev/null | jq -e --arg output "$external_output" \
        'any(.[]; .name == $output)' >/dev/null; then
        # The DP link can be present before the compositor is ready to accept
        # the monitor rule. Retry the whole recovery while the output settles.
        if hyprctl eval "$external_rule" >/dev/null 2>&1 && \
            hyprctl eval 'hl.dsp.dpms("on")' >/dev/null 2>&1; then
            exit 0
        fi
    fi

    if (( attempt < max_attempts )); then
        sleep "$retry_delay"
    fi
    (( attempt += 1 ))
done

print -u2 -- "$0:t: could not restore $external_output after suspend."
exit 1
