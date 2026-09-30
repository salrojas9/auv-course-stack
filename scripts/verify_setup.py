#!/usr/bin/env python3
"""
verify_setup.py — Lab 0.
If your environment is healthy, a fish swims across your terminal.
Screenshot the fish: that is your Lab 0 submission.
"""
import sys
import time

REQUIRED = (3, 10)
CHECKS = []


def check(name, ok, hint=""):
    CHECKS.append(ok)
    mark = "OK " if ok else "FAIL"
    print(f"[{mark}] {name}" + ("" if ok else f"\n       fix: {hint}"))
    return ok


def main():
    print("— AUV course environment check —\n")

    check(
        f"Python {sys.version_info.major}.{sys.version_info.minor} "
        f"(need >= {REQUIRED[0]}.{REQUIRED[1]})",
        sys.version_info >= REQUIRED,
        "you are outside the course container, or it needs rebuilding",
    )

    check(
        "running on Linux (i.e., inside the container)",
        sys.platform.startswith("linux"),
        "open this folder in VS Code and click 'Reopen in Container'",
    )

    try:
        import numpy  # noqa: F401
        ok_np = True
    except ImportError:
        ok_np = False
    check("numpy importable", ok_np, "container image incomplete — ask a TA")

    try:
        import matplotlib  # noqa: F401
        ok_mpl = True
    except ImportError:
        ok_mpl = False
    check("matplotlib importable", ok_mpl, "container image incomplete — ask a TA")

    print()
    if all(CHECKS):
        fish, water = '><((("> ', "~"
        width = 34
        try:
            for i in range(width):
                line = water * i + fish + water * (width - i)
                print("\r" + line, end="", flush=True)
                time.sleep(0.04)
            print("\n\nSUCCESS — your workstation is a robotics workstation.")
        except Exception:
            print(fish + "\nSUCCESS — your workstation is a robotics workstation.")
        print("Screenshot this and submit as Lab 0.")
        return 0
    print("Not yet — fix the FAIL lines above (hints given), then rerun:")
    print("  python3 verify_setup.py")
    return 1


if __name__ == "__main__":
    sys.exit(main())
