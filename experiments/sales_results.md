# Sales research: naive vs ours on every company in the case list

Task: "Write a one-paragraph sales outreach angle for {company} based on their latest news."  Query: "{company} news"  n=15 companies, 1 run each. Prices are simulated.
Verdicts are keyword checks (current / stale / other). **Usman: please read the answers below and confirm.**

| | naive (reads 10) | ours |
|---|---|---|
| current | 9 | 8 |
| stale | 2 | 0 |
| other | 4 | 7 |
| pages read | 10.0 | 2.9 |
| tokens per query | 14054 | 17132 (reading 4574 + scoring 12559) |
| cost per query (pages simulated + tokens) | 25.07c | 8.38c |

| company | naive | ours | pages | tokens naive | tokens ours (reading + scoring) | cost naive | cost ours |
|---|---|---|---|---|---|---|---|
| Humane (the AI hardware startup) | stale | current | 3 | 13809 | 16836 (4201 + 12635) | 27.25c | 9.38c |
| Builder.ai | current | current | 3 | 15152 | 17137 (4627 + 12510) | 23.66c | 8.49c |
| Windsurf (the AI coding tool company) | current | current | 3 | 18302 | 19378 (5569 + 13809) | 28.78c | 9.36c |
| Figure AI | other | other | 1 | 11651 | 12466 (2032 + 10434) | 18.75c | 2.21c |
| Natron Energy | current | other | 3 | 13597 | 16456 (4329 + 12127) | 27.03c | 9.00c |
| Rad Power Bikes | current | current | 3 | 16063 | 18236 (4737 + 13499) | 27.08c | 9.14c |
| Forward (the primary care startup) | current | other | 3 | 13969 | 16524 (4677 + 11847) | 26.74c | 8.54c |
| Notion | current | current | 4 | 16492 | 21488 (7315 + 14173) | 23.40c | 10.05c |
| 80 Acres Farms | current | current | 3 | 11929 | 16694 (4804 + 11890) | 27.91c | 8.55c |
| Limitless (formerly Rewind) | current | current | 3 | 12623 | 15812 (4166 + 11646) | 25.66c | 8.90c |
| Plenty (the vertical farming company) | current | current | 3 | 8317 | 15489 (3479 + 12010) | 26.95c | 9.48c |
| Northvolt | other | other | 3 | 18099 | 18152 (5149 + 13003) | 23.71c | 8.20c |
| Tools for Humanity (World) | stale | other | 4 | 11710 | 18054 (4669 + 13385) | 22.54c | 10.15c |
| Lattice (the HR software company) | other | other | 3 | 16409 | 18697 (5538 + 13159) | 26.42c | 9.15c |
| Scale AI | other | other | 2 | 12682 | 15566 (3312 + 12254) | 20.11c | 5.14c |

## Answers

### Humane (the AI hardware startup)

**Naive (stale):** Despite the recent turmoil surrounding Humane's AI Pin, the company’s innovative vision for a screenless, voice-activated wearable device highlights a significant opportunity in the AI hardware market. With a founding team of ex-Apple engineers and a focus on ambient computing, Humane aimed to redefine user interaction with technology. However, the product's failure due to poor performance and high costs serves as a cautionary tale for future hardware ventures. As the market evolves, there remains a demand for intuitive, integrated devices that enhance daily life without the distractions of traditional screens, suggesting that the right approach could still lead to success in this space.

**Ours (current):** Humane Inc., founded by former Apple executives, aimed to revolutionize personal technology with its innovative AI Pin, a wearable device designed for seamless, screenless interactions. Despite raising over $240 million and generating significant buzz, the AI Pin faced critical performance issues and ultimately led to the company's acquisition by HP for $116 million. This transition marks a pivotal moment for HP as it integrates Humane's technology into its new AI innovation lab, HP IQ, focusing on enhancing user experiences across its product ecosystem. As a forward-thinking partner, HP is poised to leverage Humane's vision of ambient computing to redefine the future of work and personal technology.

### Builder.ai

