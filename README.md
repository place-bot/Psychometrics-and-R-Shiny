# Psychometrics and R Shiny Notes

This repository contains the source for a MkDocs Material notes site covering psychometrics, CTT, IRT, CAT, CDM, and R Shiny.

## Website

GitHub Pages URL:

https://place-bot.github.io/Psychometrics-and-R-Shiny/

The workflow in `.github/workflows/deploy-pages.yml` builds the MkDocs source whenever `main`
is updated and publishes the generated site to the `gh-pages` branch. GitHub Pages should use
that branch at `/` as its publishing source.

## Local Development

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
mkdocs serve
```

Then open `http://127.0.0.1:8000/Psychometrics-and-R-Shiny/`.

## Repository Structure

- `docs/`: source Markdown pages and image assets.
- `mkdocs.yml`: site configuration and navigation.
- `.github/workflows/deploy-pages.yml`: GitHub Pages deployment workflow.
- `RECOVERED_SOURCE.md`: record of pages recovered from the old `gh-pages` deployment output.
- `tools/recover_mkdocs_source.py`: one-off recovery helper used to reconstruct source pages from deployed HTML.
- `tools/convert_bobcat_tex.py`: one-off converter for the BOBCAT Chinese LaTeX notes; it omits the
  exercise chapter and requires `--force` before overwriting edited Markdown.

## Maintenance Notes

- Keep source content on `main`; treat `gh-pages` or Pages artifacts as generated output.
- Run `mkdocs build --strict` before publishing changes.
- Add references when changing conceptual psychometrics content.
