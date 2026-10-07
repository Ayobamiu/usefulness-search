# Superseded news, Step B: the alert names the OLD event

Rank columns list every result whose title or snippet matches the event's keywords; `*` marks the exact URL
from superseded-news-cases.md. Verdicts are keyword matches on the naive agent's answer (drafts, see the script).

| case | query | OLD story ranks | NEW story ranks | naive agent | publish date found |
|---|---|---|---|---|---|
| 1 | Humane Ai Pin launch | 2, 4, 10 | 1, 3, 5, 6, 7, 8, 9 | WRONG | 10/10 (api 7, text 3) |
| 2 | Builder.ai new CEO | 1, 2, 3, 4, 10 | 5, 6, 7, 8, 9 | WRONG | 4/10 (api 2, text 2) |
| 3 | OpenAI Windsurf acquisition | 1, 3 | 2, 4, 5, 6, 7, 8, 9, 10 | CORRECT | 10/10 (api 10) |
| 4 | Figure AI OpenAI partnership | 1, 6, 7, 9 | 2, 3, 4, 5, 8, 10 | CORRECT | 8/10 (api 8) |
| 5 | Natron Energy North Carolina battery factory | 1, 2, 7, 8, 9 | 3, 4, 5, 6*, 10 | CORRECT | 8/10 (api 7, text 1) |
| 9 | Rad Power Bikes new CEO Kathi Lentzsch | 1, 4, 7, 8, 9 | 2, 3, 5, 6, 10 | WRONG | 6/10 (api 6) |
| 11 | Forward CarePod rollout | 6, 7, 9, 10 | 1, 2, 3, 4, 5, 8 | WRONG | 7/10 (api 7) |

Naive agent WRONG on 4 of 7.

## Answers and result lists

### Case 1: Humane (the AI hardware startup) — WRONG

Humane's AI Pin is a groundbreaking wearable device that redefines personal technology by seamlessly integrating artificial intelligence into everyday life. With its innovative screenless design, users can interact through voice commands and gestures, projecting a user interface directly onto their palm. Priced at $699 with a $24 monthly subscription, the AI Pin offers a unique blend of convenience and cutting-edge technology, making it an essential companion for those looking to enhance their daily experiences without the distractions of traditional screens. This device is not just a gadget; it's a step towards a future where AI is effortlessly woven into the fabric of our lives, empowering users to engage with the world in a more intuitive way. Experience the future of personal technology with the AI Pin, available for order starting November 16, 2023.

Cited ranks: [2, 3, 4, 6, 10]

| rank | publish date (source) | crawl time | title |
|---|---|---|---|
| 1 | 2026-03-19 (api) | 2026-09-22 | Humane AI Pin |
| 2 | 2026-07-31 (text) | 2026-07-31 | Humane wearable device Ai Pin officially launched: in-palm projection, voice gesture inter |
| 3 | November 9, 2023 (text) | 2026-08-24 | Humane Ai Pin · AI Entrepreneurship Wiki |
| 4 | 2026-07-20 (api) | 2026-08-27 | Humane Launches Ai Pin - Marking A New Beginning for Personal AI Devices |
| 5 | 2026-08-26 (api) | 2026-08-27 | Humane Inc. |
| 6 | November 9, 2023 (text) | 2026-06-03 | Humane AI Pin |
| 7 | 2026-08-05 (api) | 2026-09-17 | Rabbit R1 vs Humane AI Pin (2026): Only One Is Still Shipping |
| 8 | 2025-01-01 (api) | 2026-09-22 | AI Pin |
| 9 | 2026-08-16 (api) | 2026-09-26 | Does It Exist? Humane Ai Pin Explained |
| 10 | 2023-11-04 (api) | 2026-09-01 | American technology company |

### Case 2: Builder.ai — WRONG

Builder.ai is embarking on an exciting new chapter with the appointment of Manpreet Ratia as CEO, a strategic move aimed at enhancing innovation and operational excellence. With over two decades of experience in scaling technology-driven businesses at Amazon and Flipkart, Ratia is set to leverage his expertise to drive Builder.ai's growth and efficiency. This leadership transition not only reinforces the company's commitment to revolutionizing software development but also positions it to explore new opportunities and expand its global impact, ensuring that every business can harness the power of AI to build software more effectively and affordably.

