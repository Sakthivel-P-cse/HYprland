#!/usr/bin/env python3
"""Keep native workspace-wheel binds tied to physical BTN_MIDDLE state."""
import fcntl
import glob
import os
from pathlib import Path
import select
import signal
import socket
import time

BTN_MIDDLE = 274
BITMAP_BYTES = 96
runtime = Path(os.environ["XDG_RUNTIME_DIR"])
instance = os.environ["HYPRLAND_INSTANCE_SIGNATURE"]
ipc = runtime / "hypr" / instance / ".socket.sock"
lock = open(runtime / ("middle-workspace-wheel-" + instance + ".lock"), "w")
try:
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
except BlockingIOError:
    raise SystemExit(0)


def middle_bit(fd, request):
    bits = bytearray(BITMAP_BYTES)
    fcntl.ioctl(fd, request, bits)
    return bool(bits[BTN_MIDDLE // 8] & (1 << (BTN_MIDDLE % 8)))


def set_enabled(enabled):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.settimeout(0.5)
        client.connect(str(ipc))
        client.sendall(b"/eval middle_workspace_wheel_set(" +
                       (b"true" if enabled else b"false") + b")")
        if client.recv(4096).strip() != b"ok":
            raise OSError("Hyprland rejected workspace-wheel update")


running = True


def stop(_signum, _frame):
    global running
    running = False


signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGINT, stop)
devices = {}
examined = {}
last_state = None
last_update = last_scan = 0.0
try:
    while running and ipc.exists():
        now = time.monotonic()
        if now - last_scan >= 1:
            paths = set(glob.glob("/dev/input/event*"))
            for path in list(examined):
                if path not in paths:
                    examined.pop(path)
            for path in paths:
                try:
                    identity = os.stat(path).st_ino
                except OSError:
                    continue
                if examined.get(path) == identity:
                    continue
                if path in devices:
                    os.close(devices.pop(path))
                fd = None
                try:
                    fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
                    # EVIOCGBIT(EV_KEY): select only devices with BTN_MIDDLE.
                    if middle_bit(fd, 0x80004521 | (BITMAP_BYTES << 16)):
                        devices[path] = fd
                        fd = None
                    # Closing evdev nodes can wait for RCU. Do not reopen every
                    # keyboard each scan: inspect each node identity only once.
                    examined[path] = identity
                except OSError:
                    pass
                finally:
                    if fd is not None:
                        os.close(fd)
            last_scan = time.monotonic()

        ready, _, _ = select.select(list(devices.values()), [], [], 0.2)
        held = False
        for path, fd in list(devices.items()):
            try:
                if fd in ready:
                    try:
                        os.read(fd, 4096)  # Drain mouse events only.
                    except BlockingIOError:
                        pass
                # EVIOCGKEY reads current state, including disconnect/release.
                held |= middle_bit(fd, 0x80004518 | (BITMAP_BYTES << 16))
            except OSError:
                os.close(fd)
                del devices[path]
                examined.pop(path, None)

        if held != last_state or (held and now - last_update >= 0.5):
            try:
                set_enabled(held)
                last_state, last_update = held, now
            except OSError:
                last_state = None
finally:
    try:
        set_enabled(False)
    except OSError:
        pass
    for fd in devices.values():
        os.close(fd)
