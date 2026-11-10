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

## Push Authentication

- Git reaches GitHub through `gh auth git-credential`, so the push uses the
  token of the effective `gh` profile. Agent sessions may set `GH_CONFIG_DIR` to
  a scoped agent profile, for example `~/.config/gh-cicd-agent`.
- The CiCd-agent token covers only Hexalith.Builds and Hexalith.CiCd. Every
  other repository rejects its push with HTTP 403 ("Permission to
  Hexalith/<repo>.git denied"). That is by design, not a broken credential.
- Before diagnosing a 403, check the effective `GH_CONFIG_DIR`, whether
  `GH_TOKEN` or `GITHUB_TOKEN` is set (names only, never values), and
  `gh auth status`. An API `admin: true` describes the account, not the token.
  Do not retry the same push or ask for new tokens first.
- When the user explicitly asks for a push in an interactive session and the
  agent profile does not cover the repository, use the maintainer profile for
  that single command only:

  ```bash
  GH_CONFIG_DIR="$HOME/.config/gh" git push origin <branch>
  ```

- Never change the default profile or run `gh auth setup-git`. Never give
  unattended sessions, such as BMAD Loop runs, the maintainer profile. Never
  print credentials or credential-file contents.
- A maintainer push to a protected `main` may print "Bypassed rule violations"
  on stderr. Report that line to the user.

## Submodules

- Initialize or update only submodules declared under `references/` in the root
  repository `.gitmodules` file.
- Never initialize nested submodules inside root-declared submodules.
- Never use `git submodule update --init --recursive` or `--remote`.
- If nested submodules are initialized accidentally, deinitialize them before
  continuing.
- A request to commit a superproject includes committing and pushing all
  changes in every submodule declared in its root `.gitmodules`. Inspect
  each submodule for staged, unstaged, and untracked changes and existing
  unpushed commits, including work that predates the current task.
- Commit content changes inside each owning submodule, following its
  repository guidance and commitlint policy, and push all pending commits
  before creating the superproject commit. Do not create empty commits in
  unchanged submodules.
- Verify that every submodule commit to be recorded is available on its
  remote, then commit the updated submodule pointers in the superproject
  separately from the submodule content commits.
- If a submodule commit, push, or remote verification fails, report the
  exact command and blocker and stop before creating the superproject
  commit. Never record a submodule commit that has not been pushed.


## Commit Workflow

All commits **must** follow
[Conventional Commits Specification](https://raw.githubusercontent.com/conventional-commits/conventionalcommits.org/refs/heads/master/content/v1.0.0/index.md) because
semantic-release uses commit history to determine version bumps and changelogs.

Write the commit message to a temporary file and validate it with commitlint
before creating the commit.

