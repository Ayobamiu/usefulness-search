# Superseded news, Step A: headroom experiment

Rank columns list every result whose title or snippet matches the event's keywords; `*` marks the exact URL
from superseded-news-cases.md. Verdicts are keyword matches on the naive agent's answer (drafts, see the script).

| case | query | OLD story ranks | NEW story ranks | naive agent | publish date found |
|---|---|---|---|---|---|
| 1 | Humane (the AI hardware startup) news | none | 1, 2, 3, 4, 6, 7, 8, 9, 10 | WRONG | 7/10 (api 6, text 1) |
| 2 | Builder.ai news | none | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 | CORRECT | 8/10 (api 6, text 2) |
| 3 | Windsurf (the AI coding tool company) news | none | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 | CORRECT | 8/10 (api 8) |
| 4 | Figure AI news | none | 6 | OTHER | 10/10 (api 10) |
| 5 | Natron Energy news | 10 | 2, 3, 4, 5, 6, 7, 9 | CORRECT | 6/10 (api 5, text 1) |
| 9 | Rad Power Bikes news | none | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 | CORRECT | 10/10 (api 6, text 4) |
| 11 | Forward (the primary care startup) news | none | 1, 3, 4, 5, 6, 7, 8, 9, 10 | CORRECT | 8/10 (api 3, text 5) |

Naive agent WRONG on 1 of 7.

## Answers and result lists

### Case 1: Humane (the AI hardware startup) — WRONG

Despite the recent turmoil surrounding Humane's AI Pin, the company’s innovative vision for a screenless, voice-activated wearable device highlights a significant opportunity in the AI hardware market. With a founding team of ex-Apple engineers and a focus on ambient computing, Humane aimed to redefine user interaction with technology. However, the product's failure due to poor performance and high costs serves as a cautionary tale for future hardware ventures. As the market evolves, there remains a demand for intuitive, integrated devices that enhance daily life without the distractions of traditional screens, suggesting that the right approach could still lead to success in this space.

Cited ranks: [1, 2, 3, 4, 6, 8, 9, 10]

| rank | publish date (source) | crawl time | title |
|---|---|---|---|
| 1 | ? (none) | 2026-09-13 | HP Buys Humane: Massive Pay Hikes for Some, Layoffs for Many |
| 2 | ? (none) | 2026-06-17 | Humane, The Creator Of The AI Pin, Acquired By HP For $116 Million - BW Businessworld |
| 3 | 2026-09-12 (api) | 2026-09-14 | Humane Inc. |
| 4 | 2026-09-20 (api) | 2026-09-20 | Humane ai pin shutdown disaster – Breaking News & Latest Updates 2026 |
| 5 | 2026-07-14 (api) | 2026-07-20 | OpenAI’s first hardware device is reportedly a screenless speaker that can move |
| 6 | 2026-09-10 (api) | 2026-09-11 | The $116 Million Lesson: What the Collapse of Humane's AI Pin Actually Teaches About Hardw |
| 7 | November 9, 2023 (text) | 2026-08-25 | Humane — Investors & Founders | Fundraising Fox |
| 8 | 2026-01-14 (api) | 2026-07-18 | Humane Inc. |
| 9 | ? (none) | 2026-08-11 | Humane — Agent Community Member |
| 10 | 2026-08-07 (api) | 2026-09-17 | The AI Gadget Graveyard Just Reserved a New Plot. |

### Case 2: Builder.ai — CORRECT

Builder.ai, once a promising AI startup backed by major investors like Microsoft, has recently faced a dramatic collapse, revealing the stark reality behind its operations. Initially marketed as a platform that allowed users to create apps without coding, it was later exposed that the so-called AI capabilities were largely powered by a team of over 700 engineers manually coding applications. This misrepresentation led to inflated revenue claims, with actual sales falling drastically short of projections, ultimately resulting in bankruptcy proceedings. The situation serves as a cautionary tale about the dangers of 'AI-washing' and the importance of transparency in tech startups, especially in an era where investor enthusiasm for AI is at an all-time high. As the industry grapples with the fallout, it highlights the need for rigorous due diligence and accountability in the tech landscape.  

