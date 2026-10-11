# Xtract

**Search results you can trust, before your agent reads them.**

🎥 **Demo video (2 to 3 min):** https://youtu.be/Lup7Obs6EhY

Narration uses an earlier run (8.4c vs 25.1c); current numbers are in Results below.

---

## What we built

Xtract sits between an AI agent and web search. Before the agent reads a page, Xtract scores it: how useful it is likely to be for the task and what it costs to read. The agent only reads what helps and skips the rest. This results in an immense increase in efficiency while lowering the cost, with comparable or slightly better answers.

## Who it's for

**Teams building AI sales agents**: agents that research a company before writing an outreach email.

These agents run many searches per account and turn whatever they find into a personalized email. When a page is outdated, the email goes out with the wrong facts: a product that was shut down, an executive who left, a deal that never closed. An engineer at an AI sales-agent company told us how they catch this today:

> "Someone responding or human review. Hard to catch a fact you didn't know about before it arrived."

## The problem

- **Stale facts reach customers.** In our tests, agents pitched outdated news for **4 of 7 companies** when starting from an outdated alert. A better prompt or a bigger model did not fix it.
- **Agents read everything.** In our test setup, each search returns 10 pages and a naive agent reads all of them, even though only a few end up in the answer. Every useless page costs tokens.
- **Good sources are increasingly locked.** Paywalls, bot checks and Cloudflare's default blocking of AI crawlers mean the agent often can't read the pages that matter most, and doesn't know it until it tries.

## How it works

