# R1 — Extract Composite Action

**Mechanism:** composite action (`runs.using: composite`)
**Scope:** step-level duplication, within one repository (or across repositories if the action is published).

## Smell
The same sequence of steps (`setup-node` + `npm ci`) is copy-pasted in three jobs of `ci.yml`.
Changing the Node version or the install flags requires editing three places.

## Refactoring
1. Move the duplicated step sequence into `.github/actions/setup-node-project/action.yml`.
2. Turn the varying value (`node-version`) into an action input with a default.
3. Replace each occurrence with `uses: ./.github/actions/setup-node-project`.

## Preconditions / pitfalls
- `run:` steps in a composite action **must** declare `shell:`.
- A local action can only be used *after* `actions/checkout`, so the checkout step stays in each job.
- Composite actions cannot declare `runs-on`, `services` or job-level `if`/`needs`: only steps are extracted.
- Secrets are not accessible implicitly; they must be passed as inputs.

## Behaviour preserved
Same jobs, same dependency graph (`build` needs `lint`, `test`), same commands, same artifacts.
