# R2 — Extract Reusable Workflow

**Mechanism:** reusable workflow (`on: workflow_call`), called with `jobs.<id>.uses`.
**Scope:** job-level duplication across workflows (same repo, or other repos if the workflow is shared).

## Smell
`deploy-staging.yml` and `deploy-production.yml` contain an identical job; only the
environment name, image tag, replica count, health URL and deploy secret differ.

## Refactoring
1. Move the job into `_deploy.yml` triggered by `workflow_call`.
2. Turn every differing value into a typed `input`, and the differing secret into a `secrets:` entry.
3. Replace each original job by a caller job (`uses:` + `with:` + `secrets:`).

## Why not a composite action?
The duplicated unit is a **whole job**: it carries `runs-on`, `environment` and `permissions`,
which a composite action cannot express.

## Preconditions / pitfalls
- A caller job using `uses:` cannot have `steps:` or `runs-on:`.
- Secrets are not inherited by default: pass them explicitly (or `secrets: inherit`).
- The caller's `permissions` bound the permissions available to the called workflow.
- Limits on nesting depth and on the number of called workflows apply (see GitHub docs).

## Behaviour preserved
Same triggers, same environments (so same protection rules), same image tags and commands.
