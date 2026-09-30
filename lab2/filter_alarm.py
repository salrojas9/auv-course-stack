"""
Lab 2 — Filter & Alarm (due Friday; submit on Canvas)

Implement the two functions below, then run this file to grade yourself:

    cd /workspaces/auv-course-student && pwd
    python3 lab2/filter_alarm.py

Rules: implement moving_average from your Lecture 3 notes WITHOUT peeking at
the filled slides. The self-check at the bottom tells you PASS/FAIL per part.

Logbook questions (answer in your submission text):
  1. With N = 40 the alarm fires late. How late, in seconds?
  2. Would you bet a $2,000 vehicle on N = 40? What N do you choose,
     and what did you trade away to get it?
"""
import numpy as np


def moving_average(z, N):
    """Return the moving average of sequence z with window size N.

    out[k] = mean of the last N readings up to and including z[k]
    (fewer than N at the start — average what you have).
    """
    raise NotImplementedError("implement me from your Lecture 3 notes")


def depth_alarm(t, filtered, limit):
    """Return the TIME (from array t) at which `filtered` first exceeds
    `limit`, or None if it never does.
    """
    raise NotImplementedError("implement me — loop, condition, return early")


# ----------------------- self-check: do not edit below -----------------------
if __name__ == "__main__":
    rng = np.random.default_rng(3)
    t = np.arange(0, 20, 0.1)
    truth = np.where(t < 8, 1.0, 2.0)          # commanded dive at t = 8 s
    z = truth + rng.normal(0, 0.08, t.size)    # noisy sensor (Lecture 3's world)

    score = 0
    try:
        f10 = np.array(moving_average(z, 10))
        assert f10.shape == z.shape, "output must be same length as input"
        assert abs(f10[:50].mean() - 1.0) < 0.05, "pre-dive average should sit near 1 m"
        assert abs(f10[150:].mean() - 2.0) < 0.05, "post-dive average should sit near 2 m"
        assert np.std(f10[150:]) < np.std(z[150:]), "filtered should be smoother than raw"
        print("[OK ] moving_average behaves correctly")
        score += 1
    except NotImplementedError:
        print("[    ] moving_average not implemented yet")
    except AssertionError as e:
        print(f"[FAIL] moving_average: {e}")

    try:
        a10 = depth_alarm(t, np.array(moving_average(z, 10)), 1.5)
        a40 = depth_alarm(t, np.array(moving_average(z, 40)), 1.5)
        never = depth_alarm(t, np.array(moving_average(z, 10)), 5.0)
        assert a10 is not None and 8.0 <= a10 <= 9.5, f"N=10 alarm expected shortly after t=8, got {a10}"
        assert a40 is not None and a40 > a10, f"N=40 alarm must fire LATER than N=10 ({a40} vs {a10})"
        assert never is None, "a limit never exceeded must return None"
        print(f"[OK ] depth_alarm behaves correctly (N=10 fires at t={a10:.1f}s, N=40 at t={a40:.1f}s)")
        print(f"      <-- logbook question 1 is answered by those two numbers")
        score += 1
    except NotImplementedError:
        print("[    ] depth_alarm not implemented yet")
    except AssertionError as e:
        print(f"[FAIL] depth_alarm: {e}")

    print(f"\nLab 2 self-check: {score}/2 " + ("— submit it. ><(((\"> " if score == 2 else "— keep going."))