1. The agent sends its query. Xtract fetches results from a web search API (we use [Keenable](https://keenable.ai)).
2. For each result, Xtract scores **usefulness** for the task and attaches a **price**.
3. The agent receives a ranked list and only reads the pages worth reading.
4. Scores are stored and **reused**: when the next agent hits the same page, the work is already done. Every task makes the system better and cheaper.

Search APIs today never learn which results an agent actually used. Google learned from human clicks, but agents don't click. Xtract captures that signal.

### Technical notes

- **One scoring function.** Usefulness is a weighted sum of five signals: embedding similarity between the query and the page's title and snippet, a cheap model check ("does this snippet answer the query?"), the search engine's own rank, and how often this page and its domain were cited when agents read them before. It is all in [`usefulness.py`](usefulness.py).
- **Price follows usefulness.** `price = floor + rate × usefulness`, so a more useful page never costs less. Prices are simulated.
- **Duplicates lose value.** Once the agent buys a page, any remaining page that states the same answer loses 35% of its usefulness, and its price drops with it.
- **Freshness.** One model call per result set finds pages whose news a later page in the same results replaces or reverses. Those pages lose half their usefulness, and the agent is told the later event in one line.
- **The buyer agent** buys pages in order of usefulness per cent, within a budget, and stops when the best remaining page is not worth reading.
- **The usage loop.** After each run, pages the agent cited move up and pages it bought but did not use move down.
- **Honest accounting.** Every token we spend on scoring is counted against our own savings. Every search and model response is cached to disk, so runs are repeatable and the demo works offline.
- **Evals.** `python3 run_evals.py` runs 18 checks and writes [`eval_report.md`](eval_report.md); 16 pass today. The two that fail are reported there, not hidden.

## Results so far

Measured on 6 held-out documentation tasks, counting both reading and scoring tokens:

| | **Tokens** | **Cost\*** |
| :- | :- | :- |
| Naive agent (reads all 10 pages) | 18,829 | 26.7¢ |
| Xtract | 20,819 (6,138 reading + 14,682 scoring) | 9.9¢ |
| A second agent reusing Xtract's scores | saves 12,691 tokens vs. naive | - |

\*Page prices are simulated, so the cost column shows what happens **when pages cost money**. On a single query, tokens are roughly even today. The real savings come from reuse: a page is scored once and every later agent benefits.

Sales research on 15 companies: Xtract read 3.1 pages per query instead of 10 and cost 10.3¢ instead of 26.6¢ per query, with comparable answers (11 of 15 reflected the company's latest news, against 10 of 15 for the naive agent). Freshness detection: 4 of 4 replaced stories caught, 0 false alarms.

## Run it

You need Python 3 (built and tested on 3.14), an OpenAI API key and a [Keenable](https://keenable.ai) API key. There are no packages to install.

**1. Set up your keys**

```bash
cp .env.example .env
```

Then open `.env` and fill in `OPENAI_API_KEY` and `KEENABLE_API_KEY`.

**2. Run the demo**

```bash
python3 demo.py --live                  # the sales demo (Windsurf); about 20 seconds
python3 demo.py --company "Airbnb"      # any company you type, live, 90 second limit
python3 demo.py --docs --live           # the coding-docs demo; several minutes the first time
```

Each command builds `demo.html` and opens it in your browser. Press **Space** (or the button) to start. Add `--pace 8` for pauses between beats.

Search and model responses are cached in `cache/` as they arrive. The cache holds third-party page text, so it is not in this repository: on a fresh clone the first run of each command calls Keenable and OpenAI. After that you can drop `--live`, and `python3 demo.py` and `python3 demo.py --docs` run offline from the cache. Without `--live` and without a cache they stop with an "OFFLINE=1 and no cached response" error.

**3. Run the evals**

```bash
python3 run_evals.py
```

This runs all 18 checks, prints the table and saves it to `eval_report.md`. The first run makes a few thousand cached API calls and takes a while; reruns take seconds.

Page prices are simulated. No real money moves, apart from your own API usage.

## Market

AI sales agents are one of the fastest-growing categories in AI, and every email they send starts with web research. Just imagine if you would use the internet right now but google will not rank your answers and the most important ones are locked behind a paywall. This is the stage in which the extremely fast growing AI Agent industry is in right now:

| **Signal** | **Number** | **Source** |
| :- | :- | :- |
| AI SDR market | **$4.1B (2025) → $15.0B (2030)**, 29.5% CAGR | [MarketsandMarkets, Aug 2025](https://www.prnewswire.com/news-releases/ai-sdr-market-15-01-billion-by-2030--marketsandmarkets-302520473.html) |
| AI agents market overall | **$7.8B (2025) → $52.6B (2030)**, 46.3% CAGR | [MarketsandMarkets, Aug 2026](https://www.globenewswire.com/news-release/2026/08/20/3348589/0/en/ai-agents-market-surges-to-52-62-billion-at-a-cagr-46-3-by-2030-report-by-marketsandmarkets.html) |
| Sales intelligence market | **$4.0B (2025) → $8.7B (2033)** | [Grand View Research](https://www.grandviewresearch.com/industry-analysis/sales-intelligence-market) |
| Sellers already using AI agents | **54%**, and nearly 9 in 10 plan to by 2027 (n = 4,050) | [Salesforce State of Sales 2026](https://www.salesforce.com/news/stories/state-of-sales-report-announcement-2026/) |
| B2B data goes stale | ~**2.1% per month, ~22.5% per year** | [Apollo, citing Only-B2B](https://www.apollo.io/insights/whats-the-average-rate-of-data-decay-in-a-b2b-contact-database-and-how-do-i-address-it) |
| Investors are betting on this layer | Clay valued at **$7.1B**, Exa at **$2.2B**, Parallel at **$2B** | [Clay](https://www.eneralabs.com/blog/clay-115m-series-d-agentic-gtm-2026/), [Exa](https://www.caproasia.com/2026/05/25/united-states-ai-search-infrastructure-startup-exa-labs-raises-250-million-series-c-funding-at-2-2-billion-valuation-raised-85-million-in-series-b-funding-in-2025-september-founded-in-2021-by-wil/), [Parallel](https://www.finsmes.com/2026/04/parallel-web-systems-raises-100m-in-series-b-funding-at-2-billion-valuation.html) |

Every AI sales agent researches before it writes, so every one of them needs the layer we're building: deciding which pages are worth reading and which facts are still true.

## Value creation

For a sales-agent team, a single wrong fact costs far more than the search that found it. A personalized email that references outdated news doesn't just fail to get a reply. It tells the prospect the sender didn't do their homework. Xtract creates value in four ways:

1. **Revenue protection.** Fewer stale facts reach prospects, so fewer emails are wasted and more turn into conversations. In our tests, agents pitched outdated news for 4 of 7 companies when starting from an outdated alert.
2. **Lower research cost.** The agent only reads, and pays for, the pages that help.
3. **Access to locked sources.** As more of the web charges AI agents, Xtract will show which pages are worth paying for and which are blocked, before the agent tries.
4. **Shared learning.** Every page scored once benefits every customer after it. The more agents use Xtract, the more valuable each answer becomes.

## Business model

- **Customers pay per account researched.** The price tracks the work their agent does, so cost grows only when their pipeline grows.
- **We take a small cut of every page bought through Xtract.** Most of the payment goes to the page's author, so we earn more as more of the web becomes paid content for agents.
- **Our costs fall as we grow.** A page is scored once and reused for every customer after that. In our tests, a second agent reusing Xtract's scores needed **67% fewer tokens** than an agent reading every page itself. Each new customer makes every query cheaper for us to serve, so margins widen with scale.

## What's next

- **Automatic stale-fact detection.** With perfect "outdated" flags, stale pitches drop from 4 of 7 companies to 2 of 7. Our first detector caught 4 of 4 replaced stories with 0 false alarms. Next we test it on live sales research.
- **Paywall and bot-block detection.** The agent will know whether it can read a page before it tries. Not built yet.
- Pilots with sales-agent teams using their real research queries.
- Lower scoring cost so Xtract beats a naive agent on tokens even on a single query.

## Team

- **Usman Ayobami**: engineering. Search & backend, founder of Core Extract.
- **Simon Kley**: business. Pricing, customers, go-to-market. UC Berkeley Haas.

Built at the Innovation Intelligence Hackathon, Oct 2026.
