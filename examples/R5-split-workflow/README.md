# R5 — Split Workflow (chain with `workflow_run`)

**Mechanism:** a regular workflow triggered by the completion of another one
(`on: workflow_run`).
**Scope:** a long workflow mixing two concerns (here: CI and documentation deployment).

## Smell
`ci-and-docs.yml` is a long sequential chain `build → test → build-docs → deploy-docs`.
The two last jobs belong to a different concern (publishing), need different permissions
and only run on `main`, but they live in the CI file.

## Refactoring
1. Cut the job graph after `test`. Jobs before the cut stay in `ci.yml`.
2. Move the remaining jobs to `docs.yml`, triggered by `workflow_run` on `CI`, `types: [completed]`.
3. Translate the cross-cut `needs: test` into
   `if: github.event.workflow_run.conclusion == 'success'`, and move the old job-level
   condition (push on main) into the trigger filter + `if:`.
4. Check out `github.event.workflow_run.head_sha`, so that the docs are built from the tested commit.

## Preconditions / pitfalls (this refactoring is *not* strictly behaviour-preserving)
- `workflow_run` always uses the version of `docs.yml` on the **default branch**.
- Artifacts of the first run are not available with a plain `download-artifact`; they need
  `run-id: ${{ github.event.workflow_run.id }}` and `github-token`. (Not needed here.)
- The triggered workflow runs with the repository's secrets and a write-capable token **even
  when the first run came from a fork PR** — a known security risk; never check out and execute
  PR code in it without care.
- Chaining depth of `workflow_run` is limited (see GitHub docs).
- The two runs appear separately in the UI and are billed separately.

## Benefit
Each file has one responsibility, CI no longer needs to know about Pages,
and the docs workflow can also be re-run on its own.
