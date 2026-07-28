# AGENTS.md

## Project overview
Single-page Python Cheat Sheet HTML app with bilingual support (VI/EN), dark/light theme toggle, and algorithm-focused highlights.

## File structure
- `python-cheatsheet.html` — the entire app: HTML, CSS, and JS in one self-contained file.

## How to work on this project
- Open `python-cheatsheet.html` directly in a browser. No build step, no dependencies.
- The JS holds all content in a `langData` object with two keys: `vi` and `en`. Every key must exist in both languages.
- CSS uses `[data-theme="dark"]` to override `:root` CSS custom properties. Never hardcode color values outside `:root` or `[data-theme="dark"]`.
- Sections are rendered dynamically via `renderAll()` using data from `langData`. To add a new section, add data to both `vi` and `en`, add a nav link with `data-section`, and add a `renderSection()` call in `renderAll()`.
- Language preference and theme preference are persisted in `localStorage`.

## Constraints
- Do NOT add external dependencies (no npm, no CDN). Everything must stay in the single HTML file.
- Keep the file self-contained — no `<link>`, no `<script src>`, no separate CSS/JS files.
- `highlight` blocks with the `algo` tag are for algorithm-relevant notes. Preserve the `.tag.algo` styling.
