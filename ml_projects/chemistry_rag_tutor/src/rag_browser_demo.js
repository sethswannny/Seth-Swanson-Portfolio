const COURSE_CHUNKS = [
  {
    source: "Chemistry 101 Syllabus",
    heading: "Required Materials",
    text: "Students need a scientific calculator, lab notebook, safety goggles, and a periodic table."
  },
  {
    source: "Chemistry 101 Syllabus",
    heading: "Late Work",
    text: "Homework may be submitted one class meeting late for partial credit. Lab reports lose credit after the due date unless an extension is approved before the deadline."
  },
  {
    source: "Chemistry 101 Syllabus",
    heading: "Retakes",
    text: "Students may retake one quiz per unit after completing the correction form and attending review time."
  },
  {
    source: "Chemistry 101 Syllabus",
    heading: "Unit 4 Assessment Window",
    text: "Unit 4 covers mole conversions, percent composition, empirical formulas, stoichiometry, limiting reactants, and percent yield."
  },
  {
    source: "Course Calendar",
    heading: "October",
    text: "October 11: Mole conversion practice quiz. October 16: Percent-yield lab. October 18: Unit 4 quiz. October 23: Unit 4 review day. October 25: Unit 4 test. October 30: Introduction to gas laws."
  },
  {
    source: "Unit 4 Study Guide",
    heading: "Learning Targets",
    text: "Convert between grams, moles, and particles. Use a balanced equation to compare reactants and products. Identify the limiting reactant. Calculate theoretical yield and percent yield."
  },
  {
    source: "Unit 4 Study Guide",
    heading: "Stoichiometry Process",
    text: "Balance the chemical equation. Convert the known quantity to moles. Use the balanced equation coefficients as the mole ratio. Convert the target substance into the requested unit. Check units and significant figures."
  },
  {
    source: "Unit 4 Study Guide",
    heading: "Limiting Reactants",
    text: "If amounts are given for two reactants, solve for the product amount from each reactant. The reactant that produces the smaller amount of product is the limiting reactant."
  },
  {
    source: "Unit 4 Study Guide",
    heading: "Percent Yield",
    text: "Percent yield equals actual yield divided by theoretical yield, then multiplied by 100."
  },
  {
    source: "Lab 4: Percent Yield",
    heading: "Before Lab",
    text: "Complete the pre-lab safety check. Wear goggles throughout the experiment. Tie back loose hair and secure loose clothing."
  },
  {
    source: "Lab 4: Percent Yield",
    heading: "Report Requirements",
    text: "The report requires a balanced reaction table, measured mass data, limiting-reactant calculation, theoretical yield, percent yield, and a short error-analysis paragraph."
  },
  {
    source: "Lab 4: Percent Yield",
    heading: "Due Date",
    text: "The lab report is due at the next class meeting after the lab."
  }
];

const STOP_WORDS = new Set(["the", "and", "for", "with", "that", "this", "what", "when", "how", "does", "from", "about", "into", "class"]);

function tokenize(text) {
  return (text.toLowerCase().match(/[a-z0-9]+/g) || []).filter((term) => term.length > 2 && !STOP_WORDS.has(term));
}

function retrieve(question) {
  const queryTerms = new Set(tokenize(question));

  return COURSE_CHUNKS.map((chunk) => {
    const chunkTerms = new Set(tokenize(`${chunk.source} ${chunk.heading} ${chunk.text}`));
    let score = 0;

    queryTerms.forEach((term) => {
      if (chunkTerms.has(term)) score += 1;
    });

    if (queryTerms.has("test") && chunk.source === "Course Calendar" && chunkTerms.has("test")) score += 4;
    if (queryTerms.has("quiz") && chunk.source === "Course Calendar" && chunkTerms.has("quiz")) score += 3;
    if ((queryTerms.has("lab") || queryTerms.has("due")) && chunk.source.includes("Lab 4")) score += 3;
    if ((queryTerms.has("stoichiometry") || queryTerms.has("moles") || queryTerms.has("reactants")) && chunk.source === "Unit 4 Study Guide") score += 3;
    if (queryTerms.has("grade") || queryTerms.has("current")) score -= 2;

    return { ...chunk, score };
  })
    .filter((chunk) => chunk.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 3);
}

function buildAnswer(question, sources) {
  const lower = question.toLowerCase();

  if (sources.length === 0 || lower.includes("current grade")) {
    return "I do not see that answer in the sample course documents. A real course assistant should avoid guessing here and direct the student to the teacher or gradebook.";
  }

  if (lower.includes("stoich") || lower.includes("mole ratio") || lower.includes("moles")) {
    return "Start by balancing the chemical equation. Convert the known amount to moles, use the balanced equation coefficients as the mole ratio, then convert the target substance into the requested unit. If two reactants are provided, calculate both possible product amounts and use the smaller result as the limiting-reactant answer.";
  }

  if (lower.includes("test") || lower.includes("quiz")) {
    return "The sample calendar lists the Unit 4 quiz on October 18, the review day on October 23, and the Unit 4 test on October 25. The Unit 4 material includes mole conversions, percent composition, empirical formulas, stoichiometry, limiting reactants, and percent yield.";
  }

  if (lower.includes("lab") || lower.includes("due")) {
    return "The percent-yield lab requires the pre-lab safety check, balanced reaction table, measured mass data, limiting-reactant calculation, theoretical yield, percent yield, and a short error-analysis paragraph. The lab report is due at the next class meeting after the lab.";
  }

  return `Here is the most relevant course information I found: ${sources[0].text}`;
}

function renderSources(sources) {
  if (!sources.length) return '<span class="source-chip warning">No matching source found</span>';

  return sources
    .map((source) => `<span class="source-chip">${escapeHTML(source.source)}: ${escapeHTML(source.heading)}</span>`)
    .join("");
}

function escapeHTML(text) {
  return text.replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;"
  })[character]);
}

function addMessage(messages, type, text, sources = []) {
  const article = document.createElement("article");
  article.className = `chat-message ${type}`;
  article.innerHTML = `
    <p>${escapeHTML(text)}</p>
    ${type === "assistant" ? `<div class="message-sources">${renderSources(sources)}</div>` : ""}
  `;
  messages.appendChild(article);
  messages.scrollTop = messages.scrollHeight;
}

function askQuestion(question, messages, input) {
  const trimmed = question.trim();
  if (!trimmed) return;

  addMessage(messages, "user", trimmed);
  const sources = retrieve(trimmed);
  addMessage(messages, "assistant", buildAnswer(trimmed, sources), sources);
  input.value = "";
}

const chat = document.querySelector("[data-rag-chat]");

if (chat) {
  const messages = chat.querySelector("[data-rag-messages]");
  const form = chat.querySelector("[data-rag-form]");
  const input = form.querySelector("input");
  const sampleButtons = document.querySelectorAll("[data-rag-sample]");

  addMessage(
    messages,
    "assistant",
    "Hi. I can answer from the sample Chemistry 101 syllabus, calendar, Unit 4 study guide, and percent-yield lab handout. Try asking about stoichiometry, the Unit 4 test, or lab requirements.",
    COURSE_CHUNKS.slice(0, 4)
  );

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    askQuestion(input.value, messages, input);
  });

  sampleButtons.forEach((button) => {
    button.addEventListener("click", () => {
      askQuestion(button.dataset.ragSample, messages, input);
      input.focus();
    });
  });
}
