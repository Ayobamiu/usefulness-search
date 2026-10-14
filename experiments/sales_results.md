# Sales research: naive vs ours on every company in the case list

Task: "Write a one-paragraph sales outreach angle for {company} based on their latest news."  Query: "{company} news"  n=15 companies, 1 run each. Prices are simulated.
Verdicts are keyword checks (current / stale / other). **Usman: please read the answers below and confirm.**

| | naive (reads 10) | ours |
|---|---|---|
| current | 8 | 10 |
| stale | 1 | 0 |
| other | 6 | 5 |
| pages read | 10.0 | 3.1 |
| tokens per query | 14065 | 21424 (reading 4957 + scoring 16467) |
| cost per query (pages simulated + tokens) | 29.98c | 10.65c |

| company | naive | ours | pages | tokens naive | tokens ours (reading + scoring) | cost naive | cost ours |
|---|---|---|---|---|---|---|---|
| Humane (the AI hardware startup) | current | current | 3 | 13665 | 20910 (4570 + 16340) | 32.51c | 11.15c |
| Builder.ai | current | current | 3 | 15109 | 23253 (5531 + 17722) | 30.55c | 10.80c |
| Windsurf (the AI coding tool company) | current | current | 3 | 18331 | 23469 (5609 + 17860) | 32.11c | 10.59c |
| Figure AI | other | other | 3 | 11481 | 20610 (4922 + 15688) | 28.48c | 10.32c |
| Natron Energy | current | current | 3 | 13491 | 21704 (5451 + 16253) | 29.24c | 10.71c |
| Rad Power Bikes | current | current | 3 | 15973 | 22958 (4597 + 18361) | 29.60c | 11.16c |
| Forward (the primary care startup) | current | current | 4 | 14775 | 22064 (5652 + 16412) | 30.54c | 11.95c |
| Notion | other | other | 3 | 16518 | 22419 (5906 + 16513) | 29.77c | 10.99c |
| 80 Acres Farms | current | current | 3 | 11608 | 19353 (4832 + 14521) | 30.15c | 8.89c |
| Limitless (formerly Rewind) | current | current | 3 | 12626 | 18427 (3297 + 15130) | 30.38c | 9.39c |
| Plenty (the vertical farming company) | stale | current | 3 | 8401 | 19168 (3718 + 15450) | 26.62c | 11.32c |
| Northvolt | other | current | 3 | 18210 | 21376 (4954 + 16422) | 29.18c | 10.57c |
| Tools for Humanity (World) | other | other | 3 | 11628 | 20704 (4106 + 16598) | 28.30c | 9.95c |
| Lattice (the HR software company) | other | other | 3 | 16489 | 22524 (5828 + 16696) | 32.74c | 11.57c |
| Scale AI | other | other | 3 | 12677 | 22425 (5388 + 17037) | 29.61c | 10.44c |

## Answers

### Humane (the AI hardware startup)

**Naive (current):** Target Humane’s successor, HP IQ, rather than pitching it as an independent hardware startup: HP acquired its software, IP and engineering talent for $116 million in February 2025, while the AI Pin was discontinued and lost cloud functionality. The outreach angle is helping HP IQ turn that technology into reliable AI experiences across PCs and office hardware—position integration support, latency testing and cloud-resilience tooling as ways to reduce deployment risk. Lead with: “As you bring Humane’s technology into HP’s ecosystem, could we discuss helping your team validate responsiveness and service continuity before scaling to more devices?”

**Ours (current):** Target Humane’s former team within HP IQ, rather than pitching it as an independent hardware startup: HP’s $116 million acquisition brought its software, IP and talent into HP, while the AI Pin was discontinued. Lead with helping the team turn CosmOS into reliable AI experiences across HP’s products, positioning integration support, automated testing and AI performance monitoring as ways to accelerate delivery and reduce execution risk. Outreach hook: “As your team brings Humane’s AI technology into HP’s portfolio, could we help streamline integration and validate real-world reliability before launch?”

### Builder.ai

**Naive (current):** Lead with recovery and continuity, not growth: the latest supplied update places Builder.ai’s U.S. entity, Engineer.ai Corp., in Chapter 7 bankruptcy and its UK entity, Engineer.ai Global Limited, in compulsory liquidation, with status varying by entity. Tailor outreach to administrators or relevant stakeholders around assessing recoverable software assets, clarifying code and data access, and planning customer handovers. A practical opener: “Given the insolvency proceedings, would a focused assessment of recoverable projects and migration options help you prioritize next steps and reduce disruption for affected customers?”

