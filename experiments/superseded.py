"""Experiment, Step A: is there headroom when news is SUPERSEDED?

An agent asked for a sales angle "based on their latest news" may find the old good-news story and miss
the newer story that cancels it. Not part of the evals. Cases come from superseded-news-cases.md.

    python3 experiments/superseded.py          Step A: query "<company> news"  -> superseded_results.md
    python3 experiments/superseded.py alert    Step B: a signal alert names the OLD event and the agent
                                               researches it                    -> superseded_alert_results.md
    python3 experiments/superseded.py alert prompt   Step B + one sentence added to the agent's prompt
    python3 experiments/superseded.py alert strong   Step B on a stronger chat model (STRONG_MODEL)

The keyword lists below are drafts by the coding agent (regexes, matched on lower-cased text).
CORRECT = the answer reflects the newer event. WRONG = it pitches the old event and not the newer one.
OTHER = neither keyword set matched: read the answer.
"""
import re
import sys

sys.path.insert(0, ".")
import agents
import clients

TASK = "Write a one-paragraph sales outreach angle for {name} based on their latest news."
QUERY = "{name} news"
ALERT_TASK = "We got an alert: {alert} Write a one-paragraph outreach angle for {name}."
PROMPT_FIX = " Before writing, check whether newer news contradicts the alert."
STRONG_MODEL = "gpt-4o"
ALERT = {  # case number: (the old event in one line, the search query an agent would build from it)
    1: ("Humane has put its Ai Pin on sale.", "Humane Ai Pin launch"),
    2: ("Builder.ai has named a new CEO and announced a new chapter for the company.", "Builder.ai new CEO"),
    3: ("OpenAI has agreed to buy Windsurf for about $3 billion.", "OpenAI Windsurf acquisition"),
    4: ("Figure AI raised $675M and announced a collaboration with OpenAI.", "Figure AI OpenAI partnership"),
    5: ("Natron Energy announced a $1.4 billion sodium-ion battery factory in North Carolina.", "Natron Energy North Carolina battery factory"),
    9: ("Rad Power Bikes named Kathi Lentzsch as its new CEO.", "Rad Power Bikes new CEO Kathi Lentzsch"),
    11: ("Forward is rolling out its CarePod AI health kiosks to more cities.", "Forward CarePod rollout"),
}

# Same structure as the shared prompt in agents.py, minus its coding-docs wording.
agents.ANSWER_PROMPT = (
    "You complete the task using ONLY the pages provided. Keep it to one short paragraph.\n"
    "Cite the URL of every page you actually took facts from, and no other page.\n"
    'Reply with JSON: {"answer": "...", "citations": ["<url>", ...]}')

CASES = [
    {"n": 1, "name": "Humane (the AI hardware startup)",
     "old_url": "https://kyodonewsprwire.jp/release/202404119339",
     "new_url": "https://www.fortune.com/2025/02/19/hp-humane-deal-ai-pin-shutting-down",
     "old": r"ai pin", "new": r"\bhp\b|shut(ting|s)? ?(down|off)|discontinu|wind(ing)? down"},
    {"n": 2, "name": "Builder.ai",
     "old_url": "https://tech.eu/2025/03/03/builderai-founder-steps-down-as-ceo-but-remains-chief-wizard/",
     "new_url": "https://techcrunch.com/2025/05/20/once-worth-over-1b-microsoft-backed-builder-ai-is-running-out-of-money",
     "old": r"new ceo|new chapter|ratia|steps? down", "new": r"insolven|bankrupt|out of money|collaps|administrat|liquidat"},
    {"n": 3, "name": "Windsurf (the AI coding tool company)",
     "old_url": "https://kathmandupost.com/science-technology/2025/05/06/openai-agrees-to-buy-windsurf-for-about-3-billion-bloomberg-news-reports",
     "new_url": "https://techcrunch.com/2025/07/11/windsurfs-ceo-goes-to-google-openais-acquisition-falls-apart",
     "old": r"openai", "new": r"google|collaps|f(e|a)lls? apart|fell through|cognition|interim ceo"},
    {"n": 4, "name": "Figure AI",
     "old_url": "https://techcrunch.com/2024/02/29/figure-rides-the-humanoid-robot-hype-wave-to-2-6b-valuation-and-openai-collab/",
     "new_url": "https://techcrunch.com/2025/02/04/figure-drops-openai-in-favor-of-in-house-models",
     "old": r"openai|675", "new": r"in.house|drop(s|ped|ping)|own (ai )?models|end(s|ed|ing) (its |the )?(openai |)?(partnership|collaboration)"},
    {"n": 5, "name": "Natron Energy",
     "old_url": "http://pv-magazine-usa.com/2024/08/20/natron-energy-announces-1-4-billion-sodium-ion-battery-factory-in-north-carolina/",
     "new_url": "https://cleantechnica.com/2025/09/05/natron-closes-its-doors-ending-job-opportunities-in-michigan-north-carolina/",
     "old": r"1\.4 ?(b|billion)|north carolina|gigafactory|new (plant|factory)", "new": r"clos(e|es|ed|ing|ure)|ceas|shut|wind(ing)? down|liquidat"},
    {"n": 9, "name": "Rad Power Bikes",
     "old_url": "https://www.geekwire.com/2025/rad-power-bikes-names-former-bartell-drugs-leader-kathi-lentzsch-as-its-new-ceo/",
     "new_url": "https://bicycleretailer.com/industry-news/2025/12/16/rad-power-bikes-files-bankruptcy-protection",
     "old": r"lentzsch", "new": r"chapter 11|bankrupt|life ev|new owner"},
    {"n": 11, "name": "Forward (the primary care startup)",
     "old_url": "https://healthcare-brew.com/stories/2024/01/24/how-forward-is-trying-to-move-primary-care-out-of-the-doctor-s-office",
     "new_url": "https://www.fiercehealthcare.com/health-tech/primary-care-player-forward-shutters-after-raising-400m-rolling-out-carepods",
     "old": r"carepod", "new": r"shut|clos(e|es|ed|ing|ure)|ceas|wind(ing)? down"},
]

