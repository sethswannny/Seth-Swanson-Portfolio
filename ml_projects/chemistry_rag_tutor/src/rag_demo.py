"""Tiny local RAG-style demo for the Chemistry Class RAG Tutor project.

This script keeps the portfolio project runnable without external API keys. It
uses simple keyword retrieval over the sample course materials, then returns a
grounded answer template with source citations.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MATERIALS_DIR = PROJECT_ROOT / "sample_course_materials"


@dataclass
class Chunk:
    source: str
    heading: str
    text: str


def tokenize(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if len(token) > 2 and token not in {"the", "and", "for", "with", "that", "this"}
    }


def load_chunks() -> list[Chunk]:
    chunks: list[Chunk] = []

    for path in sorted(MATERIALS_DIR.glob("*.md")):
        heading = path.stem.replace("_", " ").title()
        lines: list[str] = []

        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("#"):
                if lines:
                    chunks.append(Chunk(path.name, heading, "\n".join(lines).strip()))
                    lines = []
                heading = line.lstrip("#").strip()
            elif line.strip():
                lines.append(line.strip())

        if lines:
            chunks.append(Chunk(path.name, heading, "\n".join(lines).strip()))

    return chunks


def retrieve(question: str, chunks: list[Chunk], limit: int = 3) -> list[Chunk]:
    query_terms = tokenize(question)
    scored: list[tuple[int, Chunk]] = []

    for chunk in chunks:
        chunk_terms = tokenize(f"{chunk.heading} {chunk.text}")
        score = len(query_terms & chunk_terms)

        if "test" in query_terms and "calendar" in chunk.source and "test" in chunk_terms:
            score += 2
        if "quiz" in query_terms and "calendar" in chunk.source and "quiz" in chunk_terms:
            score += 2
        if "lab" in query_terms and "lab" in chunk.source:
            score += 2
        if {"stoichiometry", "moles", "reactants"} & query_terms and "study_guide" in chunk.source:
            score += 2

        if score:
            scored.append((score, chunk))

    return [chunk for _, chunk in sorted(scored, key=lambda item: item[0], reverse=True)[:limit]]


def answer(question: str, chunks: list[Chunk]) -> str:
    question_lower = question.lower()
    sources = retrieve(question, chunks)
    cited_sources = ", ".join(f"{chunk.source} - {chunk.heading}" for chunk in sources)

    if "stoich" in question_lower or "mole ratio" in question_lower:
        response = (
            "To do stoichiometry, first balance the equation. Convert the known amount to moles, "
            "use the balanced equation coefficients as the mole ratio, then convert the target "
            "substance into the requested unit. If two reactants are provided, calculate the "
            "product from each one and use the smaller amount as the limiting-reactant result."
        )
    elif "test" in question_lower or "quiz" in question_lower:
        response = (
            "The sample course calendar lists the Unit 4 quiz on October 18, review day on "
            "October 23, and the Unit 4 test on October 25."
        )
    elif "lab" in question_lower or "due" in question_lower:
        response = (
            "The percent-yield lab requires the pre-lab safety check, measured mass data, "
            "limiting-reactant calculation, theoretical yield, percent yield, and an error-analysis "
            "paragraph. The sample handout says the report is due at the next class meeting."
        )
    else:
        response = (
            "I found related course material, but the sample documents do not contain a precise "
            "answer. A production version should say this clearly and ask the student or teacher "
            "for the missing context."
        )

    return f"{response}\n\nSources: {cited_sources or 'No relevant sample source found.'}"


def main() -> None:
    question = " ".join(sys.argv[1:]).strip() or "How do I do stoichiometry?"
    chunks = load_chunks()
    print(answer(question, chunks))


if __name__ == "__main__":
    main()