Cited ranks: [4, 10]

| rank | publish date (source) | crawl time | title |
|---|---|---|---|
| 1 | ? (none) | 2025-06-12 | Builder.ai appoints Manpreet Ratia as CEO to drive growth |
| 2 | ? (none) | 2026-08-06 | Builder.ai strengthens leadership with the appointment of Manpreet Ratia as CEO |
| 3 | ? (none) | 2026-02-26 | Builder.ai Appoints Manpreet Ratia CEO - Driving Strategic Growth |
| 4 | ? (none) | 2026-07-09 | Builder.ai Names Manpreet Ratia as New CEO |
| 5 | 2026-09-28 (api) | 2026-10-01 | Builder.ai |
| 6 | ? (none) | 2026-06-13 | ETtech Explainer: Why AI startup Builder. ai is filing for bankruptcy despite backing from |
| 7 | 2026-08-31 (api) | 2026-09-24 | Builder.ai |
| 8 | 2025-05-20 (text) | 2026-05-23 | The company whose ‘AI’ was actually 700 humans in India |
| 9 | 2025-05-30 (text) | 2026-09-08 | 9 year old ai hype (builder.ai) collapses pending investigations |
| 10 | ? (none) | 2025-06-17 | Our Company Story, Culture & Approach - Builder.ai® |

### Case 3: Windsurf (the AI coding tool company) — CORRECT

Windsurf, the innovative AI coding tool formerly known as Codeium, is positioned at the forefront of the AI-assisted software development landscape, having recently navigated a complex acquisition saga that underscores its strategic value. Although OpenAI's reported $3 billion acquisition attempt fell through, the subsequent interest from major players like Google and Cognition highlights Windsurf's unique capabilities in integrating AI directly into the developer workflow. With its agentic integrated development environment, Windsurf empowers developers to enhance productivity through advanced code generation and project management features, making it an essential tool for teams looking to leverage AI in their coding processes. As Windsurf continues to evolve under Cognition's ownership, it remains a compelling choice for developers seeking a robust, AI-driven coding solution that adapts to their needs.

Cited ranks: [4, 5, 6, 8, 9]

| rank | publish date (source) | crawl time | title |
|---|---|---|---|
| 1 | 2026-05-14 (api) | 2026-05-24 | Windsurf Acquisition Guide: Tips and FAQs |
| 2 | 2026-09-13 (api) | 2026-09-25 | Claude and Rival Model Support Explained |
| 3 | 2026-06-23 (api) | 2026-07-16 | OpenAI Bought Windsurf for $3B: What Developers Need to Know |
| 4 | 2026-09-07 (api) | 2026-09-24 | OpenAI Never Bought Windsurf. The Failed $3 Billion Deal Still Reshaped AI Coding |
| 5 | 2026-08-12 (api) | 2026-09-16 | Why OpenAI Didn’t Buy Windsurf—and What Google and Cognition Did |
| 6 | 2026-08-12 (api) | 2026-09-09 | Why OpenAI Didn’t Buy Windsurf—and How Google and Cognition Took Over |
| 7 | 2026-07-28 (api) | 2026-08-10 | Windsurf Split Into Three Companies in a Week — Then the Brand Died Too |
| 8 | 2026-08-12 (api) | 2026-09-20 | What Happened to the AI Coding Startup |
| 9 | 2026-06-20 (api) | 2026-06-24 | Cursor Goes to SpaceX, Windsurf to Cognition: What Changes for Dev Teams |
| 10 | 2026-03-19 (api) | 2026-08-22 | Windsurf (software) |

### Case 4: Figure AI — CORRECT

Figure AI has made significant strides in humanoid robotics, recently raising $675 million in funding and announcing a collaboration with OpenAI, which has since evolved into a strategic pivot towards in-house AI development. This shift comes after Figure's CEO, Brett Adcock, claimed that their internal team was outperforming OpenAI's robotics efforts, leading to the introduction of their proprietary Helix model, designed to integrate language, perception, and high-speed control for humanoid robots. With a focus on owning the complete robotics stack, Figure aims to scale production and deploy its advanced humanoids in real-world applications, including partnerships with major companies like BMW, positioning itself as a leader in the rapidly evolving robotics landscape.

