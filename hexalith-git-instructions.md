# Hexalith Git Instructions

These rules apply before creating Git commits in a Hexalith repository and
before pushing parent-repository commits that bump root-declared `references/`
submodule pointers. This file also covers branch, submodule, staging, and push
checks where they affect commit safety.

## Repository Boundaries

- Run Git commands from the repository that owns the change. If the change is
  inside a submodule, `cd` into that submodule first.
- Inspect the current repository before changing it:

  ```bash
  git status --short --branch
  git remote -v
  git log --oneline --decorate --max-count=8
  ```

- Do not revert, overwrite, or clean changes you did not make unless the user
  explicitly asks for that operation.
- Avoid destructive commands such as `git reset --hard`, `git checkout --`, or
  `git clean` unless the user clearly requested them.

## Branches

- Work on the **`main`** branch by default. Only create or switch to another
  branch when the task genuinely requires it.
- Use branch names that describe the change:
  - `feat/<description>` for features and enhancements.
  - `fix/<description>` for bug fixes.
  - `docs/<description>` for documentation changes.
- Before pushing, fetch and inspect divergence. Prefer rebasing a local change
  onto the current remote branch when the remote has advanced and the local work
  is a simple linear continuation.

## Submodules

- Initialize or update only submodules declared under `references/` in the root
  repository `.gitmodules` file.
- Never initialize nested submodules inside root-declared submodules.
- Never use `git submodule update --init --recursive` or `--remote`.
- If nested submodules are initialized accidentally, deinitialize them before
  continuing.
- Commit submodule content changes inside the submodule first. Then commit the
  parent repository submodule pointer update separately.


## Commit Workflow

All commits **must** follow
[Conventional Commits Specification](https://raw.githubusercontent.com/conventional-commits/conventionalcommits.org/refs/heads/master/content/v1.0.0/index.md) because
semantic-release uses commit history to determine version bumps and changelogs.

Write the commit message to a temporary file and validate it with commitlint
before creating the commit.

