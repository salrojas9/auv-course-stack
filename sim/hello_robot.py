"""
hello_robot.py — the tier-one kinematic fake AUV.
Intro to Autonomous Robotics (AUV) · Part I, Lecture 4 / Lab 3

This is the smallest honest robot simulator: state + dynamics + integration,
plus a noisy depth sensor and a CSV log. It has NO hydrodynamics — that is
tier two (Stonefish, Week 5). It runs identically on every laptop on Earth.

Run:      python3 hello_robot.py           (runs the demo mission, saves plot + log)
Extend:   see LAB 3 markers below.
"""
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")           # headless-safe: works in the container
import matplotlib.pyplot as plt

DT = 0.1                        # tick length [s]  -> 10 Hz
RNG = np.random.default_rng(7)


# ----------------------------------------------------------------------------
# 1) STATE + DYNAMICS + INTEGRATION  (the three ingredients of any simulator)
# ----------------------------------------------------------------------------
def step(state, cmd, dt=DT, disturbance=0.03):
    """Advance one tick.
    state = [x, y, yaw, depth]         (m, m, rad, m)
    cmd   = [u surge m/s, r yaw rad/s, w heave m/s]
    disturbance: constant sink rate — the vehicle is slightly heavy. Real
    water always pushes; a simulator that never fights you teaches lies.
    """
    x, y, yaw, d = state
    u, r, w = cmd
    return np.array([
        x + u * np.cos(yaw) * dt,
        y + u * np.sin(yaw) * dt,
        yaw + r * dt,
        max(0.0, d + (w + disturbance) * dt),   # surface is a hard floor
    ])


# ----------------------------------------------------------------------------
# 2) SENSING — the only depth the robot is ALLOWED to see (never the state!)
# ----------------------------------------------------------------------------
def read_depth(state, sigma=0.05):
    """Pressure-derived depth: truth + gaussian noise (sigma in meters)."""
    return state[3] + RNG.normal(0.0, sigma)


# ----------------------------------------------------------------------------
# 3) CONTROL — from Lecture 4
# ----------------------------------------------------------------------------
def depth_controller(measured_depth, target, Kp=0.8, w_max=0.4):
    """P control on depth, saturated to the vehicle's real heave authority.
    clamp() is your Week 0 function, all grown up."""
    w = Kp * (target - measured_depth)
    return max(-w_max, min(w_max, w))          # clamp(w, -w_max, w_max)


# ----------------------------------------------------------------------------
# MISSION RUNNER — a list of (name, duration, command-maker) phases.
# A command-maker is a function of the latest measured depth -> [u, r, w].
# (Peek ahead: in Week 12 this list becomes a behavior tree.)
# ----------------------------------------------------------------------------
def run_mission(phases, state=None):
    state = np.array([0., 0., 0., 0.]) if state is None else state
    rows = [("t", "x", "y", "yaw", "depth_true", "depth_meas", "u", "r", "w")]
    t = 0.0
    for name, duration, make_cmd in phases:
        for _ in range(int(duration / DT)):
            z = read_depth(state)
            cmd = make_cmd(z)
            state = step(state, cmd)
            t += DT
            rows.append((round(t, 2), *np.round(state, 4), round(z, 4), *cmd))
            # ---- LAB 3 (2): SAFETY ABORT goes here --------------------------
            # if battery_v < V_MIN or state[3] > D_MAX: switch to a 'surface'
            # phase and break out. Log WHY in the CSV.
            # -----------------------------------------------------------------
    with open("mission_log.csv", "w", newline="") as f:
        csv.writer(f).writerows(rows)
    return np.array([r[1:6] for r in rows[1:]], dtype=float), rows


# ---- LAB 3 (1): BATTERY ----------------------------------------------------
# Add battery_v to the loop: start at 16.8 V and drain proportionally to
# |u| + |r| + |w| each tick. Sensible constants are yours to choose & justify.
# ----------------------------------------------------------------------------


def demo():
    target = 1.2
    phases = [
        ("dive+hold", 20.0, lambda z: [0.5, 0.0, depth_controller(z, target)]),
        ("turn",       6.0, lambda z: [0.4, 0.30, depth_controller(z, target)]),
        ("cruise",    10.0, lambda z: [0.6, 0.0, depth_controller(z, target)]),
        # LAB 3 (3): add a P-controlled 'surface' phase (target = 0.0)
    ]
    traj, rows = run_mission(phases)

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.2))
    a1.plot(traj[:, 0], traj[:, 1]); a1.set_aspect("equal")
    a1.set_xlabel("x [m]"); a1.set_ylabel("y [m]"); a1.set_title("top view")
    tt = np.arange(traj.shape[0]) * DT
    a2.plot(tt, traj[:, 3], label="true depth")
    a2.plot(tt, traj[:, 4], ".", ms=2, alpha=0.4, label="measured")
    a2.axhline(target, ls="--", c="k", lw=1)
    a2.set_xlabel("time [s]"); a2.set_ylabel("depth [m]"); a2.legend()
    a2.set_title("depth hold under disturbance")
    fig.tight_layout(); fig.savefig("mission.png", dpi=140)
    print("Mission complete. Wrote mission_log.csv and mission.png")
    print(f"Final state: x={traj[-1,0]:.2f}  y={traj[-1,1]:.2f}  "
          f"depth={traj[-1,3]:.2f} (target {target})")


if __name__ == "__main__":
    demo()
