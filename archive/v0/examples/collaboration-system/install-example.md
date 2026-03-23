# Install Example

This guide explains how to copy `project-template/` into a new repository with minimal manual work.

## Option A: Manual Copy

From the target repository root:

```sh
cp -R ./examples/collaboration-system/project-template/. /path/to/target-repo/
```

Then immediately:

1. add `.ai/` to `.gitignore` if it is not already ignored
2. open `bootstrap-checklist.md`
3. rewrite the placeholder lane files under `.ai/active-lane/`
4. update `docs/ai-relay.md`, `docs/ai-collaboration.md`, and `docs/ai-workbench.md` for the real project

## Option B: Use The Copy Script

From the target repository root:

```sh
./examples/collaboration-system/copy-into-new-repo.sh /path/to/target-repo
```

The script only copies the template skeleton.
It does not rewrite project-specific facts for you.

## What To Check Immediately After Copying

- `.ai/` is ignored and remains local-only
- `docs/ai-relay.md` points to the intended active lane path
- placeholder branch / commit / blocker text has been replaced
- `AGENTS.md` matches the new repository's AI conventions
- the first supervisory pass can run without manually re-explaining the system

## Safe Follow-Up Order

1. run through `bootstrap-checklist.md`
2. decide the first active lane
3. rewrite placeholder lane docs
4. run the first supervisory pass
5. run the first bounded execution pass
