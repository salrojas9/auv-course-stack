"""
Lab 4 — The Filtered Mission
Intro to Autonomous Robotics (AUV) · after Lectures 5 and 6

Lab 3 flew the mission on raw readings. Lab 4 flies the SAME plan on a
belief: Lecture 6's filter, predict every tick and correct when a reading
arrives. Two things fight you. The sensor dies for 5 s in the turn (a
blackout), and YOUR water is heavier than the model believes.

Run me from the repo root:   python3 lab4/lab4_mission.py
I self-grade: 3 checks. 3/3 = submit on Canvas (this file + logbook).

Submit TWO files in ONE submission:  [ lab4_mission.py ] + [ logbook.txt ]

YOUR NUMBERS (set them in my_numbers() below; they make your run yours alone):
  seed  your sensor's seed, drawn for you: run me once with it unset, and I
        print one whole number from 1000 to 9999. Put it in my_numbers(),
        and record it in your logbook as SEED.
  sink  your water's real sink rate in m/s, your one real choice: any value
        from 0.031 to 0.050, with exactly three decimals. The model still
        believes 0.03, so the gap between your sink and 0.03 is the error
        your estimator must correct for.

THE NOISE, exactly: one lie every tick, the blackout included.
    rng = np.random.default_rng(seed)     # once, before the loop
    lie = rng.normal(0.0, 0.05)           # every tick, even when blind
    z = s[3] + lie                        # outside the blackout
    z = None                              # inside it: 22.0 <= k * DT < 27.0

A WORKED EXAMPLE, never yours: seed 7 is below 1000 and sink 0.090 is above
0.050, so check [1] refuses them, and no run of yours can print these
numbers. Flown through the recipe in run_filtered(), (7, 0.090) gives:
      settles 26.62 cm deep of target · depth jitter 0.28 cm · cmd jitter 0.27 cm/s
      drift 30.00 cm across the blackout

LOGBOOK (logbook.txt, beside this file): write PREDICTED_DRIFT BEFORE you
run, then copy your two numbers and your run's four labels into the
KEY = value lines, and answer its two questions.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
from sim.hello_robot import step, depth_controller, DT
from sim.estimator import predict, correct


def my_numbers():
    """Return (seed, sink): your two numbers, set in code (see YOUR NUMBERS).

    seed is the whole number this starter drew for you on your first run;
    sink is a float with three decimals, from 0.031 to 0.050: your water's
    sink rate. Its gap from the model's 0.03 is the error your estimator must
    correct for. The self-check prints both back in its first line, and your
    logbook records the same two.
    """
    seed = None    # your seed: run me once with it unset, and I print one to put here
    sink = None    # your water's sink rate [m/s], three decimals
    if seed is None:   # one draw from the operating system's randomness: never the clock, never anything of yours
        import secrets
        drawn = secrets.randbelow(9000) + 1000
        print(f"Your seed is {drawn}. Put it in my_numbers() and record it in your logbook as SEED = {drawn}.")
    return seed, sink


def run_filtered(seed, sink):
    """Fly Lab 3's plan on your Kalman belief. Return four stories, each an
    np array with one row per tick (500 of them): (truth, belief, push,
    doubt), logged BEFORE each step (Lecture 4's order: sense, think, act).

    Recipe (Lab 3's loop, with Lecture 6 between SENSE and THINK):
      1. rng = np.random.default_rng(seed)              # your lies
         s = np.array([0., 0., 0., 0.])                 # at the surface, at rest
         est, P, w = 0.0, 0.0, 0.0                      # belief, doubt, last push
         d_log, e_log, w_log, P_log = [], [], [], []
      2. The plan, Lab 3's, born full (surge, yaw-rate, depth-target, seconds):
         phases = [(0.5, 0.0, 1.2, 20.0),   # dive + hold
                   (0.4, 0.3, 1.2, 10.0),   # turning cruise: the blackout is here
                   (0.5, 0.0, 0.0, 20.0)]   # surface
      3. For each phase, for each tick (int(seconds/DT) of them), with k
         counting every tick of the mission from 0:
           lie = rng.normal(0.0, 0.05)                         # one lie EVERY tick
           z = None if 22.0 <= k * DT < 27.0 else s[3] + lie   # SENSE (blind?)
           est, P = predict(est, P, w)                         # the model speaks
           if z is not None:
               est, P = correct(est, P, z)                     # the sensor speaks
           w = depth_controller(est, target)                   # THINK, on the belief
           append s[3], est, w, P to the four logs             # remember, BEFORE acting
           s = step(s, [u, r, w], disturbance=sink)            # ACT, in YOUR water
      4. Return np.array(d_log), np.array(e_log), np.array(w_log), np.array(P_log)
    Lecture 5's spelling works too: on a reading, predict_correct with the
    gain K = P / (P + R) is the same update; when blind, predict alone.
    """
    raise NotImplementedError("implement me — Lab 3's loop, fed your Kalman belief")


# Run the scaffold — don't edit it. Your work goes above this line; the
# self-check below is the harness's, and the grader runs its own copy.
# ----------------------- self-check: do not edit below -----------------------
if __name__ == "__main__":
    # The harness's own copies of the arithmetic and the lab's constants: pinned
    # here, never read from sim/ while it checks you.
    _DT, _Q, _R, _N = 0.1, 0.002 ** 2, 0.05 ** 2, 500
    _PLAN = [(0.5, 0.0, 1.2, 20.0), (0.4, 0.3, 1.2, 10.0), (0.5, 0.0, 0.0, 20.0)]
    _GAP = (22.0, 27.0)
    _TARGETS = [target for _, _, target, secs in _PLAN for _ in range(int(round(secs / _DT)))]

    def _predict(est, P, w):
        return max(0.0, est + (w + 0.03) * _DT), P + _Q

    def _correct(pred, P, z):
        K = P / (P + _R)
        return pred + K * (z - pred), (1 - K) * P

    def _law(est, target):
        return max(-0.4, min(0.4, 0.8 * (target - est)))

    def _fmt(x):
        return f"{round(x, 2) + 0.0:.2f}"

    def _replay(seed, sink, stories, lo, hi):
        """The first relation your loop breaks in ticks lo..hi-1, in words; None if every tick replays."""
        ds, es, ws, Ps = stories
        lies = np.random.default_rng(seed).normal(0.0, 0.05, size=_N)
        for k in range(lo, hi):
            d0, e0, w0, P0 = (0.0, 0.0, 0.0, 0.0) if k == 0 else (ds[k - 1], es[k - 1], ws[k - 1], Ps[k - 1])
            truth = 0.0 if k == 0 else max(0.0, d0 + (w0 + sink) * _DT)
            if not abs(ds[k] - truth) <= 1e-9:          # a NaN fails too
                return "the truth does not move by step() in your water, from your last push"
            z = None if _GAP[0] <= k * _DT < _GAP[1] else ds[k] + lies[k]
            est, P = _predict(e0, P0, w0)
            if z is not None:
                est, P = _correct(est, P, z)
            if not abs(Ps[k] - P) <= 1e-12:
                return "the doubt is not predict on every tick, then correct only on a reading"
            if not abs(es[k] - est) <= 1e-9:
                return "the belief is not your prediction corrected by your reading, one lie every tick"
            if not abs(ws[k] - _law(es[k], _TARGETS[k])) <= 1e-9:
                return "the push is not the law on your belief, toward the phase's target"
        return None

    ok, numbers, stories, why_not = 0, None, None, "waiting on your numbers (check [1])"

    try:  # [1] your numbers
        seed, sink = my_numbers()
        if seed is None or sink is None:
            raise NotImplementedError
        if not (isinstance(seed, int) and not isinstance(seed, bool) and 1000 <= seed <= 9999):
            print("[FAIL] your numbers: seed must be a whole number in its range, from your box (see YOUR NUMBERS)")
        elif not (isinstance(sink, float) and 0.031 <= sink <= 0.050 and float(f"{sink:.3f}") == sink):
            print("[FAIL] your numbers: sink must be a float in its range, with exactly three decimals (see YOUR NUMBERS)")
        else:
            print(f"[OK ] your numbers: seed={seed} sink={sink:.3f} m/s")
            numbers = (seed, sink)
            ok += 1
    except NotImplementedError:
        print("[    ] your numbers are not set yet: my_numbers()")
    except Exception as e:
        print(f"[FAIL] your numbers: my_numbers() raised {type(e).__name__}")

    if numbers is not None:
        try:
            stories = [np.asarray(story, dtype=float) for story in run_filtered(*numbers)]
            if len(stories) != 4 or any(story.shape != (_N,) for story in stories):
                stories, why_not = None, "run_filtered() must return four stories, one row per tick"
        except NotImplementedError:
            why_not = "run_filtered() is not implemented yet"
        except Exception as e:
            why_not = f"run_filtered() raised {type(e).__name__}"

    for check, name, lo, hi in (("[2]", "dive and hold, ticks 0-199", 0, 200),
                                ("[3]", "blackout and surface, ticks 200-499", 200, _N)):
        try:
            if stories is None:
                print(f"[{'    ' if why_not.startswith(('waiting', 'run_filtered() is not')) else 'FAIL'}] {name}: {why_not}")
                continue
            why = _replay(numbers[0], numbers[1], stories, lo, hi)
            if why is not None:
                print(f"[FAIL] {name}: {why}")
                continue
            ds, es, ws, Ps = stories
            print(f"[OK ] {name}: every tick of your loop replays")
            if check == "[2]":
                print(f"      settles {_fmt((ds[100:200].mean() - 1.2) * 100)} cm deep of target"
                      f" · depth jitter {_fmt(ds[100:200].std() * 100)} cm"
                      f" · cmd jitter {_fmt(ws[100:200].std() * 100)} cm/s")
            else:
                print(f"      drift {_fmt(((ds[269] - es[269]) - (ds[219] - es[219])) * 100)} cm across the blackout")
            ok += 1
        except Exception as e:
            print(f"[FAIL] {name}: the check could not read your stories ({type(e).__name__})")

    print(f"\nLab 4 self-check: {ok}/3", end="")
    print(" — submit it. ><(((\"> " if ok == 3 else " — keep going.")
