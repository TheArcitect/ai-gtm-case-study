# AI GTM Case-Study Generator

Turn before/after GTM metrics + screenshots into a polished one-page case study (Markdown CLI).

[![CI](https://github.com/TheArcitect/ai-gtm-case-study/actions/workflows/ci.yml/badge.svg)](https://github.com/TheArcitect/ai-gtm-case-study/actions) [![Release](https://img.shields.io/github/v/release/TheArcitect/ai-gtm-case-study?display_name=tag)](https://github.com/TheArcitect/ai-gtm-case-study/releases) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Stars](https://img.shields.io/github/stars/TheArcitect/ai-gtm-case-study)](https://github.com/TheArcitect/ai-gtm-case-study/stargazers)

![Quick demo](assets/demo.gif)  
_30-second demo: init a sample case YAML, then generate a polished Markdown case study._

**⭐ Star this repo if it helps you ship proof faster.**

---

### Why this exists

- **Faster proof for GTM/sales enablement** — skip the manual copy-paste loop
- **Consistent storytelling** — one template, repeatable results
- **Generates evidence from YAML** — before/after metrics + screenshot refs in one source

---

### Install (pipx)

```bash
pipx install git+https://github.com/TheArcitect/ai-gtm-case-study.git
gtm-casegen --help
```

### Quickstart

```bash
gtm-casegen init --dir examples
gtm-casegen generate --input examples/case.yaml --out out/
```

---

### Sample Output

Here's a short excerpt from a typical generated `out/case-study.md`:

```markdown
# AI-Accelerated Pipeline Lift

**Timeframe:** Q2 2025  
**Customer:** B2B SaaS scale-up, North America

## Results
- 32% increase in qualified meetings per rep/week
- Ramp time reduced from 28 → 19 days
- Qualified rate improved from 22% → 29%
```

---

### Detailed module README

For developer docs, installation from source, and architecture notes, see [`gtm-casegen/README.md`](gtm-casegen/README.md).

---

### Roadmap

- [ ] **PDF export** — one-click polished PDF for sales decks
- [ ] **Multiple templates** — choose story structure (problem/solution, before/after, etc.)
- [ ] **CSV input** — bulk-generate case studies from a spreadsheet
- [ ] **Charts** — auto-generate metric visualizations from YAML deltas

---

### Contributing

Issues and PRs are welcome! Please run the test suite and linter locally before submitting:

```bash
cd gtm-casegen
uv sync --all-extras --dev
uv run ruff check .
uv run pytest -q
```

---

### License

MIT License. See [`LICENSE`](LICENSE).

---

### Repo assets & social preview

- Replace `assets/demo.gif` with a real 30–60s recording of `init → generate`.
- Set `assets/social-preview.png` in **GitHub → Settings → Social preview**.

---

<!-- SEO keywords: ai, go-to-market, case study generator, cli, python, typer, jinja2, uv -->