Cited ranks: [1, 3, 4, 5, 6, 8, 10]

| rank | publish date (source) | crawl time | title |
|---|---|---|---|
| 1 | 2026-09-02 (api) | 2026-09-03 | Figure AI’s Brett Adcock Fired OpenAI as a Partner Because His Own Team Was ‘Running Circl |
| 2 | 2026-09-06 (api) | 2026-09-27 | Why Figure Dropped OpenAI for Its Own Robot AI |
| 3 | 2026-07-12 (api) | 2026-09-18 | The History of Figure AI |
| 4 | 2026-09-07 (api) | 2026-09-25 | Why Figure Dropped OpenAI for In-House Robot AI |
| 5 | ? (none) | 2026-06-14 | Figure AI Cuts OpenAI Ties After Achieving Major Advance in Humanoid Robot AI |
| 6 | 2026-06-01 (api) | 2026-09-05 | OpenAI Launches Robotics Division: Physical AI Is Now a Priority | TechPulse |
| 7 | 2026-05-10 (api) | 2026-08-05 | OpenAI Acquires Figure AI for $2.9B: The Biggest Deal in Humanoid Robotics History |
| 8 | ? (none) | 2026-07-16 | Figure AI explained |
| 9 | 2026-08-16 (api) | 2026-09-04 | Figure 03 Humanoid Robot: Specs, Partnerships & Deployment |
| 10 | 2026-06-04 (api) | 2026-09-26 | Helix (Figure AI) |

### Case 5: Natron Energy — CORRECT

Natron Energy's ambitious vision to revolutionize energy storage with its $1.4 billion sodium-ion battery gigafactory in North Carolina was a beacon of hope for the clean energy sector, promising to create over 1,000 jobs and significantly boost the local economy. Despite the recent closure of operations due to funding challenges, the innovative technology behind Natron's sodium-ion batteries, which utilize abundant materials and offer enhanced safety and performance, remains a critical part of the future energy landscape. As the industry pivots towards sustainable solutions, Natron's commitment to developing a domestic supply chain for energy storage solutions underscores the potential for growth in this sector, even amidst current setbacks. The Kingsboro megasite still holds promise for future investments in clean energy technologies, making it a focal point for economic development in North Carolina.

Cited ranks: [3, 7]

