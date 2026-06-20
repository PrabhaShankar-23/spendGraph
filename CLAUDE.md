# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

This is **Spendly**, a Flask expense-tracker app being built incrementally as a step-by-step course/tutorial project. Most functionality is intentionally unimplemented — comments in the code mark what is expected to be built ("Step N") rather than indicating a bug:

- `database/db.py` currently has no implementation; it documents the contract it must fulfill: `get_db()` (SQLite connection with `row_factory` and foreign keys enabled), `init_db()` (create tables with `CREATE TABLE IF NOT EXISTS`), `seed_db()` (insert sample dev data).
- `app.py` has working routes for `/`, `/register`, `/login` (render templates only, no form handling yet) and placeholder routes for `/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete` that just return plaintext stubs.
- `static/js/main.js` is an empty placeholder for future client-side behavior.

When asked to "implement Step N" or add a feature, check which pieces above are still stubs before assuming infrastructure (DB, auth, sessions) already exists — it likely needs to be built first.

## Commands

```bash
# activate the existing venv (Python 3.13)
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# run the dev server (debug mode, port 5001)
python app.py

# run tests (pytest + pytest-flask are installed; no tests/ directory exists yet)
pytest
```

There is no build step, linter, or formatter configured in this repo.

## Architecture

- **Flask app factory-less app**: `app.py` creates a single module-level `Flask(__name__)` instance and defines routes directly — there's no blueprint structure yet.
- **Database**: SQLite, accessed via a future `database/db.py` module (see contract above). The DB file (`expense_tracker.db`) is gitignored and created at runtime, not committed.
- **Templates**: Jinja2 templates in `templates/` all extend `base.html`, which defines the shared navbar/footer shell and exposes `{% block title %}`, `{% block head %}`, `{% block content %}`, `{% block scripts %}`. Auth forms (`login.html`, `register.html`) post directly to `/login` and `/register` and render a flash-style `{% if error %}` block passed from the view.
- **Styling**: Single stylesheet `static/css/style.css` using CSS custom properties defined in `:root` (e.g. `--ink`, `--accent`, `--paper`) for the color palette, plus `--font-display` (DM Serif Display) and `--font-body` (DM Sans) loaded from Google Fonts in `base.html`. No CSS framework or build pipeline — edit the file directly.
- **Currency/locale**: amounts are displayed in ₹ (INR) per the existing landing-page copy — keep this convention when adding expense displays.
