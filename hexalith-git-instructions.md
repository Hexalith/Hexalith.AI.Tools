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

## Staging

Inspect the working tree and stage only the intended files:

```bash
git status --short
git add <paths>
git diff --cached --name-status
git diff --cached --check
```

If `git diff --cached --check` reports whitespace or conflict-marker problems,
fix them before committing.

## Commit Workflow

All commits **must** follow
[Conventional Commits](https://www.conventionalcommits.org/) because
semantic-release uses commit history to determine version bumps and changelogs.

Write the commit message to a temporary file and validate it with commitlint
before creating the commit:

```bash
COMMIT_MSG="$(mktemp)"
printf '%s\n\n%s\n' \
  'docs: explain local commitlint workflow' \
  'Add guidance for validating Hexalith commit messages before committing.' \
  > "$COMMIT_MSG"

npx commitlint --edit "$COMMIT_MSG" --verbose
git commit -F "$COMMIT_MSG"
npx commitlint --last --verbose && rm "$COMMIT_MSG"
```

Replace the sample subject and body with the message for the actual change. If
repository Node dependencies are not installed, run `npm ci` first so the
repository-pinned `@commitlint/cli` and config are used. If the repository
being committed has no `package.json` or commitlint config, run the
`npx commitlint --edit "$COMMIT_MSG" --verbose` validation from the nearest
parent Hexalith repository that does have them; `mktemp` returns an absolute
message file path that is safe to pass across repositories.

If commitlint fails, edit the message and rerun `npx commitlint --edit
"$COMMIT_MSG" --verbose` until it passes. Never use `git commit --no-verify` to
bypass commit hooks.

If the post-commit `npx commitlint --last --verbose` check fails, amend the
message and rerun the check before continuing:

```bash
git commit --amend -F "$COMMIT_MSG"
npx commitlint --last --verbose && rm "$COMMIT_MSG"
```

Before pushing a branch or opening a pull request, validate the full branch
commit range that CI will inspect:

```bash
git fetch origin main --quiet
npx commitlint --from "$(git merge-base origin/main HEAD)" --to HEAD --verbose
```

## Message Rules

Use this subject format:

```text
<type>[optional scope][!]: <description>
```

| Type | Description | Version bump |
| ---- | ----------- | ------------ |
| `feat` | New feature | Minor |
| `fix` | Bug fix | Patch |
| `perf` | Performance improvement | Patch |
| `docs` | Documentation only | None |
| `refactor` | Code change, no feature/fix | None |
| `test` | Add/modify tests | None |
| `build` / `ci` / `chore` / `style` | Tooling, build, formatting | None |

- The colon must be followed by a space: `feat: add projection replay`, not
  `feat:add projection replay` or `feat:Add projection replay`.
- The description starts lowercase, uses imperative mood, and has no trailing
  period.
- Keep the subject under about 50 characters. Wrap body text at 72 characters.
- Choose the type by release impact: `feat` for new user-visible capability,
  `fix` or `perf` for patch releases, `docs` for documentation, `test` for
  tests, `refactor` for behavior-preserving code changes, and `build`, `ci`,
  `chore`, or `style` for maintenance.
- Do not use `feat` for pure refactoring, test-only work, dependency bumps, or
  submodule pointer updates.
- Breaking changes use `BREAKING CHANGE:` in the footer or `!` after the type
  (`feat!:`), which triggers a major version bump.
- Every commit needs a `type:` prefix. A subject that starts with a plain-English
  verb (`Update ...`, `Add ...`, `Fix ...`, `Bump ...`) is not conventional: it
  does not match the Conventional Commit header pattern and fails with
  `type-empty` / `subject-empty`.

Valid examples:

```text
docs: add commitlint workflow instructions
test(integration): add round-trip counter coverage
refactor(testing): reorganize integration test fixtures
chore(deps): bump Hexalith.Memories submodule to 27bebfa
fix(server): prevent duplicate event sequence numbers
feat!: rename EventEnvelope.StreamId to AggregateId
```

Invalid examples:

```text
feat:Refactor integration tests and add round-trip counter aggregate
Update subproject reference for Hexalith.Memories
Add commit instructions
```

## Submodule And Dependency Commits

Git's default submodule message, `Update subproject reference ...`, is not a
valid Conventional Commit. Rewrite submodule, dependency, merge, revert,
formatting, and configuration commits explicitly:

```text
chore(deps): bump Hexalith.AI.Tools submodule
chore(deps): bump Fluent UI Blazor to 5.x
revert: restore previous event envelope naming
ci: update release package validation
```

When a change requires both a submodule commit and a parent-repository pointer
update, validate and commit each repository's message from that repository root.

## Pushes

- Before pushing, verify the branch state:

  ```bash
  git status --short --branch
  git log --oneline --decorate --left-right --graph @{u}...HEAD
  ```

- If there is no upstream branch, push with `git push -u origin <branch>`.
- If the branch is behind its upstream, fetch and integrate the remote work
  before pushing.
- Do not force-push unless the user explicitly asks for it and the branch is
  known to be safe to rewrite.
