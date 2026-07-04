"""Build a standalone HTML project dossier.

The output is a single HTML file with embedded CSS, charts, tables, and source
snippets. It can be opened directly from the filesystem with no local server.
"""

from __future__ import annotations

import base64
import html
import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = PROJECT_ROOT / "reports"
FIGURE_DIR = REPORT_DIR / "figures"
DIST_DIR = PROJECT_ROOT / "dist"
OUTPUT_PATH = DIST_DIR / "buell_market_value_one_file.html"


def money(value: float) -> str:
    return f"${value:,.0f}"


def pct(value: float) -> str:
    return f"{value:+.1%}"


def image_data_uri(path: Path) -> str:
    mime = "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def table_html(data: pd.DataFrame, columns: list[str] | None = None) -> str:
    if columns:
        data = data[columns]
    return data.to_html(index=False, border=0, classes="data-table", escape=True)


def source_block(path: Path, title: str) -> str:
    code = html.escape(path.read_text(encoding="utf-8"))
    return f"""
      <details class="source-block">
        <summary>{html.escape(title)}</summary>
        <pre><code>{code}</code></pre>
      </details>
    """


def main() -> None:
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    metrics = pd.read_csv(REPORT_DIR / "model_metrics.csv")
    importance = pd.read_csv(REPORT_DIR / "feature_importance.csv").head(10)
    deals = pd.read_csv(REPORT_DIR / "top_deal_examples.csv").head(8)
    metadata = json.loads((PROJECT_ROOT / "models" / "model_metadata.json").read_text(encoding="utf-8"))

    metrics_display = metrics.copy()
    metrics_display["mae"] = metrics_display["mae"].map(money)
    metrics_display["rmse"] = metrics_display["rmse"].map(money)
    metrics_display["r2"] = metrics_display["r2"].map(lambda value: f"{value:.4f}")
    metrics_display["mape"] = metrics_display["mape"].map(lambda value: f"{value:.1%}")
    metrics_display.columns = ["Model", "MAE", "RMSE", "R2", "MAPE"]

    importance_display = importance.copy()
    importance_display["importance"] = importance_display["importance"].map(lambda value: f"{value:,.0f}")
    importance_display["std"] = importance_display["std"].map(lambda value: f"{value:,.0f}")
    importance_display.columns = ["Feature", "Importance", "Std."]

    deals_display = deals.copy()
    deals_display["listing_price"] = deals_display["listing_price"].map(money)
    deals_display["predicted_price"] = deals_display["predicted_price"].map(money)
    deals_display["predicted_delta_pct"] = deals_display["predicted_delta_pct"].map(pct)
    deals_display.columns = [
        "Make",
        "Model",
        "Year",
        "Mileage",
        "Condition",
        "Region",
        "Asking Price",
        "Predicted Price",
        "Delta",
        "Deal Flag",
    ]

    figures = {
        "actual": image_data_uri(FIGURE_DIR / "actual_vs_predicted.png"),
        "residuals": image_data_uri(FIGURE_DIR / "residuals.png"),
        "importance": image_data_uri(FIGURE_DIR / "feature_importance.png"),
        "price": image_data_uri(FIGURE_DIR / "price_by_model.png"),
    }

    html_doc = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Buell Market Value Predictor - One File Report</title>
    <style>
      :root {{
        --ink: #14201f;
        --muted: #566664;
        --paper: #fffdfa;
        --surface: #f7f4ee;
        --line: #d9ded6;
        --teal: #0b6b68;
        --teal-dark: #074f4d;
        --coral: #d86446;
        --mustard: #d5a93f;
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        color: var(--ink);
        background: var(--surface);
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        line-height: 1.62;
      }}
      header, section, footer {{ padding: 56px clamp(18px, 5vw, 72px); }}
      header {{
        min-height: 76vh;
        display: grid;
        align-items: center;
        background:
          linear-gradient(90deg, rgba(247,244,238,.98), rgba(247,244,238,.9)),
          radial-gradient(circle at 82% 22%, rgba(11,107,104,.18), transparent 34%);
      }}
      .report-nav {{
        padding-bottom: 0;
      }}
      .back-link {{
        display: inline-flex;
        min-height: 40px;
        align-items: center;
        gap: 8px;
        padding: 8px 13px;
        color: var(--teal-dark);
        border: 1px solid rgba(11,107,104,.2);
        border-radius: 8px;
        background: rgba(255,255,255,.82);
        box-shadow: 0 10px 28px rgba(20,32,31,.08);
        font-weight: 850;
        text-decoration: none;
      }}
      .back-link::before {{
        content: "<";
        font-weight: 900;
      }}
      .eyebrow {{
        margin: 0 0 12px;
        color: var(--coral);
        font-size: .78rem;
        font-weight: 850;
        letter-spacing: 0;
        text-transform: uppercase;
      }}
      h1, h2, h3, p {{ margin-top: 0; }}
      h1 {{
        max-width: 980px;
        margin-bottom: 22px;
        font-size: clamp(3rem, 8vw, 7rem);
        line-height: .94;
        letter-spacing: 0;
      }}
      h2 {{
        max-width: 900px;
        font-size: clamp(2rem, 4vw, 4rem);
        line-height: 1.03;
      }}
      h3 {{ margin-bottom: 8px; font-size: 1.18rem; }}
      .lead {{
        max-width: 820px;
        color: var(--muted);
        font-size: clamp(1.08rem, 2vw, 1.35rem);
      }}
      .meta {{
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 24px;
      }}
      .meta span {{
        padding: 7px 10px;
        color: var(--teal-dark);
        border-radius: 8px;
        background: rgba(11,107,104,.1);
        font-size: .82rem;
        font-weight: 800;
      }}
      .stat-grid, .two-col, .visual-grid, .workflow {{
        display: grid;
        gap: 18px;
      }}
      .stat-grid {{ grid-template-columns: repeat(3, minmax(0, 1fr)); margin-top: 36px; }}
      .two-col, .visual-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .workflow {{ grid-template-columns: repeat(5, minmax(0, 1fr)); }}
      .card, .step, .table-wrap, figure, .source-block {{
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--paper);
        box-shadow: 0 18px 54px rgba(20,32,31,.08);
      }}
      .card, .step {{ padding: 24px; }}
      .card p, .step p, figcaption {{ color: var(--muted); }}
      .stat strong {{
        display: block;
        color: var(--teal-dark);
        font-size: clamp(2rem, 4vw, 3.5rem);
        line-height: 1;
      }}
      .step b {{
        display: grid;
        width: 36px;
        height: 36px;
        place-items: center;
        margin-bottom: 16px;
        color: white;
        border-radius: 8px;
        background: var(--teal);
      }}
      .band {{ background: var(--paper); }}
      .table-wrap {{ overflow-x: auto; }}
      .data-table {{
        width: 100%;
        min-width: 760px;
        border-collapse: collapse;
      }}
      .data-table th, .data-table td {{
        padding: 13px 15px;
        text-align: left;
        border-bottom: 1px solid var(--line);
        vertical-align: top;
      }}
      .data-table th {{
        color: var(--teal-dark);
        font-size: .78rem;
        text-transform: uppercase;
      }}
      figure {{ margin: 0; padding: 14px; }}
      figure img {{
        width: 100%;
        display: block;
        border-radius: 6px;
      }}
      figcaption {{ margin: 10px 4px 2px; font-size: .92rem; }}
      code, pre {{
        font-family: "SFMono-Regular", Consolas, monospace;
        font-size: .86rem;
      }}
      .source-block {{ margin-bottom: 14px; overflow: hidden; }}
      .source-block summary {{
        padding: 16px 18px;
        color: var(--teal-dark);
        font-weight: 850;
        cursor: pointer;
      }}
      .source-block pre {{
        max-height: 460px;
        margin: 0;
        padding: 18px;
        overflow: auto;
        color: #f6fbfa;
        background: #14201f;
      }}
      footer {{ color: var(--muted); border-top: 1px solid var(--line); }}
      @media (max-width: 900px) {{
        .stat-grid, .two-col, .visual-grid, .workflow {{ grid-template-columns: 1fr; }}
        header {{ min-height: auto; }}
      }}
    </style>
  </head>
  <body>
    <section class="report-nav">
      <a class="back-link" href="../../../index.html#projects">Back to portfolio</a>
    </section>
    <header>
      <div>
        <p class="eyebrow">One-File Portfolio Dossier</p>
        <h1>Buell Market Value Predictor</h1>
        <p class="lead">
          A self-contained machine learning case study: synthetic marketplace data, feature engineering,
          model comparison, explainability, visuals, sample deal outputs, and source snippets in one HTML file.
        </p>
        <div class="meta">
          <span>Python</span>
          <span>scikit-learn</span>
          <span>Regression</span>
          <span>Streamlit companion app</span>
          <span>Opens without a server</span>
        </div>
        <div class="stat-grid">
          <div class="card stat"><strong>{metadata["rows"]:,}</strong><p>synthetic marketplace listings</p></div>
          <div class="card stat"><strong>{money(float(metrics.iloc[0]["mae"]))}</strong><p>best model test-set MAE</p></div>
          <div class="card stat"><strong>{float(metrics.iloc[0]["r2"]):.3f}</strong><p>best model test-set R-squared</p></div>
        </div>
      </div>
    </header>

    <section>
      <p class="eyebrow">Project Story</p>
      <div class="two-col">
        <article class="card">
          <h2>Why this project exists</h2>
          <p>
            I wanted a public data science project that felt more like a real pricing decision than a canned
            tutorial dataset. Buell works well because the market mixes current performance bikes, older enthusiast
            models, scarcity, condition, mileage, and comparison-shopping against similar motorcycles.
          </p>
        </article>
        <article class="card">
          <h2>What it is not</h2>
          <p>
            This is not an official appraisal tool and it does not use scraped private listings. The dataset is
            synthetic by design, so the project demonstrates modeling workflow and product thinking rather than
            claiming real-world valuation authority.
          </p>
        </article>
      </div>
    </section>

    <section class="band">
      <p class="eyebrow">Workflow</p>
      <h2>The full pipeline in one view.</h2>
      <div class="workflow">
        <div class="step"><b>1</b><h3>Frame</h3><p>Estimate fair listing price and translate the gap into deal labels.</p></div>
        <div class="step"><b>2</b><h3>Generate</h3><p>Create a safe synthetic marketplace with Buell and comparable bikes.</p></div>
        <div class="step"><b>3</b><h3>Engineer</h3><p>Build model-ready fields like age, power-to-weight, listing quality, and condition.</p></div>
        <div class="step"><b>4</b><h3>Train</h3><p>Compare ridge regression, random forest, and histogram gradient boosting.</p></div>
        <div class="step"><b>5</b><h3>Explain</h3><p>Save metrics, feature importance, charts, examples, and a decision app.</p></div>
      </div>
    </section>

    <section>
      <p class="eyebrow">Model Results</p>
      <h2>Model comparison and selected winner.</h2>
      <div class="table-wrap">{table_html(metrics_display)}</div>
    </section>

    <section class="band">
      <p class="eyebrow">Visual Evidence</p>
      <h2>Charts generated by the training pipeline.</h2>
      <div class="visual-grid">
        <figure><img src="{figures["actual"]}" alt="Actual versus predicted price"><figcaption>Actual vs. predicted listing prices.</figcaption></figure>
        <figure><img src="{figures["residuals"]}" alt="Residual plot"><figcaption>Residuals by predicted listing price.</figcaption></figure>
        <figure><img src="{figures["importance"]}" alt="Feature importance"><figcaption>Permutation feature importance.</figcaption></figure>
        <figure><img src="{figures["price"]}" alt="Price by model"><figcaption>Synthetic price distribution by motorcycle model.</figcaption></figure>
      </div>
    </section>

    <section>
      <div class="two-col">
        <div>
          <p class="eyebrow">Explainability</p>
          <h2>Top model drivers.</h2>
          <div class="table-wrap">{table_html(importance_display)}</div>
        </div>
        <div>
          <p class="eyebrow">Decision Output</p>
          <h2>Example listings flagged as strong deals.</h2>
          <div class="table-wrap">{table_html(deals_display)}</div>
        </div>
      </div>
    </section>

    <section class="band">
      <p class="eyebrow">Source Snippets</p>
      <h2>The core code is included here too.</h2>
      {source_block(PROJECT_ROOT / "src" / "generate_synthetic_data.py", "Data generation script")}
      {source_block(PROJECT_ROOT / "src" / "train_model.py", "Model training script")}
      {source_block(PROJECT_ROOT / "app.py", "Streamlit app")}
    </section>

    <section>
      <p class="eyebrow">How To Reproduce</p>
      <h2>Run the full project locally.</h2>
      <div class="source-block" open>
        <summary>Commands</summary>
        <pre><code>python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python src/generate_synthetic_data.py
python src/train_model.py
python src/build_one_file_report.py
streamlit run app.py</code></pre>
      </div>
    </section>

    <footer>
      <p>Generated from the Buell Market Value Predictor project. This file is self-contained and can be opened without a webhost.</p>
    </footer>
  </body>
</html>
"""

    OUTPUT_PATH.write_text(html_doc, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
