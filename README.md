# Seth Swanson Portfolio

Personal analytics and data science portfolio for Seth Swanson.

## Main Projects

- **MyOrdr**: Cross-platform iOS and Android social ordering app using Flutter, Supabase, Resend, Netlify, Cloudflare, and product analytics.
- **Buell Market Value Predictor**: Synthetic marketplace regression project that predicts used motorcycle listing prices and packages the full workflow with reports, charts, code, and a Streamlit app.
- **Synthetic REIT Portfolio Risk Model**: Portfolio-safe classification project that screens fictional REIT assets as healthy, watchlist, or at risk using financial, lease, tenant, and market signals.

## Structure

```text
assets/                 Portfolio images and resume
projects/               HTML case study pages
ml_projects/            Full machine learning project folders
index.html              Portfolio homepage
styles.css              Site styling
script.js               Small site interactions
```

## Local Preview

```bash
python3 -m http.server 4173
```

Then open:

```text
http://localhost:4173
```

The one-file reports in `ml_projects/*/dist/` can also be opened directly without a local server.

## Notes

The public ML datasets are synthetic by design. They do not use employer data,
private schemas, tenant names, API keys, or confidential business logic.