**Ours (current):** Lead with business continuity and asset recovery, not a growth pitch: the latest supplied update, dated August 12, 2026, identifies U.S. entity Engineer.ai Corp. in Chapter 7 bankruptcy and UK entity Engineer.ai Global Limited in compulsory liquidation. Target the relevant insolvency representatives or affected customers with a tightly scoped offer to assess recoverable code, secure infrastructure access, and plan migration or project completion. Position the outreach around transparent costs and verifiable deliverables, while confirming asset ownership and purchasing authority before proposing work.

### Windsurf (the AI coding tool company)

**Naive (current):** Pitch Windsurf’s team—now part of Cognition’s Devin Desktop—on scaling enterprise adoption after its June 2026 rebrand. Cognition’s July 14 retrospective reported growth from 44 to 350 employees and a revenue run rate exceeding $500 million, making onboarding and adoption a timely conversation: “With Windsurf now unified under Devin Desktop and your business scaling rapidly, how are you helping enterprise customers adopt local and cloud agents without disrupting established workflows? Could we explore ways to simplify that transition and demonstrate measurable developer productivity gains?”

**Ours (current):** Reach out to Windsurf’s team under its current Cognition/Devin brand with an enterprise-adoption angle: “Congratulations on the transition to Devin Desktop and July’s reported milestone of more than $500 million in combined revenue run rate. With Cascade replaced by Devin Local and local, cloud, and third-party agents coming together in one workspace, there’s a timely opportunity to help enterprise customers navigate the transition and expand adoption. Could we explore ways to streamline onboarding and demonstrate the value of these multi-agent workflows?” Position the pitch around supporting this product transition and growth—not Windsurf as a standalone company.

### Figure AI

**Naive (other):** Figure’s retirement of most F.02 robots highlights a timely sales angle: secure hardware lifecycle management that protects proprietary technology without diverting engineers from F.04 development. Outreach could lead with: “Your F.02 sendoff underscored a challenge beyond retirement: protecting custom hardware while keeping technical teams focused on the next generation. As your F.03 fleet grows, would it be worth exploring a repeatable decommissioning workflow designed to safeguard IP and reduce internal engineering effort?”

**Ours (other):** Lead with Figure’s transition from F.02 retirement to scaling Figure 03 and improving Helix: the opportunity is helping turn rapid robotics iteration into reliable deployments. Position fleet observability and training-data operations as ways to capture failures, prioritize high-value real-world examples, and reduce engineering overhead across robot generations. Personalize outreach around Helix 2.5’s reported 56% task success across 30 unfamiliar homes: “As you scale Figure 03, could better fleet-to-training feedback help your team improve task completion without adding operational burden?” Offer a focused pilot around failure analysis and data capture.

### Natron Energy

**Naive (current):** Natron Energy’s September 2025 shutdown after funding fell short makes wind-down support—not factory expansion—the relevant sales angle. With Sherwood Partners engaged to sell its assets, target the asset-sale team or prospective buyers with services that could preserve and recover value from Natron’s sodium-ion intellectual property and manufacturing equipment, such as technical due diligence, equipment disposition, or technology-transfer support. Lead with: “As Natron’s assets transition, could we help evaluate the technology and equipment for potential buyers and reduce handover risk?”

**Ours (current):** Natron Energy’s September 2025 shutdown, asset liquidation, and cancellation of its $1.4 billion North Carolina gigafactory make wind-down support—not manufacturing expansion—the relevant sales angle. Direct outreach to those managing the remaining assets, positioning services around equipment disposition, asset valuation, or buyer identification: “Given Natron’s closure, would support identifying qualified buyers and coordinating asset disposition help simplify the wind-down and preserve recovery value?” Confirm who controls the assets before pursuing outreach rather than assuming Natron remains an active buyer.

### Rad Power Bikes

**Naive (current):** With Life EV’s acquisition completed on March 5, 2026, and plans for U.S. assembly, expanded retail, and improved customer support, Rad’s next chapter offers a timely outreach angle: rebuilding rider confidence while simplifying operations. Position your offering as support for that transition: “As Rad rebuilds under Life EV, clear warranty communication, reliable service coordination, and inventory visibility could help turn renewed interest into repeat business. Could we explore a focused pilot to support your retail and service expansion while reducing friction for existing riders?”

**Ours (current):** Position your outreach around rebuilding rider confidence during Rad Power Bikes’ transition to Rad Life Mobility: “With Life EV’s acquisition complete and plans to expand retail, improve customer service, and support existing riders, this is a timely opportunity to make your brand’s next chapter tangible. We’d welcome a conversation about streamlining owner communications, service requests, and battery-replacement updates—helping customers navigate the transition while supporting your retail growth. Would a brief discussion about your post-acquisition customer-experience priorities be useful?”

### Forward (the primary care startup)