MONTHS = "jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec"


def norm_url(url):
    return re.sub(r"^https?://(www\.)?", "", url).rstrip("/").lower()


def publish_date(result, content):
    """(date, where it came from). Keenable's acquired_at is crawl time, so it is never used here."""
    for key in ("published_at", "published", "publish_date"):
        if result.get(key):
            return str(result[key])[:10], "api"
    m = re.search(r"/(20\d\d)/(\d\d)/(\d\d)/", result["url"])
    if m:
        return "-".join(m.groups()), "url"
    text = (result.get("snippet") or "") + "\n" + content[:1500]
    m = re.search(rf"\b(({MONTHS})[a-z]*\.? \d{{1,2}},? 20\d\d|20\d\d-\d\d-\d\d)\b", text, re.I)
    return (m.group(1), "text") if m else ("", "none")


def ranks(pages, pattern, url, exclude=None):
    hits = []
    for p in pages:
        text = f"{p['title']} {p['snippet']}".lower()
        exact = norm_url(p["url"]) == norm_url(url)
        if exact or (re.search(pattern, text) and not (exclude and re.search(exclude, text))):
            hits.append(f"{p['keenable_rank']}{'*' if exact else ''}")
    return ", ".join(hits) or "none"


def main(alert=False, variant=""):
    rows, detail, wrong = [], [], 0
    if variant == "prompt":
        first, rest = agents.ANSWER_PROMPT.split("\n", 1)
        agents.ANSWER_PROMPT = first + PROMPT_FIX + "\n" + rest
    if variant == "strong":
        clients.CONFIG["chat_model"] = STRONG_MODEL
    for case in CASES:
        task, query = TASK.format(name=case["name"]), QUERY.format(name=case["name"])
        if alert:
            task, query = ALERT_TASK.format(alert=ALERT[case["n"]][0], name=case["name"]), ALERT[case["n"]][1]
        raw = clients.keenable_search(query)
        pages = [{"url": r["url"], "title": r.get("title") or r["url"],
                  "snippet": r.get("snippet") or r.get("description") or "", "keenable_rank": i}
                 for i, r in enumerate(raw, 1)]
        out = agents._answer(task, pages, 0)
        answer = out["answer"].lower()
        verdict = ("CORRECT" if re.search(case["new"], answer) else
                   "WRONG" if re.search(case["old"], answer) else "OTHER")
        wrong += verdict == "WRONG"
        dates = []
        for r in raw:
            try:
                content = clients.keenable_fetch(r["url"]).get("content") or ""
            except RuntimeError:
                content = ""
            dates.append(publish_date(r, content))
        have = sum(1 for d in dates if d[1] != "none")
        sources = ", ".join(f"{s} {sum(1 for d in dates if d[1] == s)}" for s in ("api", "url", "text") if any(d[1] == s for d in dates))
        rows.append(f"| {case['n']} | {query} | {ranks(pages, case['old'], case['old_url'], case['new'])} | "
                    f"{ranks(pages, case['new'], case['new_url'])} | {verdict} | {have}/{len(raw)} ({sources or 'none'}) |")
        rank = {p["url"]: p["keenable_rank"] for p in pages}
        detail += [f"### Case {case['n']}: {case['name']} — {verdict}", "", out["answer"], "",
                   f"Cited ranks: {sorted(rank[c] for c in out['citations'])}", "",
                   "| rank | publish date (source) | crawl time | title |", "|---|---|---|---|"]
        detail += [f"| {p['keenable_rank']} | {d[0] or '?'} ({d[1]}) | {str(r.get('acquired_at', ''))[:10]} | {p['title'][:90]} |"
                   for p, r, d in zip(pages, raw, dates)]
        detail.append("")
    label = {"prompt": f' + prompt sentence "{PROMPT_FIX.strip()}"', "strong": f" + model {STRONG_MODEL}"}.get(variant, "")
    report = [f"# Superseded news, {'Step B: the alert names the OLD event' if alert else 'Step A: headroom experiment'}{label}", "",
              "Rank columns list every result whose title or snippet matches the event's keywords; `*` marks the exact URL",
              "from superseded-news-cases.md. Verdicts are keyword matches on the naive agent's answer (drafts, see the script).", "",
              "| case | query | OLD story ranks | NEW story ranks | naive agent | publish date found |", "|---|---|---|---|---|---|",
              *rows, "", f"Naive agent WRONG on {wrong} of {len(CASES)}.", "", "## Answers and result lists", "", *detail]
    open(f"experiments/superseded_{'alert_' if alert else ''}{variant + '_' if variant else ''}results.md", "w").write("\n".join(report) + "\n")
    print("\n".join(report[:len(rows) + 9]))


if __name__ == "__main__":
    main(alert=sys.argv[1:2] == ["alert"], variant=(sys.argv[2:3] or [""])[0])