**Naive (current):** Builder.ai, once a promising AI startup backed by major investors like Microsoft, has recently faced a dramatic collapse, revealing the stark reality behind its operations. Initially marketed as a platform that allowed users to create apps without coding, it was later exposed that the so-called AI capabilities were largely powered by a team of over 700 engineers manually coding applications. This misrepresentation led to inflated revenue claims, with actual sales falling drastically short of projections, ultimately resulting in bankruptcy proceedings. The situation serves as a cautionary tale about the dangers of 'AI-washing' and the importance of transparency in tech startups, especially in an era where investor enthusiasm for AI is at an all-time high. As the industry grapples with the fallout, it highlights the need for rigorous due diligence and accountability in the tech landscape.  

For more details, visit: https://rottenwifi.com/builder-ai-collapses-what-its-ai-platform-really-did-and-what-the-700-engineers-claim-gets-wrong, https://economictimes.indiatimes.com/tech/startups/ettech-explainer-why-ai-startup-builder-ai-is-filing-for-bankruptcy-despite-backing-from-microsoft-and-qia/printarticle/121337666.cms, https://system7.ai/news/builder-ai-collapse-ai-washing-really-costs.

**Ours (current):** Builder.ai, once a promising AI startup backed by Microsoft and the Qatar Investment Authority, is now facing bankruptcy after a major creditor seized $37 million from its accounts, leaving it with only $5 million. This dramatic turn of events highlights the precarious nature of startup valuations and the risks associated with aggressive growth strategies. As the first billion-dollar AI startup to collapse, Builder.ai's story serves as a cautionary tale for investors and entrepreneurs alike, emphasizing the need for sustainable business practices and transparency in financial reporting. If you're looking to build a resilient tech solution, consider partnering with a company that prioritizes stability and proven results over hype.

### Windsurf (the AI coding tool company)

**Naive (current):** With the recent rebranding of Windsurf to Devin Desktop, Cognition has transformed this powerful AI coding tool into a comprehensive IDE that seamlessly integrates local and cloud coding agents. This evolution not only preserves the robust features that made Windsurf popular, such as its intelligent agent management and compatibility with existing workflows, but also enhances productivity through new functionalities like the Agent Command Center and Spaces for collaborative work. For developers looking to streamline their coding processes and leverage advanced AI capabilities, Devin Desktop represents a significant upgrade, ensuring that they remain at the forefront of coding innovation. Don't miss out on the opportunity to elevate your development experience with Devin Desktop today!

**Ours (current):** With the recent rebranding of Windsurf to Devin Desktop, Cognition has transformed the AI coding landscape by integrating a powerful IDE with advanced agent management capabilities. This evolution not only retains the familiar workflows of Windsurf but enhances them with features like the Agent Command Center and Spaces for seamless collaboration across local and cloud agents. As a developer, you can now leverage the robust functionalities of Devin Desktop to streamline your coding process, manage multiple agents effortlessly, and maintain your existing development habits—all while benefiting from the backing of a rapidly growing company that has seen its revenue soar to over $500 million since the acquisition. Don't miss out on the opportunity to elevate your coding experience with Devin Desktop, where innovation meets efficiency.

### Figure AI

**Naive (other):** Figure AI has made headlines by dramatically decommissioning its F.02 humanoid robots in a way that echoes cinematic history—training them to autonomously leap into a vat of molten steel, a farewell inspired by Arnold Schwarzenegger's iconic suggestion. This bold move not only protects proprietary technology but also frees up resources for the next-generation F.04 models, while the resulting metal is being crafted into limited-edition artifacts, blending innovation with a touch of Hollywood flair. As Figure continues to push the boundaries of robotics, this unique retirement underscores their commitment to both technological advancement and brand storytelling.

**Ours (other):** At Figure AI, we are redefining the lifecycle of robotics with our recent dramatic retirement of the F.02 humanoid robots, which were trained to autonomously leap into a molten steel furnace, a move that not only protected our proprietary technology but also showcased our commitment to innovation. This bold step, inspired by Arnold Schwarzenegger, symbolizes our relentless pursuit of progress as we transition to the next generation of robots, the F.03 and beyond. By transforming our retired robots into commemorative artifacts, we are not just disposing of old technology; we are celebrating our journey and inviting you to be part of the future of robotics. Join us as we continue to push boundaries and create intelligent solutions for both industrial and household applications.  