**Naive (current):** Forward shut down in November 2024, so avoid outreach premised on clinic expansion or CarePod growth. A better angle is relationship-building with former leadership: reporting indicated Adrian Aoun and other executives were recruiting for a new startup shortly after the closure. Try: “Saw the reports that you were exploring a new venture after Forward. If that effort is still active, we’d welcome a conversation about validating customer demand and unit economics before committing to a capital-intensive rollout. Is that relevant to what you’re building next?” Verify their current roles before sending.

**Ours (current):** Forward shut down on November 13, 2024, so its earlier funding and nationwide expansion plans are not a valid sales trigger. Remove it from active growth campaigns; the more credible angle is relationship-building with former leadership around a verified next venture. If one is confirmed, lead with: “As you plan your next build, we’d welcome a conversation about validating operating costs and rollout readiness before scaling—helping ambitious healthcare technology reach patients sustainably.” Treat this as a conditional prospecting angle, not evidence that Forward is buying.

### Notion

**Naive (other):** Hi Notion team—your September 2 update giving admins control over AI model access, alongside agents’ new suggested-edit workflow, creates a strong enterprise story: more AI productivity without giving up oversight. A timely partnership angle is helping customers turn those controls into practical rollout plans, with model-selection policies, review workflows, and team onboarding. Would you be open to exploring a focused enablement pilot that helps enterprise customers move from experimenting with agents to adopting them confidently?

**Ours (other):** Notion’s July 31 update lets AI Meeting Notes trigger Custom Agents to update project trackers, share recaps, and turn feedback into engineering tickets—creating a timely outreach angle around turning new AI capabilities into repeatable customer workflows. Target Notion’s product or growth team: “Your latest meeting-to-action automation makes the value of agents tangible. As you roll it out, could a focused activation pilot help more teams adopt these workflows and measure the manual follow-up they eliminate? We’d start with one post-meeting workflow and track adoption and time saved.”

### 80 Acres Farms

**Naive (current):** Lead with transition support, not a growth pitch: 80 Acres Farms announced it is winding down after failing to secure capital, so outreach should sensitively focus on reducing closure costs and preserving asset value. Offer a narrowly scoped conversation about equipment disposition, vendor closeout, or secure data handover rather than new operational investment. If your offering relates to its technology, first confirm who is handling Infinite Acres and GroLoop—their inclusion in the wind-down remains unclear—before proposing support for any potential transfer or continued commercialization.

**Ours (current):** Lead with wind-down support, not growth: 80 Acres Farms announced on August 3, 2026, that it was winding down after failing to secure capital, with a prospective acquisition falling through the previous evening. Outreach should sensitively target leadership overseeing the transition and emphasize near-term cost reduction, asset recovery, or vendor closeout rather than long-term investment. Suggested opener: “Given the difficult transition underway at 80 Acres, would a brief conversation about reducing shutdown costs and coordinating asset and vendor closeout be useful? We’d keep the scope narrow and focused on immediate value.”

### Limitless (formerly Rewind)

**Naive (current):** Lead with post-acquisition integration rather than standalone product growth: Meta acquired Limitless (formerly Rewind) on December 5, 2025, bringing its team into Reality Labs while ending new Pendant sales and sunsetting Rewind. Outreach should position your offering around reducing transition workload, protecting customer data, or accelerating AI-wearables development—not helping sell more Pendants. Suggested hook: “Congratulations on joining Meta. As your team balances existing-customer support with its new wearables mission, could we explore ways to streamline migration and compliance workflows so engineers can stay focused on product development?”

**Ours (current):** Congratulations on Limitless joining Meta’s Reality Labs wearables organization. With pendant sales ending and Rewind winding down, the strongest outreach angle is supporting a smooth transition—not expanding the standalone product. Position your offering around helping the team maintain service for existing pendant users, streamline customer data exports, or reduce integration overhead as it shifts toward Meta’s broader AI-wearables roadmap. A timely opener: “As Limitless transitions into Meta, how are you balancing existing-user support with integration priorities—and would a conversation about reducing that operational load be useful?”

### Plenty (the vertical farming company)

**Naive (stale):** Lead with operational efficiency rather than expansion: July 2026 coverage shows Plenty relinquished its option on 66 acres at its Chesterfield strawberry campus while retaining a 30-acre option through April 2029. That creates a timely opening for a sales conversation about improving the existing operation without major new capital commitments. Position your offering around measurable reductions in production costs, downtime, or waste—not another ambitious buildout—and propose a tightly scoped pilot: “As Plenty refines its campus plans, would it be useful to explore a low-capital way to improve strawberry production economics, with clear ROI milestones before any broader rollout?”

