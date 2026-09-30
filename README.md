# Intro to Autonomous Robotics — AUV · Student Stack

This is everything you run. Lecture notes and Week 0 lessons come from Canvas.

## One-time setup (Lecture 2, together in class)
1. Install Docker Desktop (Mac/Windows) or Docker Engine (Linux) — Canvas has
   the per-OS walkthrough.
2. Install VS Code + the "Dev Containers" extension.
3. Open this folder in VS Code → click **"Reopen in Container"** → wait for the
   first build.
4. In the VS Code terminal:  `python3 scripts/verify_setup.py`
   A swimming fish = you're done. Screenshot it — that's Lab 0.

## What's here
- `.devcontainer/` — the course environment (identical for every student)
- `notebooks/`     — lecture follow-alongs; replace each `NotImplementedError`
                     with your solution from the handout, then run the cell
- `lab2/`          — Lab 2 starter (`filter_alarm.py`): implement, run it to
                     self-grade, submit on Canvas
- `lab3/`          — Lab 3 starter (`mission_capstone.py`): battery, safety
                     abort, full mission — run from the repo root to self-grade
- `sim/`           — `hello_robot.py`, the fake AUV (read it; Lab 3 imports it)
- `scripts/`       — the environment check + the Week 0 treasure hunt
                     (`bash scripts/setup_hunt.sh`, then hunt, then
                      `bash scripts/check_hunt.sh`)

## The homework loop (every assignment, forever)
git pull → edit → git status → git add → git commit -m "why" → git push
