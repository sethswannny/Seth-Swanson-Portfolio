# Chemistry Class RAG Tutor

Portfolio project concept for a retrieval-augmented chemistry course assistant.

The assistant is designed to answer two kinds of student questions:

- Course logistics: test dates, quiz coverage, lab due dates, late-work rules, and required materials.
- Chemistry tutoring: stoichiometry steps, mole conversions, limiting reactants, percent yield, and lab calculations.

## Product Goal

Students should be able to ask natural-language questions about their chemistry class and receive answers grounded in course files rather than a generic model response.

Example questions:

- "When is the Unit 4 test?"
- "What is due for the percent-yield lab?"
- "How do I do stoichiometry?"
- "What topics are on the next quiz?"
- "Can you walk me through limiting reactants?"

## RAG Design

1. Ingest syllabus, calendar, lab handouts, study guides, and unit notes.
2. Split documents into chunks using headings, dates, problem types, and lab sections.
3. Store chunk text, metadata, and embeddings in a vector database.
4. Retrieve the most relevant chunks for each student question.
5. Generate an answer with citations and clear uncertainty when the source material does not include the answer.

## Recommended Stack

- Frontend: Next.js or simple HTML prototype
- Backend: Python FastAPI or Supabase Edge Functions
- Embeddings: OpenAI embeddings
- Vector store: Supabase pgvector, Pinecone, or Chroma
- Document parsing: pypdf, python-docx, markdown
- Evaluation: curated question set with expected source chunks

## Local Demo

Run the no-API-key prototype from the project folder:

```bash
python3 src/rag_demo.py "How do I do stoichiometry?"
python3 src/rag_demo.py "When is the Unit 4 test?"
python3 src/rag_demo.py "What is due for the lab?"
```

This is intentionally lightweight: it demonstrates ingestion, chunking, retrieval, and grounded answer formatting without requiring API keys or a hosted vector database.

## Guardrails

- Cite course sources for every logistics answer.
- Do not invent test dates, due dates, grading rules, or teacher policies.
- For chemistry tutoring, explain the process step by step.
- For graded homework, guide the student without simply doing the full assignment when the prompt asks for learning support.
- Ask a follow-up question when a calculation is missing units, a balanced equation, or a known quantity.

## Portfolio Value

This project demonstrates applied AI engineering: retrieval design, document chunking, prompt guardrails, answer evaluation, source citation, and a practical education use case.
