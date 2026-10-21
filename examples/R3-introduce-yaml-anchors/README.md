# R3 — Introduce YAML Anchors

**Mechanism:** YAML anchors (`&name`) and aliases (`*name`), supported in GitHub Actions
workflows since September 2025.
**Scope:** duplication of *any YAML node* (mapping, sequence item, scalar) **inside a single file**.

## Smell
Three jobs repeat the same `env`, the same `services` block and the same first three steps.

## Refactoring
1. Put an anchor on the first occurrence of each repeated node (`&ci-env`, `&ci-services`, `&checkout`, ...).
2. Replace the later occurrences with aliases (`*ci-env`, ...).

## Preconditions / pitfalls
- Anchors are **file-local**: they cannot remove duplication across workflow files
  (use R1/R2 for that).
- An alias copies the node *as is*: no parameters. If one occurrence differs slightly,
  either keep it inline or use another mechanism.
- Merge keys (`<<: *anchor`, to extend a mapping) are **not documented** by GitHub; this
  example deliberately avoids them.
- Aliases are expanded when the workflow is parsed, so behaviour is strictly identical:
  this is the "purest" refactoring of the set (easy to verify by comparing the expanded YAML).

## Behaviour preserved
After alias expansion, `after/` is structurally equal to `before/` (checked by `examples/check.py`).
