# Architecture

`python -m note_search` delegates to `core.main`. Argument parsing and filesystem
access live at the boundary; the exported core functions own the behavior.
Results are plain Python data structures that can be serialized as JSON.

## Design decisions

- Standard library only: easy to run in a fresh agent environment.
- Explicit validation: bad input should fail predictably rather than be coerced.
- Stable ordering: examples and tests stay reproducible across machines.
- Read-only processing: input files are never modified.

## Extension strategy

Add a focused core function, test it using synthetic fixtures, then expose it via
the CLI. Keep the documented default behavior compatible where possible.

## Scope

Recursively reads `.md` files as UTF-8, skips symlinked files and paths outside the root,
and ranks matches by normalized term frequency with smoothed inverse document frequency.
This is lexical search, without embeddings, stemming or fuzzy matching. Ties sort by path.
JSON output contains path, title, score and excerpt. Exit codes: 0 success (including
no matches), 2 invalid input or unreadable files. The index is rebuilt in memory per query.
