# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

The two files below are the source of truth for scope and work order, and should be read before doing any work here:

- [`_docs/plan.md`](_docs/plan.md) — the full MVP scope: domain model, rules, and an explicit "Out of Scope" list.
- [`_docs/tasks.md`](_docs/tasks.md) — the implementation backlog, ordered so each task is small and independently handoff-able.

Task 1 ("empty project with a passing test") is done: a Django project (`config`) and a first app (`chores`) are scaffolded, with a trivial passing test. From here, work proceeds task-by-task through `_docs/tasks.md`; keep the Commands section below current as tooling is added.

### Local environment notes

- Python 3.14 and Django 6.x are used, but this dev container only ships Python 3.12 by default — Python 3.14 was installed via the deadsnakes PPA (`sudo add-apt-repository ppa:deadsnakes/ppa`) into `.venv`.
- PostgreSQL 18 runs via Docker (`docker-compose.yml`, official `postgres:18` image) rather than a system install — the container is the intended way to get Postgres here, not `apt install postgresql`.
- The `postgres:18` image changed its default data directory convention from `/var/lib/postgresql/data` to `/var/lib/postgresql`; `docker-compose.yml` already accounts for this — don't "fix" the volume path back to `.../data`, it will fail to start.

## Chosen stack

Decided stack for this project (do not propose alternatives unless asked):

- **Backend**: Django, Python 3.14
- **Database**: PostgreSQL 18
- **Frontend**: server-rendered Django templates + HTMX for interactivity (checking/unchecking tasks) — no JS framework, no separate SPA, no DRF/JSON API layer
- **Weekly rotation generation**: lazy, on-request generation — a view-layer check computes whether the current week's `WeekAssignment` exists and creates it if not (keyed by week so it can never be generated twice). There is intentionally **no Celery, no cron, and no scheduler** in this project — do not introduce one.

## Domain model (from the plan)

The core model chain is: **Apartment → Areas → Tasks → Weekly Assignment → Completion Tracking**.

- The household (3 roommates, 3 areas, each area's tasks, and the rotation order) is **fixed and immutable** for the MVP — there is no setup UI and no add/remove/edit flow for any of it. Any task that seems to need one is out of scope; see `_docs/plan.md` § 13.
- A **week** is the unit of both assignment and history: each week, every roommate is assigned exactly one area (following a fixed rotation order), and that area's tasks get fresh, independent completion records. Completion state belongs to a specific week's assignment — it is never shared or carried across weeks.
- Completion tracking is deliberately minimal: only a completed/incomplete boolean per task. **Do not add** timestamps, "who completed it," fairness scoring, or task carry-over — these are explicitly out of scope (`_docs/plan.md` § 13) even though they're common features to reach for.
- There is no authentication and no per-roommate identity in the UI — the dashboard is the same shared, transparent view for everyone. Don't gate anything behind a login.

## Commands

```
# Start PostgreSQL 18 (via Docker)
docker compose up -d db

# One-time env setup
python3.14 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env   # adjust if needed; loaded automatically by config/settings.py

# Apply migrations
.venv/bin/python manage.py migrate

# Run the dev server
.venv/bin/python manage.py runserver

# Run the full test suite (either works; both are configured)
.venv/bin/python manage.py test
.venv/bin/python -m pytest

# Run a single test
.venv/bin/python manage.py test chores.tests.HomeViewTests.test_home_returns_200
.venv/bin/python -m pytest chores/tests.py::HomeViewTests::test_home_returns_200
```

There is no lint/format tooling configured yet. If one is added (e.g. ruff, black), document its commands here.

## Git / GitHub workflow

Do not commit, push, create branches, open pull requests, or merge anything unless the user explicitly asks for it in that session. Finishing a task's code is not, by itself, permission to commit it — wait to be asked, even if a previous task in this same project was committed/pushed/PR'd without much friction.

## Things to be careful about

- Treat `_docs/plan.md` § 13 ("Explicitly Out of Scope") as a hard boundary, not a suggestion — it lists several features (auth, notifications, manual assignment edits, fairness stats, task deadlines, etc.) that are easy to accidentally reach for out of habit but are intentionally excluded from the MVP.
- The household configuration (roommates, areas, tasks, rotation order) must stay immutable in code paths reachable by the app — there is no UI or endpoint that edits it after seeding.
- "A week is never generated twice" is a correctness requirement, not just a performance nicety (`_docs/plan.md` § 12) — any change to the lazy-generation logic must preserve that guarantee.
- When picking up a backlog task from `_docs/tasks.md`, its own description is meant to be self-sufficient — but it assumes the models/utilities from earlier-numbered tasks already exist in the codebase, since the backlog is ordered as a dependency chain even though each task is written to stand alone.