Learn more about our latest advancements and how we can help you revolutionize your operations at [Figure AI](https://www.figure.ai/news/f-02-decommission).

### Natron Energy

**Naive (current):** Despite its recent shutdown, Natron Energy's pioneering sodium-ion battery technology remains a compelling solution for industries seeking safe, high-performance energy storage. With a unique focus on non-flammable, fast-charging batteries that boast over 50,000 cycles, Natron's products are ideal for data centers and industrial applications where reliability and safety are paramount. As the only U.S. company to achieve commercial-scale production of sodium-ion batteries, Natron's legacy highlights the potential of sodium-ion technology to disrupt traditional lithium-ion markets, especially in sectors prioritizing sustainability and cost-effectiveness. This is an opportunity for investors and partners to explore the future of energy storage with a technology that addresses critical supply chain challenges and environmental concerns.

**Ours (other):** Natron Energy is at the forefront of revolutionizing energy storage with its innovative sodium-ion batteries, which are not only non-flammable but also utilize abundant materials like sodium, making them a sustainable alternative to traditional lithium-ion batteries. With the recent commencement of commercial-scale production at their Holland, Michigan facility, Natron is poised to meet the growing demand for high-performance energy solutions, particularly in data centers and electric vehicle fast-charging applications. This strategic move not only strengthens the domestic supply chain but also positions Natron as a leader in the clean energy sector, ready to tackle the challenges of the electrification of our economy.

### Rad Power Bikes

**Naive (current):** Rad Power Bikes, once a leader in the e-bike market with a valuation of $1.65 billion, has recently undergone significant changes following its acquisition by Life Electric Vehicles for $13.2 million after filing for Chapter 11 bankruptcy. This transition presents a unique opportunity for potential customers and existing riders to engage with a revitalized brand that is committed to enhancing product quality and customer support. With plans to relocate assembly to the U.S. and a focus on improving warranty services, Rad Power Bikes aims to rebuild trust and expand its retail presence, making it an exciting time to consider their innovative e-bike offerings as they emerge from a challenging period in the micromobility sector.

**Ours (current):** Rad Power Bikes is making a strong comeback in 2026 after being acquired by Life Electric Vehicles, which is revitalizing the brand with plans for domestic assembly and expanded retail operations. With over 600,000 bikes sold, Rad continues to lead the affordable utility e-bike market, offering innovative models like the Radster Road, which boasts a powerful 100 Nm torque-sensor motor and a 720Wh battery capable of 53 real-world miles on a single charge. This is the perfect time to invest in a Rad bike, as the new ownership is committed to enhancing customer support and ensuring quality, making it an ideal choice for commuters and families alike.

### Forward (the primary care startup)

**Naive (current):** Forward Health aimed to revolutionize primary care with its innovative CarePods, self-service AI kiosks designed to provide diagnostic services without the need for a clinician. However, despite raising over $657 million and achieving a billion-dollar valuation, the company abruptly shut down in November 2024 after failing to scale its ambitious vision. The closure highlights the critical need for a human element in healthcare, as patients ultimately seek personal connections and trust in their care, which Forward's technology-first approach could not adequately provide. This presents a unique opportunity for healthcare providers to learn from Forward's experience and focus on integrating technology to enhance, rather than replace, the human touch in patient care.

**Ours (other):** Forward Health is revolutionizing primary care by merging technology with personalized healthcare, offering a unique membership model that prioritizes long-term health outcomes over short-term fixes. With a recent $225 million funding boost, Forward is set to expand its innovative approach across the U.S., leveraging AI and biometric assessments to tailor care to individual needs, ensuring that patients receive proactive support rather than reactive treatment. This model not only enhances patient experience but also aligns healthcare incentives with the well-being of the individual, making it a compelling choice for those seeking a more effective and engaging healthcare solution.

### Notion

**Naive (current):** With Notion's recent transformation into a hub for AI agents, now is the perfect time for startups to leverage its capabilities to streamline workflows and enhance productivity. The introduction of the Developer Platform allows teams to integrate custom and external agents, enabling automated workflows that can pull data from various sources, thus reducing tool sprawl and chaos. As Notion prepares for the shutdown of Notion Mail, founders can benefit from centralizing their operations within a single workspace that not only captures knowledge but also interprets and routes tasks efficiently. This shift positions Notion as an essential tool for any startup looking to optimize their processes and maintain a competitive edge in a rapidly evolving landscape.

**Ours (current):** With Notion's recent pivot towards becoming a comprehensive AI workspace, now is the perfect time for startups to leverage its capabilities to streamline operations and enhance productivity. As Notion prepares to shut down its Mail feature on September 22, 2026, founders must act quickly to export essential workflows and embrace Notion as their central hub for knowledge management and decision-making. By utilizing Notion's powerful tools for organizing documents, tasks, and team collaboration, startups can transform scattered information into actionable insights, ensuring they remain agile and competitive in a rapidly evolving landscape.

### 80 Acres Farms

**Naive (current):** Despite the recent closure of 80 Acres Farms, which has been a pioneer in vertical farming, the potential for innovation in this sector remains vast. With a decade of experience and a proven track record of supplying fresh produce to over 18,000 retail locations, 80 Acres has demonstrated that vertical farming can operate at scale. This legacy can serve as a foundation for future ventures that learn from past challenges, particularly in securing sustainable funding and optimizing operational efficiencies. As the industry evolves, there is an opportunity for new players to build on the groundwork laid by 80 Acres, focusing on niche markets and innovative technologies to redefine urban agriculture.

**Ours (current):** In light of the recent closure of 80 Acres Farms, a pioneer in vertical farming that supplied fresh produce to over 18,000 retail locations, we at [Your Company] recognize the urgent need for innovative solutions in sustainable agriculture. With the challenges faced by large-scale operations, we offer tailored partnerships that focus on efficiency, quality, and sustainability, ensuring that your farm can thrive in today's competitive landscape. Let's work together to redefine the future of farming and continue the legacy of providing fresh, clean produce to communities across the nation.

### Limitless (formerly Rewind)

**Naive (current):** With the recent acquisition of Limitless by Meta, the landscape of AI wearables has shifted dramatically, leaving Plaud as the sole independent option for consumers seeking innovative recording technology. Unlike Limitless, which has ceased sales and will only support existing users for a limited time, Plaud continues to thrive, offering a range of devices that not only capture audio but also provide robust transcription services without the risk of obsolescence. As the market consolidates under big tech, choosing Plaud means investing in a future-proof solution that prioritizes user autonomy and privacy, ensuring that your data remains yours, free from the constraints of corporate acquisitions.

**Ours (current):** With the recent acquisition of Limitless by Meta, the landscape of AI wearables has shifted dramatically, leaving many users of the now-discontinued Limitless Pendant seeking alternatives. As the only independent wearable still available, Plaud offers a compelling solution for those looking for a reliable and privacy-focused device. Unlike Limitless, which has ceased sales and will only support existing users for a limited time, Plaud continues to innovate and provide robust features, including a free Starter plan with 300 transcription minutes monthly. This makes Plaud not just a viable alternative, but a forward-thinking choice for users who value independence and ongoing support in their AI wearables. Don't miss out on the opportunity to secure a device that prioritizes your needs and privacy in a rapidly evolving tech landscape.

### Plenty (the vertical farming company)

**Naive (current):** Plenty is revolutionizing the agricultural landscape with its cutting-edge vertical farming technology, recently highlighted by the opening of the world's first large-scale indoor strawberry farm in Richmond, Virginia. This innovative facility not only promises to produce over 4 million pounds of strawberries annually but also exemplifies a commitment to sustainability by utilizing advanced AI and automation to ensure peak-season flavor year-round. As we emerge from a restructuring phase, our focused strategy on premium strawberries positions us to meet the growing demand for fresh, locally-grown produce while minimizing environmental impact. Join us in shaping the future of food with Plenty's unparalleled farming solutions.

**Ours (current):** Plenty Unlimited Inc. has recently emerged from Chapter 11 bankruptcy with a renewed focus on vertical strawberry farming, positioning itself as a leader in sustainable agriculture. With the backing of significant investors like Walmart, who is investing in Plenty to enhance its fresh produce offerings, the company is set to revolutionize the market by providing pesticide-free, peak-flavor strawberries year-round. This strategic pivot not only strengthens Plenty's operational efficiency but also aligns with the growing consumer demand for fresh, locally sourced produce, making it an ideal time for retailers and partners to collaborate with Plenty as they expand their innovative farming technology.

### Northvolt

**Naive (other):** In light of recent developments, Northvolt's legacy is being revitalized under the leadership of Lyten, which has acquired key assets including the Northvolt Ett gigafactory and plans to establish a robust industrial hub in Skellefteå. With a focus on lithium-sulfur battery technology and a commitment to sustainability, Lyten aims to deliver commercial cell production by the second half of 2026, creating over 600 jobs and potentially restoring confidence in European battery manufacturing. This transition presents a unique opportunity for investors and partners to engage with a restructured entity poised to meet the growing demand for green energy solutions in the automotive sector.

**Ours (other):** Northvolt is poised to revolutionize the electric vehicle battery market with its ambitious plans to build new factories in Europe and North America, backed by a recent $1.2 billion funding round. This investment not only underscores the confidence major players like Blackstone and Canadian pension funds have in Northvolt's vision but also highlights its commitment to sustainable energy solutions. As the demand for electric vehicles surges, Northvolt's innovative battery technology and strategic expansions position it as a key player in the green economy, ready to meet the needs of leading automotive manufacturers like BMW and Volkswagen. Join us in this exciting journey towards a sustainable future with Northvolt's cutting-edge battery solutions.

### Tools for Humanity (World)

**Naive (stale):** Tools for Humanity is revolutionizing digital identity verification with its newly launched World ID system, designed to combat the rise of AI-generated scams and impersonations. By utilizing advanced biometric technology through its innovative Orb device, users can securely prove their humanity and gain access to a range of services, including partnerships with major platforms like Zoom and Tinder. This initiative not only enhances user trust in digital interactions but also positions Tools for Humanity as a leader in the fight against online fraud, making it an essential tool for anyone navigating the increasingly complex digital landscape.

**Ours (other):** Tools for Humanity is revolutionizing the way we verify human identity in an increasingly digital world. With the recent launch of their iris-scanning technology in major U.S. cities, participants can now prove their humanity and receive cryptocurrency rewards, all while contributing to a secure and decentralized identity system. This innovative approach not only addresses the growing concerns over AI-generated fake accounts but also empowers individuals with a unique digital identity through the World app. Join us in shaping the future of identity verification and financial inclusion today!

### Lattice (the HR software company)

**Naive (other):** Lattice is revolutionizing performance management by integrating AI-driven insights into everyday workflows, ensuring that managers have real-time access to performance data when they need it most. With the recent acquisition of Pando and the launch of Lattice MCP, the platform is positioned to transform traditional performance reviews into meaningful conversations, enhancing employee development and engagement. As organizations face a growing need for continuous feedback and real-time performance tracking, Lattice stands out as the go-to solution for HR leaders looking to bridge the gap between AI capabilities and actual workforce performance. Join the movement towards a more effective and engaging performance management system with Lattice, where people and AI succeed together.

**Ours (other):** As Lattice pivots to focus solely on performance management following the discontinuation of its HRIS and payroll products, now is the perfect time for organizations to reassess their HR strategies. With Lattice's robust capabilities in structured reviews, goal tracking, and engagement surveys, companies can enhance their performance management processes while integrating specialized tools for other HR functions. This strategic shift not only streamlines operations but also allows businesses to leverage Lattice's strengths in performance management alongside dedicated solutions for payroll and leave management, ensuring a comprehensive and efficient HR ecosystem.

### Scale AI

**Naive (other):** With the recent appointment of Francis deSouza as CEO and a significant $500 million contract from the Pentagon, Scale AI is poised to redefine the landscape of AI applications in both military and enterprise sectors. As a leader in providing essential data infrastructure and AI solutions, Scale AI is uniquely positioned to support organizations in making critical decisions with reliability and speed. This is an opportune moment for potential partners to leverage Scale's expertise and innovative technologies to enhance their own AI capabilities and operational efficiency.

**Ours (other):** Scale AI is at the forefront of transforming AI infrastructure, recently securing a $500 million contract with the Pentagon and expanding its role in military applications, including the development of advanced AI agents for the U.S. Air Force's E-4C doomsday plane. With a projected revenue exceeding $1 billion in 2026, Scale AI is not just a data labeling company but a leader in enterprise and government AI solutions, making it an ideal partner for organizations looking to leverage cutting-edge AI technology for critical decision-making. Let's discuss how Scale AI can help your organization harness the power of AI for strategic advantage.

