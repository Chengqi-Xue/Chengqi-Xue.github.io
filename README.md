# Chengqi Xue — personal website

Bilingual (English / 中文) static site, hosted on GitHub Pages.

- `index.html` — home page (research, publications, patents, about)
- `projects/*.html` — one page per project
- `assets/` — stylesheet, script, images, compressed videos, CV and reports
- `sitegen/` — the Python scripts that generate the HTML (`python3 build_home.py && python3 build_projects.py` from inside `sitegen/`, with the output path pointing at the repo root)

Language is toggled with the button in the header and remembered in `localStorage`.
