"""Small lexical search engine; scores use term frequency and inverse document frequency."""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import re

def tokenize(text: str) -> list[str]:
    return re.findall(r"[^\W_]+", text.casefold(), flags=re.UNICODE)

def search(root: Path, query: str, limit: int = 5) -> list[dict]:
    if limit < 1:
        raise ValueError("limit must be positive")
    if not root.is_dir():
        raise ValueError("notes path must be a directory")
    terms = set(tokenize(query))
    if not terms:
        return []
    documents = []
    for path in sorted(root.rglob("*.md")):
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            continue
        text = path.read_text(encoding="utf-8")
        documents.append((path, text, Counter(tokenize(text))))
    frequencies = Counter(term for _, _, counts in documents for term in terms if term in counts)
    results = []
    for path, text, counts in documents:
        size = sum(counts.values()) or 1
        score = sum(counts[term] / size * (1 + math.log((1 + len(documents)) /
                    (1 + frequencies[term]))) for term in terms)
        if score:
            title = next((line.lstrip("# ").strip() for line in text.splitlines()
                          if line.startswith("# ")), path.stem)
            results.append({"path": path.relative_to(root).as_posix(), "title": title,
                            "score": round(score, 6), "excerpt": " ".join(text.split())[:160]})
    return sorted(results, key=lambda row: (-row["score"], row["path"]))[:limit]

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args(argv)
    try:
        print(json.dumps(search(args.directory, args.query, args.limit), ensure_ascii=False, indent=2))
    except (OSError, UnicodeError, ValueError) as exc:
        parser.exit(2, f"error: {exc}\n")
    return 0
