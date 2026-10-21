# R4 — Extract Workflow Template

**Mechanism:** organization workflow template (`workflow-templates/` folder of the
organization's `.github` repository + a `.properties.json` metadata file).
Since September 2025 the `.github` repository may also be internal or private.
**Scope:** duplication of whole workflow files **across repositories of an organization**.

## Smell
`repo-a` and `repo-b` (two services of the same organization) contain the same CI workflow,
which was copy-pasted by hand when the second repository was created.

## Refactoring
1. Create `workflow-templates/java-maven-ci.yml` in the organization's `.github` repository,
   replacing the hard-coded default branch by `$default-branch`.
2. Add `java-maven-ci.properties.json` (name, description, categories, `filePatterns`).
3. New repositories create their CI from the template ("Actions → New workflow").

## Important difference with R1–R3
A template is a **creation-time** reuse mechanism: the template is *copied* into the
repository. `after/repo-a` and `after/repo-b` therefore still contain the full workflow —
the duplication is not removed, it is *standardised* and made traceable.
Later changes to the template are **not** propagated. When propagation is needed,
the template should itself call a reusable workflow (R2): the copied file then stays a thin caller.

## Behaviour preserved
The instantiated workflow in each repository is identical to the original one
(modulo the `$default-branch` placeholder, resolved to `main`).