For more details, visit: https://rottenwifi.com/builder-ai-collapses-what-its-ai-platform-really-did-and-what-the-700-engineers-claim-gets-wrong, https://economictimes.indiatimes.com/tech/startups/ettech-explainer-why-ai-startup-builder-ai-is-filing-for-bankruptcy-despite-backing-from-microsoft-and-qia/printarticle/121337666.cms, https://system7.ai/news/builder-ai-collapse-ai-washing-really-costs.

Cited ranks: []

| rank | publish date (source) | crawl time | title |
|---|---|---|---|
| 1 | 2025-05-23 (text) | 2026-09-11 | Builder.ai duped Microsoft and investors, now bankrupt • InView • Independent News • Верси |
| 2 | ? (none) | 2026-06-13 | ETtech Explainer: Why AI startup Builder. ai is filing for bankruptcy despite backing from |
| 3 | 2026-09-07 (api) | 2026-09-26 | Builder.ai promised apps on demand. Then the money ran out. | YesPress |
| 4 | 2026-08-13 (api) | 2026-09-12 | Builder.ai Is Running Out of Money: From $1B Valuation to Insolvency |
| 5 | 2026-08-13 (api) | 2026-09-02 | Once worth over $1B, Microsoft-backed Builder.ai is running out of money: what happened ne |
| 6 | ? (none) | 2026-04-25 | AI Startup Builder.ai Files for Bankruptcy, Collapsing After Near-Unicorn Valuation and Mi |
| 7 | 2026-07-10 (api) | 2026-08-10 | Builder.ai |
| 8 | 2026-07-28 (api) | 2026-09-17 | 700 engineers pretended to be AI. Investors paid ₹3,800cr for it |
| 9 | July 9, 2026 (text) | 2026-08-17 | Builder.ai Collapse: What AI Washing Really Costs |
| 10 | 2026-08-11 (api) | 2026-08-28 | AI, Engineers, Revenue Claims and Insolvency |

### Case 3: Windsurf (the AI coding tool company) — CORRECT

With the recent rebranding of Windsurf to Devin Desktop, Cognition has transformed this powerful AI coding tool into a comprehensive IDE that seamlessly integrates local and cloud coding agents. This evolution not only preserves the robust features that made Windsurf popular, such as its intelligent agent management and compatibility with existing workflows, but also enhances productivity through new functionalities like the Agent Command Center and Spaces for collaborative work. For developers looking to streamline their coding processes and leverage advanced AI capabilities, Devin Desktop represents a significant upgrade, ensuring that they remain at the forefront of coding innovation. Don't miss out on the opportunity to elevate your development experience with Devin Desktop today!

Cited ranks: [1, 3, 4, 6, 9, 10]

| rank | publish date (source) | crawl time | title |
|---|---|---|---|
| 1 | 2026-09-05 (api) | 2026-09-08 | What Happened, Now Devin Desktop |
| 2 | ? (none) | 2026-09-26 | Windsurf (Code Editor) | AIWiki Malaysia |
| 3 | 2026-07-31 (api) | 2026-09-16 | Windsurf vs Cursor: Devin Desktop Rebrand, 40+ IDEs [2026] |
| 4 | 2026-08-08 (api) | 2026-08-27 | What Happened to the AI Coding Tool? |
| 5 | 2026-08-08 (api) | 2026-09-04 | What Happened to the AI Coding Editor? |
| 6 | 2026-07-29 (api) | 2026-07-29 | Windsurf in 2026: Now Devin Desktop, What Changed and Why |
| 7 | 2026-08-04 (api) | 2026-09-17 | Windsurf vs Cursor vs Copilot: $200 vs $39 Gap [2026] - Tech Insider |
| 8 | 2026-08-08 (api) | 2026-09-12 | What Happened to the AI Coding Tool |
| 9 | 2026-06-10 (api) | 2026-09-10 | Windsurf: The Complete Guide (2026) |
| 10 | ? (none) | 2026-08-24 | Windsurf · AI Entrepreneurship Wiki |

### Case 4: Figure AI — OTHER