**Ours (current):** Lead with capital-efficient strawberry production—not expansion. Plenty’s latest news is its April 2026 decision to waive additional land rights at Meadowville Tech Park, scaling back campus plans following its 2025 emergence from Chapter 11 and pivot toward strawberries. Frame outreach around improving the economics of its existing farm: reducing energy costs, minimizing downtime, or increasing saleable yield without a major capital commitment. A relevant opener: “With Plenty focusing its strawberry operations rather than expanding its campus, would a small, measurable pilot to improve production efficiency at the existing facility be worth exploring?”

### Northvolt

**Naive (other):** Lead with coordinated site redevelopment, not Northvolt’s old expansion story: Lyten has acquired its Swedish battery assets, while EdgeConneX is planning a seven-building data-center campus on former Northvolt land in Skellefteå. Target Lyten’s Swedish operations and infrastructure leaders with an offer to coordinate energy demand, contractor schedules and commissioning across the evolving site. Position a focused assessment as a way to identify potential power and execution bottlenecks before major commitments, then ask: “Would a short workshop to map infrastructure dependencies and prioritize near-term risks be useful?”

**Ours (current):** Lead with restart readiness and rebuilding customer confidence—not factory expansion. Following Northvolt’s bankruptcy, Lyten acquired its key Swedish assets in February 2026 and plans commercial NMC battery-cell deliveries in the second half of 2026. Target the Lyten team overseeing the former Northvolt operations with a focused pitch: “As you restart Northvolt Ett, could we explore a small pilot to improve production visibility, strengthen quality controls and demonstrate reliable delivery to prospective customers?” Position the offer around measurable operational results rather than another ambitious scale-up promise.

### Tools for Humanity (World)

**Naive (other):** World’s September launch of World Money across 150+ countries creates a timely outreach angle around turning global availability into funded, active users. With Stripe enabling U.S. Apple Pay-to-stablecoin funding and World ID unlocking additional savings rewards, pitch support for reducing onboarding friction, explaining self-custody clearly, and tailoring activation journeys to regional feature availability. Lead with: “As World Money scales globally, how are you identifying where users drop off between signup, verification, and their first funded transaction—and could a focused activation pilot help improve conversion?”

**Ours (other):** With September’s launch of World Money across more than 150 countries, Tools for Humanity has a timely outreach hook: turning global availability into active, verified financial users. Lead with an offer to help streamline onboarding and measure conversion from account creation to World ID verification and first funded transaction, particularly across Stripe funding, Kalshi, and Morpho integrations. Position the value around reducing onboarding friction and improving activation while accommodating jurisdiction-specific feature availability, then propose a focused pilot in one market with clear conversion metrics.

### Lattice (the HR software company)

**Naive (other):** Lead with helping Lattice turn its AI-native performance push into measurable customer adoption. Its latest updates highlight an AI Agent that joins calls, generates recaps, and delivers coaching insights, while the Pando acquisition strengthens its continuous, evidence-based performance strategy. Outreach to Chief Marketing and Strategy Officer Barbra Gago could center on translating those capabilities into clear buyer messaging and customer proof: “As Lattice moves beyond review cycles toward continuous coaching, how are you helping HR buyers quantify the impact—and turning early customer wins into a repeatable sales story?”

**Ours (other):** Lead with helping Lattice turn its AI-native performance strategy into customer adoption. Its latest updates highlight an AI Agent that joins 1:1 calls and delivers recaps and coaching, MCP availability in Glean’s Marketplace, and the recent Pando acquisition—creating a timely opening around product education and go-to-market enablement. Outreach hook: “With your AI Agent expanding into everyday manager conversations and Pando joining Lattice, how are you helping customers turn these capabilities into repeatable habits? Would it be useful to explore ways to simplify onboarding and demonstrate value through manager adoption and time saved?”

### Scale AI

**Naive (other):** Lead with Scale AI’s expanded defense work: the Air Force recently added $12.1 million to its E-4C agentic AI contract, bringing its value to $44.3 million, with work running through November 2027. Use that milestone to open a conversation with its public-sector engineering team about supporting rigorous agent evaluation, traceability, and deployment readiness—not assume gaps in its current capabilities. Suggested hook: “Congratulations on the E-4C expansion. As the program scales, is reducing the effort needed to validate agent reliability and document test results a priority? Would a brief discussion about your evaluation workflow be useful?”

**Ours (other):** Scale AI’s latest $12.1 million Air Force contract expansion—bringing its E-4C agentic AI work to $44.3 million—creates a timely outreach angle around validating AI for mission-critical environments. Lead with: “Congratulations on the E-4C expansion. As Scale takes on more high-stakes defense work, how are you scaling agent testing, failure monitoring, and audit-ready evidence without slowing delivery? We’d welcome a conversation about supporting those workflows so your teams can demonstrate reliability as deployment demands grow.” Position these as discovery questions, not claims about gaps in Scale’s capabilities.

