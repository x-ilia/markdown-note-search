# markdown-note-search

Offline ranked search for Markdown notes with Unicode tokenization and JSON output.

A small, dependency-free Python project designed to be useful on its own and easy
for coding agents to understand. Runs locally; no API keys or services required.

## Quick start

Requires Python 3.11 or newer. From the repository root:

```sh
python -m note_search examples/notes "python"
python -m unittest discover -s tests -v
```

Optional installation in a virtual environment:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
markdown-note-search --help
```

## Behavior and limits

Recursively reads `.md` files as UTF-8, skips symlinked files and paths outside the root,
and ranks matches by normalized term frequency with smoothed inverse document frequency.
This is lexical search, without embeddings, stemming or fuzzy matching. Ties sort by path.
JSON output contains path, title, score and excerpt. Exit codes: 0 success (including
no matches), 2 invalid input or unreadable files. The index is rebuilt in memory per query.

## Layout

- `note_search/core.py`: public functions and command-line interface.
- `tests/`: unit and command-line regression tests.
- `examples/`: small, synthetic inputs safe to share publicly.
- `AGENTS.md`: orientation and working conventions for coding agents.
- `docs/architecture.md`: data flow and extension points.

## Possible next steps

- Add persistent indexing.
- Add phrase matching.
- Add configurable ignore patterns.

These are suggestions for future work, not implemented features.

## Development

Tests use the Python standard library. The CI workflow runs them on Python 3.11
and 3.12. Keep changes focused and add regression tests for behavior changes.
The project is intentionally small; it does not claim production readiness.

## License

MIT. See [LICENSE](LICENSE).