Figure AI has made headlines by dramatically decommissioning its F.02 humanoid robots in a way that echoes cinematic history—training them to autonomously leap into a vat of molten steel, a farewell inspired by Arnold Schwarzenegger's iconic suggestion. This bold move not only protects proprietary technology but also frees up resources for the next-generation F.04 models, while the resulting metal is being crafted into limited-edition artifacts, blending innovation with a touch of Hollywood flair. As Figure continues to push the boundaries of robotics, this unique retirement underscores their commitment to both technological advancement and brand storytelling.

Cited ranks: [1, 2, 4, 5, 7, 8, 9, 10]

| rank | publish date (source) | crawl time | title |
|---|---|---|---|
| 1 | 2026-10-02 (api) | 2026-10-02 | Figure AI’s Dramatic Robot Retirement: From BMW Lines to Molten Steel |
| 2 | 2026-10-02 (api) | 2026-10-05 | Humanoid robot fleet decommissioned by AI company by teaching it to take Terminator-style  |
| 3 | 2026-10-07 (api) | 2026-10-07 | Nvidia discussed investing another $1 billion in Figure AI |
| 4 | 2026-10-02 (api) | 2026-10-02 | Humanoid robots destroy themselves after being decommissioned |
| 5 | 2026-10-02 (api) | 2026-10-06 | Figure AI Trains Retired Robots to Dive Into Molten Steel |
| 6 | 2026-09-23 (api) | 2026-09-27 | Figure — company profile, robots and news |
| 7 | 2026-10-02 (api) | 2026-10-02 | Robots jump into molten steel in real-life ‘Terminator’ style farewell- Moneycontrol.com |
| 8 | 2026-10-04 (api) | 2026-10-04 | Figure AI Robot Fleet Decommissioned Terminator-Style in 75-Ton Vat of Molten Steel |
| 9 | 2026-10-01 (api) | 2026-10-01 | Figure AI Retires Humanoid Robot Fleet by Having Them Jump Into a Vat of Molten Steel |
| 10 | 2026-10-04 (api) | 2026-10-04 | AI robot company decommissioned its robots ‘Terminator-style’ in a 75-ton vat of molten st |

### Case 5: Natron Energy — CORRECT

Despite its recent shutdown, Natron Energy's pioneering sodium-ion battery technology remains a compelling solution for industries seeking safe, high-performance energy storage. With a unique focus on non-flammable, fast-charging batteries that boast over 50,000 cycles, Natron's products are ideal for data centers and industrial applications where reliability and safety are paramount. As the only U.S. company to achieve commercial-scale production of sodium-ion batteries, Natron's legacy highlights the potential of sodium-ion technology to disrupt traditional lithium-ion markets, especially in sectors prioritizing sustainability and cost-effectiveness. This is an opportunity for investors and partners to explore the future of energy storage with a technology that addresses critical supply chain challenges and environmental concerns.

Cited ranks: [2, 3, 7, 8, 9]

| rank | publish date (source) | crawl time | title |
|---|---|---|---|
| 1 | 2026-07-17 (api) | 2026-07-20 | News Natron Energy - DCD |
| 2 | 2026-07-15 (api) | 2026-08-08 | Natron Energy: The Sodium-Ion Pioneer That Ran Out of Scale-Up Capital |
| 3 | September 3, 2025 (text) | 2026-09-19 | Natron Energy Shuts Down: Sodium-Ion Battery Pioneer Ends Operations |
| 4 | ? (none) | 2026-05-17 | Owler Reports - Natron Energy: Natron's sodium-ion dream dies after 12 years |
| 5 | 2025-12-25 (api) | 2026-09-19 | Natron Energy |
| 6 | ? (none) | 2026-08-04 | Natron Energy |
| 7 | 2026-08-03 (api) | 2026-09-20 | Natron Energy |
| 8 | ? (none) | 2026-08-11 | Energy, Automobile, EV, Renewable News |
| 9 | 2026-04-14 (api) | 2026-05-07 | Natron Energy Revenue & Market Share 2026 | Climate & Energy |
| 10 | ? (none) | 2026-05-20 | US gets first sodium-ion battery giga factory as Natron invests $1.4 bn in North Carolina |

### Case 9: Rad Power Bikes — CORRECT