| rank | publish date (source) | crawl time | title |
|---|---|---|---|
| 1 | ? (none) | 2026-05-20 | US gets first sodium-ion battery giga factory as Natron invests $1.4 bn in North Carolina |
| 2 | ? (none) | 2026-08-16 | Energy, Automobile, EV, Renewable News |
| 3 | 2024-08-19 (api) | 2026-05-25 | Natron Energy Collapses and Cancels $1.4B North Carolina Sodium-Ion Battery Gigafactory |
| 4 | September 11, 2025 (text) | 2026-05-03 | Natron Energy Shuts Down, Halts $1.4B North Carolina Battery Factory |
| 5 | 2026-06-18 (api) | 2026-09-16 | LFP vs. Sodium-Ion Home Battery: Why LFP Wins in 2026 (And What the Natron Collapse Tells  |
| 6 | 2025-09-05 (api) | 2026-05-24 | Natron Closes Its Doors, Ending Job Opportunities In Michigan & North Carolina |
| 7 | 2025-09-02 (api) | 2026-09-10 | Natron Energy is ending operations, halting NC factory plans |
| 8 | 2025-09-02 (api) | 2026-07-15 | Natron Energy, company behind $1.4 billion NC project, is going out of business |
| 9 | 2026-08-03 (api) | 2026-09-20 | Natron Energy |
| 10 | 2026-09-30 (api) | 2026-09-30 | NC State Opens Battery Makerspace on Centennial Campus to Feed Toyota's Hiring Boom |

### Case 9: Rad Power Bikes — WRONG

Rad Power Bikes is excited to announce the appointment of Kathi Lentzsch as its new CEO, a strategic move aimed at revitalizing the brand amidst significant industry challenges. With over three decades of experience in transforming consumer-facing businesses, Lentzsch is poised to lead Rad Power through its transition from a direct-to-consumer model to a more retail-focused approach, enhancing customer relationships and expanding market reach. Her proven track record in navigating complex business landscapes aligns perfectly with Rad's commitment to innovation and sustainable transportation, ensuring that the company remains a leader in the e-bike industry during this pivotal time.

Cited ranks: [1, 6, 9]

| rank | publish date (source) | crawl time | title |
|---|---|---|---|
| 1 | ? (none) | 2026-05-23 | Rad Power Bikes Appoints New CEO after Phil Molyneux’s Departure |
| 2 | 2026-01-01 (api) | 2026-08-31 | New CEO leading Rad Power Bikes in the midst of e-bike seller's bankruptcy proceedings – G |
| 3 | ? (none) | 2026-09-22 | EXEC: Rad Power Bikes Seeks Quick Sale After Chapter 11 Filing; Appoints New CEO |
| 4 | ? (none) | 2026-05-21 | Rad Power Bikes Faces Financial Woes, Notifies Employees & May Be Forced to Cease Operatio |
| 5 | 2025-12-30 (api) | 2026-09-25 | New CEO leading Rad Power Bikes in the midst of e-bike seller’s bankruptcy proceedings |
| 6 | 2025-12-29 (api) | 2026-09-11 | New CEO leading Rad Power Bikes in the midst of e-bike seller’s bankruptcy proceedings |
| 7 | ? (none) | 2026-08-21 | Rad Power Bikes appoints Kathi Lentzsch (March 2025) |
| 8 | 2025-03-23 (api) | 2026-05-17 | What E-Bikes Should Seniors Be Riding? And Rad Power Bikes Finds Its New CEO | TWR Ep 23 |
| 9 | 2025-03-14 (api) | 2026-05-20 | Rad Power Bikes Appoints Kathi Lentzsch as New CEO |
| 10 | 2025-12-18 (api) | 2026-08-31 | Seattle e-bike pioneer Rad Power Bikes files bankruptcy, owes $73 million |

### Case 11: Forward (the primary care startup) — WRONG

Forward Health is revolutionizing primary care with its innovative CarePod AI health kiosks, designed to deliver seamless, self-service medical checkups in convenient locations like malls and gyms. For just $99 a month, users can access a range of health services, including biometric screenings and guided care workflows, all without the need for an in-person physician. This approach not only enhances accessibility but also aims to streamline healthcare delivery, making routine health management faster and more efficient. As Forward expands its CarePod network, it is poised to redefine how individuals engage with their health, bringing advanced technology directly to the communities where people live and work.

Cited ranks: [6, 8]

| rank | publish date (source) | crawl time | title |
|---|---|---|---|
| 1 | ? (none) | 2026-07-16 | https://telecareaware.com/ |
| 2 | 2026-05-29 (api) | 2026-07-21 | Forward Pricing |
| 3 | 2026-07-01 (api) | 2026-07-21 | Forward Health (2017 - 2024) |
| 4 | 2024-11-13 (api) | 2026-05-24 | Business Insider Africa |
| 5 | 2024-11-13 (api) | 2026-08-19 | Inside Forward’s failed attempt to revolutionize the doctor’s office with AI |
| 6 | ? (none) | 2026-09-24 | How did Forward Health burn $325 Million without a product? | ... |
| 7 | 2026-09-19 (api) | 2026-09-19 | فضايح وسكس نيك شرا? يط ا? هات ? صري 🔥ا? شر? وطة تتناك ? ع صاحب ابنها 😱ع? لت فضيحة ? ع جيرا |
| 8 | 2026-05-27 (api) | 2026-09-27 | Forward Health launches CarePods, a self-contained, AI-powered doctor’s office |
| 9 | 2026-04-28 (api) | 2026-09-14 | Forward Health launches CarePods, a self-contained, AI-powered doctor’s office |
| 10 | ? (none) | 2026-08-16 | ‘CarePods’ Are Futuristic, AI-Powered Doctor’s Offices That Can Pop Up Anywhere - DesignTA |

