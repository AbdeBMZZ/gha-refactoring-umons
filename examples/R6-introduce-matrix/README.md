# R6 — Introduce Matrix Strategy

**Mechanism:** `strategy.matrix` (job-level parametrisation).
**Scope:** several jobs of the same workflow that differ only by a few values.

## Smell
Nine jobs, one per (OS, Node version) pair, with identical steps.

## Refactoring
1. Identify the values that vary between the jobs (`runs-on`, `node-version`).
2. Replace the jobs by one job with a matrix over these values.
3. Set `fail-fast: false` to keep the original semantics (independent jobs).
4. Use `include:` / `exclude:` when the set of combinations is not a full cartesian product.

## Preconditions / pitfalls
- Job ids change (`test-ubuntu-node18` → `test (ubuntu-latest, 18)`): any `needs:`
  on a single old job, and any **required status check** in branch protection,
  must be updated. This is the main behaviour difference.
- The default `fail-fast: true` would *change* behaviour (one failure cancels the others).
- Matrices are limited to 256 jobs per workflow run.

## Note
Not strictly a "reuse" mechanism in the sense of R1–R5, but it removes duplication of the same kind
and is the most common refactoring in practice, so it belongs in the catalogue.
