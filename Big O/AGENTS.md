# AGENTS.md

## Overview
Single-file static Big-O cheatsheet using Tailwind CSS CDN. No build step, no package manager, no tests.

## Running locally
Open `big-o-cheatsheet.html` directly in a browser. No server needed — it's a fully offline HTML file (Tailwind is loaded from CDN, the data and chart are inline).

## Editing
- All content is in `big-o-cheatsheet.html` (~458 lines).
- Tailwind config is inline in a `<script>` tag (dark mode via `class` strategy).
- i18n strings live in the `i18n` and `glossaryI18n` globals, supporting `en` and `vi`. The lang button in the header toggles between them.
- The complexity chart is rendered with an inline `<script>` using a Canvas-based line chart (log-scale Y axis). It plots all 7 functions: O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ), O(n!). Colors match the CSS `.legend-dot` classes exactly. The chart redraws on window resize and theme toggle.
- Data tables (data structures, sorting algorithms) are generated from the `i18n.en.dsa` / `i18n.en.sorter` arrays plus inline JS data objects.

## Conventions
- No external JS dependencies beyond Tailwind CDN.
- All JS is vanilla, in a single `<script>` tag at the end of `<body>` (after all HTML content).
- Dark mode toggle: class-based, toggled via `dark` class on `<html>` (see `darkMode: 'class'` in Tailwind config). Theme and lang are restored from `localStorage` in an IIFE that runs immediately at body-end.
- No `onclick` attributes — both buttons use `addEventListener` inside the init IIFE.
- Language state is tracked via `document.documentElement.dataset.lang` (no global variable).
