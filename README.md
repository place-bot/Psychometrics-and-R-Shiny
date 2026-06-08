# Psychometrics and R Shiny Notes

This repository contains the source for a MkDocs Material notes site covering psychometrics, CTT, IRT, CAT, and R Shiny.

## Website

Expected GitHub Pages URL:

https://place-bot.github.io/Psychometrics-and-R-Shiny/

As of 2026-06-08, that URL returns 404 from the public web. The repository has a `gh-pages` branch with old generated HTML, but GitHub Pages does not appear to be publicly serving it. This repair moves the maintainable source into `main` and adds a GitHub Pages Actions workflow.

After pushing `main`, set repository Pages to deploy from the `gh-pages` branch at `/` if it is not already enabled. The workflow in `.github/workflows/deploy-pages.yml` builds the MkDocs source from `main` and publishes the generated site to `gh-pages`.

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

## Maintenance Notes

- Keep source content on `main`; treat `gh-pages` or Pages artifacts as generated output.
- Run `mkdocs build --strict` before publishing changes.
- Add references when changing conceptual psychometrics content.
