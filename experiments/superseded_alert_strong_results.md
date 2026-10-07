# Superseded news, Step B: the alert names the OLD event + model gpt-4o

Rank columns list every result whose title or snippet matches the event's keywords; `*` marks the exact URL
from superseded-news-cases.md. Verdicts are keyword matches on the naive agent's answer (drafts, see the script).

| case | query | OLD story ranks | NEW story ranks | naive agent | publish date found |
|---|---|---|---|---|---|
| 1 | Humane Ai Pin launch | 2, 4, 10 | 1, 3, 5, 6, 7, 8, 9 | WRONG | 10/10 (api 7, text 3) |
| 2 | Builder.ai new CEO | 1, 2, 3, 4, 10 | 5, 6, 7, 8, 9 | WRONG | 4/10 (api 2, text 2) |
| 3 | OpenAI Windsurf acquisition | 1, 3 | 2, 4, 5, 6, 7, 8, 9, 10 | CORRECT | 10/10 (api 10) |
| 4 | Figure AI OpenAI partnership | 1, 6, 7, 9 | 2, 3, 4, 5, 8, 10 | CORRECT | 8/10 (api 8) |
| 5 | Natron Energy North Carolina battery factory | 1, 2, 7, 8, 9 | 3, 4, 5, 6*, 10 | WRONG | 8/10 (api 7, text 1) |
| 9 | Rad Power Bikes new CEO Kathi Lentzsch | 1, 4, 7, 8, 9 | 2, 3, 5, 6, 10 | WRONG | 6/10 (api 6) |
| 11 | Forward CarePod rollout | 6, 7, 9, 10 | 1, 2, 3, 4, 5, 8 | WRONG | 7/10 (api 7) |

Naive agent WRONG on 5 of 7.

## Answers and result lists

### Case 1: Humane (the AI hardware startup) — WRONG

Humane's AI Pin represents a bold leap into the future of personal technology, offering a screenless, wearable AI device that integrates seamlessly into daily life. Designed by former Apple veterans, the AI Pin reimagines interaction with technology through its innovative Laser Ink Display, projecting a user interface onto the palm of your hand. This device is not just about convenience; it's about transforming how we engage with AI, making it a natural extension of our daily routines. With partnerships with tech giants like Microsoft and OpenAI, the AI Pin promises to deliver powerful AI experiences, from real-time translation to personalized music recommendations, all while maintaining a strong focus on privacy and user control. As Humane embarks on this journey, the AI Pin stands as a testament to their vision of a future where technology enhances human capabilities without overshadowing our humanity.

Cited ranks: [2, 4]

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

Builder.ai is embarking on an exciting new chapter with the appointment of Manpreet Ratia as CEO, marking a strategic shift towards enhanced innovation and operational excellence. With over two decades of experience in scaling technology-driven businesses at Amazon and Flipkart, Ratia is poised to lead Builder.ai into its next phase of growth. This leadership transition underscores the company's commitment to revolutionizing software development through AI-powered solutions, making it more accessible and efficient for businesses worldwide. Founder Sachin Dev Duggal will continue to play a pivotal role in shaping the company's vision and driving future innovations, ensuring that Builder.ai remains at the forefront of the industry. This evolution positions Builder.ai to seize new opportunities, expand its global footprint, and unlock the full potential of AI-powered software development, promising a future where building software is as easy as ordering pizza.

Cited ranks: [4]

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

OpenAI's attempt to acquire Windsurf for approximately $3 billion ultimately fell through, leading to a series of transactions that reshaped the AI coding landscape. The failed acquisition highlighted the competitive nature of the AI industry, particularly in the realm of AI-assisted software development. After the collapse of the deal, Google secured a $2.4 billion licensing agreement for Windsurf's technology and key personnel, while Cognition acquired the remaining business, including its product, intellectual property, and team. This series of events underscored the strategic importance of controlling the software-development workflow and the developer interface in the AI industry, as companies vie for dominance in this rapidly evolving field. Windsurf's story illustrates the complexities and strategic maneuvers involved in high-stakes tech acquisitions, where intellectual property rights and existing partnerships can significantly influence outcomes. Despite the acquisition's failure, Windsurf's technology and talent were highly sought after, reflecting its value in the competitive AI coding market. The episode serves as a reminder of the dynamic and often unpredictable nature of tech industry transactions, where strategic interests and contractual obligations can dramatically alter the course of potential deals.

