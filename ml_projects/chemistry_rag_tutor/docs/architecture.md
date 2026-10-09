# Architecture Notes

## Document Types

- Syllabus: grading, test policy, retake policy, late-work policy, required materials.
- Course calendar: quiz dates, test dates, lab dates, unit windows.
- Unit notes: chemistry concepts, worked examples, formulas, vocabulary.
- Lab handouts: procedures, safety requirements, due dates, report sections.
- Study guides: test scope, practice problems, learning targets.

## Chunking Strategy

Chunk by semantic boundaries, not fixed length only.

- Keep date rows together in the course calendar.
- Keep lab procedure steps together with safety warnings.
- Keep worked stoichiometry examples together with their balanced equation.
- Add metadata for unit, document type, source title, date, and topic.

Example metadata:

```json
{
  "course": "Chemistry 101",
  "unit": "Unit 4",
  "document_type": "study_guide",
  "topic": "stoichiometry",
  "source_title": "Unit 4 Study Guide",
  "chunk_id": "unit4_study_guide_003"
}
```

## Retrieval Strategy

Use hybrid retrieval when possible:

- Vector similarity for flexible student wording.
- Keyword/date matching for exact logistics questions.
- Metadata filters for unit-specific or document-specific questions.

For example, "When is the stoichiometry test?" should retrieve from the course calendar and Unit 4 study guide, not only generic stoichiometry notes.

## Answer Prompt Requirements

The model should:

- Answer only from retrieved course context when the question is about course policy or dates.
- Cite the retrieved source titles.
- Separate course facts from chemistry explanation.
- Say when the course documents do not include the answer.
- Ask for missing values when a calculation is underspecified.

## Evaluation Set

Test categories:

- Date lookup: "When is the Unit 4 test?"
- Policy lookup: "Can I retake the quiz?"
- Lab workflow: "What do I turn in for Lab 4?"
- Content tutoring: "How do I do stoichiometry?"
- Calculation support: "If I have 5.0 g of H2, how much H2O can I make?"
- Missing context: "What is my current grade?"
