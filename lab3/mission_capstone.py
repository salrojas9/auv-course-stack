"""
Lab 3 — Mission Capstone (Part I finale)
Intro to Autonomous Robotics (AUV) · after Lecture 4

You built the loop in class: sense -> think -> act. This lab makes it a
VEHICLE: a battery that drains, a safety system that can override the
mission, and a full dive-cruise-surface run — using the same `step`,
`read_depth`, and `depth_controller` you met in `sim/hello_robot.py`
(imported below; read that file first, it is short and honest).

Run me from the repo root:   python3 lab3/mission_capstone.py
I self-grade: 3 checks. 3/3 = submit on Canvas (this file + logbook).

LOGBOOK (submit alongside the code):
  1. Your chosen Kp, its PREDICTED hold offset 0.03/Kp [m] (Lecture 4,
     "Why it never quite arrives"), and the MEASURED offset this file
     prints. Do they agree? One sentence why.
  2. Your battery numbers: with DRAIN = 0.02 V per (command-unit·s), how
     many minutes would a full battery last at full effort (|u|+|r|+|w|
     = 1.5)? Show the arithmetic. Is that plausible for a real AUV?
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
from sim.hello_robot import step, read_depth, depth_controller, DT

# Vehicle constants — the self-check depends on these exact values;
# argue with them in the logbook, not in the code.
V_FULL = 16.8   # [V] a fresh 4S battery
V_MIN  = 14.0   # [V] below this, electronics brown out -> abort
D_MAX  = 2.5    # [m] the pool is 3 m deep; past 2.5 we abort
DRAIN  = 0.02   # [V per command-unit-second] how effort costs charge


def battery_step(v, cmd):
    """Return the battery voltage after ONE tick of running command `cmd`.

    Effort this tick is |u| + |r| + |w| (add the absolute values of the
    three commands). Voltage drops by DRAIN * effort * DT.
    Pattern: one line of arithmetic, then return the new voltage.
    """
    raise NotImplementedError("implement me — one Euler step, but for charge")


def safety_abort(depth, battery_v):
    """Return None if all is well; otherwise the REASON we must surface.

    Check depth FIRST: if depth > D_MAX      -> return "depth"
    then battery:      if battery_v < V_MIN  -> return "battery"
    otherwise                                 -> return None
    (A conditional chain — Lecture 3's if/elif/else, guarding a robot.)
    """
    raise NotImplementedError("implement me — if / elif / else, three lines")


def run_capstone(Kp):
    """Fly the full mission. Return (t, depth_true, volts, abort_reason).

    Recipe (every piece is from Lecture 4 — cite your notes line by line):
      1. Born-empty stories: t_log, d_log, v_log = [], [], []
         Born-full state:    s = np.array([0., 0., 0., 0.]); v = V_FULL
         abort_reason = None; t = 0.0
      2. The plan, born full — (surge, yaw-rate, depth-target, seconds):
         phases = [(0.5, 0.0, 1.2, 20.0),   # dive + hold
                   (0.4, 0.3, 1.2, 10.0),   # turning cruise, holding depth
                   (0.5, 0.0, 0.0, 20.0)]   # surface: target 0 — same law!
      3. For each phase, for each tick (int(seconds/DT) of them):
           z = read_depth(s)                        # SENSE (the lie)
           w = depth_controller(z, target, Kp=Kp)   # THINK (your Kp!)
           s = step(s, [u, r, w])                   # ACT
           v = battery_step(v, [u, r, w])           # pay for it
           t += DT; append t, s[3], v to the logs   # remember everything
           if abort_reason is None:
               abort_reason = safety_abort(s[3], v) # the guard, every tick
      4. Return np.array(t_log), np.array(d_log), np.array(v_log), abort_reason
    (With sane Kp nothing aborts — the guard earns its keep the day
     something breaks. That is what safety systems are for.)
    """
    raise NotImplementedError("implement me — the loop you built in class, grown up")


# ----------------------- self-check: do not edit below -----------------------
if __name__ == "__main__":
    ok = 0

    try:  # [1] battery physics
        v1 = battery_step(V_FULL, [0.5, 0.0, 0.4])          # effort 0.9
        v100 = V_FULL
        for _ in range(100):                                 # 10 s cruising
            v100 = battery_step(v100, [0.6, 0.0, 0.0])
        assert abs(v1 - 16.79820) < 1e-6, f"one tick: got {v1:.5f}, want 16.79820"
        assert abs(v100 - 16.68) < 1e-6, f"100 ticks: got {v100:.5f}, want 16.68000"
        print("[OK ] battery_step: charge pays for effort, tick by tick")
        ok += 1
    except NotImplementedError:
        print("[    ] battery_step not implemented yet")
    except AssertionError as e:
        print(f"[FAIL] battery_step: {e}")

    try:  # [2] the guard's truth table
        assert safety_abort(1.0, 16.0) is None, "safe case must return None"
        assert safety_abort(2.6, 16.0) == "depth", "too deep -> 'depth'"
        assert safety_abort(1.0, 13.9) == "battery", "low volts -> 'battery'"
        assert safety_abort(2.6, 13.9) == "depth", "depth is checked first"
        print("[OK ] safety_abort: all four cases of the truth table")
        ok += 1
    except NotImplementedError:
        print("[    ] safety_abort not implemented yet")
    except AssertionError as e:
        print(f"[FAIL] safety_abort: {e}")

    try:  # [3] the full mission
        Kp = 0.8                                  # grade with the lecture's Kp;
        t, d, v, why = run_capstone(Kp)           # fly YOUR Kp for the logbook
        assert len(t) == len(d) == len(v) == 500, f"50 s at 10 Hz = 500 rows, got {len(t)}"
        assert why is None, f"mission aborted ('{why}') — it shouldn't, with Kp={Kp}"
        assert d.max() < 1.8, f"max depth {d.max():.2f} m — overshooting the 1.2 m hold?"
        assert d[-1] < 0.30, f"final depth {d[-1]:.2f} m — did the surface phase run?"
        assert 15.5 < v[-1] < 16.5, f"final battery {v[-1]:.2f} V — check battery_step wiring"
        hold = d[150:200].mean() - 1.2            # late in the hold phase
        print(f"[OK ] mission: dove, held, surfaced; battery {v[-1]:.2f} V")
        print(f"      logbook: measured hold offset {hold*100:+.1f} cm "
              f"(prediction: 0.03/Kp = {3.0/Kp:.1f} cm)")
        ok += 1
    except NotImplementedError:
        print("[    ] run_capstone not implemented yet")
    except AssertionError as e:
        print(f"[FAIL] mission: {e}")

    print(f"\nLab 3 self-check: {ok}/3", end="")
    print(" — submit it. ><(((\"> " if ok == 3 else " — keep going.")