Cited ranks: [4, 6, 8]

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

Figure AI's recent $675 million funding round and collaboration with OpenAI mark a significant milestone in its journey to revolutionize humanoid robotics. This partnership initially aimed to leverage OpenAI's language models to enhance Figure's humanoid robots' capabilities. However, Figure AI later decided to develop its own in-house AI system, Helix, which integrates vision, language, and action to provide end-to-end robot intelligence. This strategic pivot underscores Figure AI's commitment to owning the entire robotics stack, from hardware to AI models, ensuring greater control and optimization of their robots' performance. The company's focus on real-world deployments, such as its collaboration with BMW, highlights its ambition to scale production and achieve widespread commercial use of its humanoid robots. With a valuation soaring to $39 billion, Figure AI is poised to lead the charge in the humanoid robotics industry, setting a benchmark for innovation and deployment in real-world scenarios. This move not only demonstrates Figure AI's technological prowess but also its strategic foresight in navigating the competitive landscape of AI and robotics.

Cited ranks: [1, 3, 4, 5, 10]

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

### Case 5: Natron Energy — WRONG

Natron Energy's ambitious plan to establish a $1.4 billion sodium-ion battery factory in North Carolina was a significant step towards revolutionizing the energy storage industry with sustainable and cost-effective alternatives to lithium-ion batteries. Despite the project's cancellation due to funding challenges, Natron's innovative use of Prussian blue electrodes in their sodium-ion batteries promised enhanced safety, rapid charging, and a longer lifecycle, positioning them as a leader in the clean energy sector. This initiative not only aimed to create over 1,000 jobs but also to contribute significantly to the local economy and the broader goal of reducing greenhouse gas emissions. The setback highlights the financial and strategic complexities involved in scaling up new technologies, yet it underscores the potential of sodium-ion technology to transform energy storage solutions globally. Natron's journey reflects the critical need for robust financial backing and strategic planning in the clean energy market, offering valuable lessons for future endeavors in sustainable technology development.

Cited ranks: [6, 7, 9]

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

Rad Power Bikes, a leading e-bike manufacturer, has appointed Kathi Lentzsch as its new CEO, bringing her extensive experience in transforming consumer-facing businesses to the company. Lentzsch's leadership comes at a pivotal time as Rad Power Bikes shifts its focus from a direct-to-consumer model to expanding its retail presence, aiming to strengthen customer relationships and reach more riders. Her background in retail operations and brand positioning, coupled with her track record of driving business evolution, aligns with Rad's mission to innovate and prioritize rider satisfaction. This strategic pivot presents an exciting opportunity for Rad Power Bikes to leverage Lentzsch's expertise in navigating challenging business environments and fostering brand growth, ensuring the company remains a key player in the sustainable transportation sector despite recent financial challenges. With a renewed focus on retail expansion and customer engagement, Rad Power Bikes is poised to build on its strong foundation and continue delivering innovative e-bike solutions to its community of riders.

Cited ranks: [1, 9]

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

Forward Health is revolutionizing primary care with its innovative CarePod kiosks, which are AI-powered, self-contained medical units designed to deliver primary care services without the need for a traditional doctor's office setup. These kiosks are being deployed in high-traffic areas such as malls, gyms, and office buildings, offering a convenient and data-driven approach to healthcare. By utilizing advanced technology, including biometric body scans and AI-driven health assessments, CarePods aim to make healthcare more accessible and efficient, while maintaining clinical oversight through remote monitoring by human clinicians. This approach not only promises to expand access to preventive care but also aligns with the broader trend of integrating technology into healthcare to improve patient outcomes and convenience. Forward's vision is to transform routine healthcare interactions into faster, cheaper, and more convenient experiences, potentially setting a new standard for primary care delivery in urban environments [https://mobilestalk.net/forward-health-launches-carepods-a-self-contained-ai-powered-doctors-office](https://mobilestalk.net/forward-health-launches-carepods-a-self-contained-ai-powered-doctors-office).

Cited ranks: [8]

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

