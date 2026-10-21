# Refactoring GitHub Actions for Reuse

Master's thesis — Abdellah Boumaiza, UMONS, 2026–2027.
Supervisor: Prof. Tom Mens · Co-supervisor: Aref Talebzadeh Bardsiri.

## Repository layout

```
thesis/                 LaTeX sources (UMONS template), bibliography in references.bib
examples/               Ground-truth exemplars of reuse refactorings (before/after)
  R1-extract-composite-action/
  R2-extract-reusable-workflow/
  R3-introduce-yaml-anchors/
  R4-extract-workflow-template/
  check.py              Automatic equivalence checks (R3, R4)
.github/workflows/
  build-thesis.yml      Compiles the PDF; publishes it on the `pdf` branch
  check-examples.yml    actionlint + check.py on all exemplars
```

Each exemplar folder contains a `README.md` (smell, steps, preconditions, what is preserved),
a `before/` and an `after/` folder laid out as real repositories.

Exemplars are added one by one (R1, R2, …).

## Latest PDF

Built automatically on every change to `thesis/` or `examples/` on `main`
(or manually: *Actions → Build thesis PDF → Run workflow*):
**[`thesis.pdf` on the `pdf` branch](../../blob/pdf/thesis.pdf)**.
PRs get the PDF as a downloadable workflow artifact.

## Build locally

```bash
cd thesis && latexmk -pdf main.tex
python3 examples/check.py
```