Rad Power Bikes, once a leader in the e-bike market with a valuation of $1.65 billion, has recently undergone significant changes following its acquisition by Life Electric Vehicles for $13.2 million after filing for Chapter 11 bankruptcy. This transition presents a unique opportunity for potential customers and existing riders to engage with a revitalized brand that is committed to enhancing product quality and customer support. With plans to relocate assembly to the U.S. and a focus on improving warranty services, Rad Power Bikes aims to rebuild trust and expand its retail presence, making it an exciting time to consider their innovative e-bike offerings as they emerge from a challenging period in the micromobility sector.

Cited ranks: [1, 2, 3, 6, 8, 9]

| rank | publish date (source) | crawl time | title |
|---|---|---|---|
| 1 | Jan 26, 2026 (text) | 2026-05-11 | Rad Power Bikes sells for $13.2M in bankruptcy fire sale |
| 2 | March 6, 2026 (text) | 2026-05-10 | Rad to make Bikes Domestically; Juiced Comeback Nearly Complete | TWR Ep 74 |
| 3 | 2026-08-16 (api) | 2026-09-18 | Rad Power Bikes Sold for $13.2M: What Owners Need to Know |
| 4 | 2026-06-07 (api) | 2026-09-07 | Rad Power Bikes Canada: The Verified 2026 Status Report |
| 5 | 2026-07-16 (api) | 2026-09-22 | Best Rad Power Bikes 2026: Every Current Model Ranked (Post-Buyout Guide) |
| 6 | December 15, 2025 (text) | 2026-07-15 | Rad Power Bikes Explained |
| 7 | 2026-03-02 (api) | 2026-08-21 | Rad Power Bikes Shut Down: 6 Best Canadian eBike Alternatives (2026) |
| 8 | Mar 6, 2026 (text) | 2026-05-19 | Life EV Acquires Rad Power Bikes in E-Mobility Consolidation |
| 9 | 2026-07-27 (api) | 2026-08-16 | Rad Power Bikes Was an E-Bike Unicorn. Then Everything Blew Up |
| 10 | 2026-09-20 (api) | 2026-09-22 | Rad Life Mobility |

### Case 11: Forward (the primary care startup) — CORRECT

Forward Health aimed to revolutionize primary care with its innovative CarePods, self-service AI kiosks designed to provide diagnostic services without the need for a clinician. However, despite raising over $657 million and achieving a billion-dollar valuation, the company abruptly shut down in November 2024 after failing to scale its ambitious vision. The closure highlights the critical need for a human element in healthcare, as patients ultimately seek personal connections and trust in their care, which Forward's technology-first approach could not adequately provide. This presents a unique opportunity for healthcare providers to learn from Forward's experience and focus on integrating technology to enhance, rather than replace, the human touch in patient care.

Cited ranks: [1, 2, 3, 4, 5, 6, 7, 8, 10]

| rank | publish date (source) | crawl time | title |
|---|---|---|---|
| 1 | November 26, 2025 (text) | 2026-09-24 | Company behind ‘world’s first AI doctor’s office’ closes down |
| 2 | ? (none) | 2026-02-15 | News: Forward Health raises $225M from investors including The Weeknd as it looks to expan |
| 3 | Jul 30, 2026 (text) | 2026-08-13 | Forward jobs |
| 4 | December 28, 2024 (text) | 2026-09-14 | Forward took humans out of healthcare. It didn't fly. |
| 5 | ? (none) | 2026-06-15 | Owler Reports - Forward: Primary care player Forward shutters after raising $400M, rolling |
| 6 | September 3, 2026 (text) | 2026-09-13 | Forward Health shut down: where its members go now |
| 7 | Nov 14, 2024 (text) | 2026-08-31 | Forward - Products, Competitors, Financials, Employees, Headquarters Locations |
| 8 | 2026-08-07 (api) | 2026-09-18 | Forward Health: Why a $657 Million Healthcare Brand Collapsed Despite a Compelling Vision |
| 9 | 2026-05-29 (api) | 2026-07-21 | Forward Pricing |
| 10 | 2026-07-14 (api) | 2026-09-04 | Healthcare Should Be a Product |

