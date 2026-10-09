# Sales research: naive vs ours on every company in the case list

Task: "Write a one-paragraph sales outreach angle for {company} based on their latest news."  Query: "{company} news"  n=15 companies, 1 run each. Prices are simulated.
Verdicts are keyword checks (current / stale / other). **Usman: please read the answers below and confirm.**

| | naive (reads 10) | ours |
|---|---|---|
| current | 9 | 7 |
| stale | 2 | 1 |
| other | 4 | 7 |
| pages read | 10.0 | 3.1 |
| tokens per query | 14083 | 19490 (reading 4817 + scoring 14673) |
| cost per query (pages simulated + tokens) | 23.12c | 8.99c |

| company | naive | ours | pages | tokens naive | tokens ours (reading + scoring) | cost naive | cost ours |
|---|---|---|---|---|---|---|---|
| Humane (the AI hardware startup) | current | current | 3 | 13855 | 19664 (5111 + 14553) | 22.28c | 8.83c |
| Builder.ai | current | current | 4 | 15284 | 21512 (5946 + 15566) | 20.69c | 10.71c |
| Windsurf (the AI coding tool company) | current | current | 3 | 18348 | 21414 (5627 + 15787) | 27.65c | 9.90c |
| Figure AI | other | other | 1 | 11686 | 14324 (2037 + 12287) | 18.75c | 2.67c |
| Natron Energy | current | current | 3 | 13596 | 17060 (3136 + 13924) | 24.90c | 9.21c |
| Rad Power Bikes | current | other | 3 | 16037 | 20274 (4839 + 15435) | 24.87c | 9.68c |
| Forward (the primary care startup) | current | current | 4 | 13951 | 20400 (5604 + 14796) | 25.45c | 10.45c |
| Notion | current | other | 4 | 16521 | 22873 (6761 + 16112) | 21.66c | 10.38c |
| 80 Acres Farms | current | current | 3 | 11766 | 18486 (4807 + 13679) | 27.90c | 9.00c |
| Limitless (formerly Rewind) | current | current | 3 | 12693 | 19074 (5471 + 13603) | 20.17c | 8.31c |
| Plenty (the vertical farming company) | stale | stale | 3 | 8337 | 16361 (2539 + 13822) | 24.66c | 9.56c |
| Northvolt | other | other | 4 | 18143 | 23622 (7550 + 16072) | 21.43c | 10.44c |
| Tools for Humanity (World) | stale | other | 4 | 11859 | 18972 (3720 + 15252) | 21.58c | 10.58c |
| Lattice (the HR software company) | other | other | 3 | 16419 | 20621 (5645 + 14976) | 25.22c | 9.45c |
| Scale AI | other | other | 2 | 12746 | 17700 (3462 + 14238) | 19.51c | 5.67c |

## Answers

### Humane (the AI hardware startup)

**Naive (current):** In a landscape where AI hardware startups are struggling to find their footing, Humane's recent acquisition by HP for $116 million serves as a cautionary tale and a unique opportunity. With a founding team of ex-Apple engineers and a vision for a post-smartphone era, Humane aimed to revolutionize personal technology with its AI Pin, a wearable device that promised seamless interaction without screens. However, the product's failure to deliver on its ambitious promises, coupled with a high price point and a subscription model, led to its downfall. As HP integrates Humane's technology into its own products, there's a chance to learn from these missteps and innovate in a way that truly meets consumer needs, potentially paving the way for a new generation of AI-driven devices that prioritize functionality and user experience over hype. Let's discuss how we can leverage these insights to create a more viable and user-friendly AI hardware solution.

**Ours (current):** Despite the recent challenges faced by Humane, including the shutdown of their AI Pin, the company has a unique opportunity to pivot and leverage its innovative technology and experienced team to redefine personal AI hardware. With a strong foundation in AI and a vision for a screenless, voice-driven future, Humane can focus on developing new, user-friendly devices that integrate seamlessly into daily life, potentially capturing the growing market for personal intelligence solutions. By emphasizing their commitment to user-centric design and the lessons learned from past endeavors, Humane can position itself as a leader in the next wave of AI-driven consumer technology.

### Builder.ai

**Naive (current):** Builder.ai, once a promising AI startup backed by major investors like Microsoft, has recently faced a dramatic collapse, revealing the stark reality behind its operations. Initially marketed as a platform that allowed users to create apps with minimal coding through its AI assistant, Natasha, it was later uncovered that the majority of the work was performed by over 700 engineers manually coding applications. This misrepresentation, coupled with inflated revenue claims—reportedly overstating 2024 projections by 300%—led to a liquidity crisis and ultimately, insolvency proceedings in May 2025. As the tech landscape evolves, Builder.ai serves as a cautionary tale about the dangers of 'AI washing' and the importance of transparency in the tech industry. For businesses seeking reliable software solutions, understanding the balance between automation and human involvement is crucial to avoid similar pitfalls.  

For more details, visit: https://rottenwifi.com/builder-ai-collapses-what-its-ai-platform-really-did-and-what-the-700-engineers-claim-gets-wrong, https://economictimes.indiatimes.com/tech/startups/ettech-explainer-why-ai-startup-builder-ai-is-filing-for-bankruptcy-despite-backing-from-microsoft-and-qia/printarticle/121337666.cms, https://system7.ai/news/builder-ai-collapse-ai-washing-case-study

**Ours (current):** Builder.ai, once a promising AI startup backed by major investors like Microsoft, has recently faced significant challenges, culminating in its insolvency announcement in May 2025. Despite its initial claims of revolutionizing app development through AI, investigations revealed that the company relied heavily on a large team of engineers rather than the automated systems it marketed. This discrepancy between its promises and operational reality has raised serious concerns about transparency and due diligence in the tech industry. As businesses seek reliable partners for software development, understanding the true capabilities behind AI claims is crucial to avoid the pitfalls exemplified by Builder.ai's collapse.

### Windsurf (the AI coding tool company)

**Naive (current):** With the recent rebranding of Windsurf to Devin Desktop, Cognition has transformed this powerful AI coding tool into a comprehensive IDE that seamlessly integrates local and cloud coding agents. This evolution not only preserves the robust features that made Windsurf popular, such as its agent management capabilities and compatibility with existing workflows, but also enhances them with new functionalities like the Agent Command Center and Spaces for better task organization. For developers looking to streamline their coding processes and leverage advanced AI capabilities, Devin Desktop represents a significant upgrade, ensuring that they remain at the forefront of coding innovation. Don't miss out on the opportunity to elevate your development experience with Devin Desktop today!

**Ours (current):** Windsurf, now rebranded as Devin Desktop, has transformed into a powerful integrated development environment (IDE) that combines local and cloud coding capabilities, making it an essential tool for developers looking to streamline their workflows. Following its acquisition by Cognition, Devin Desktop not only retains the robust features of Windsurf but also introduces an advanced Agent Command Center for managing multiple coding agents seamlessly. With over 350 enterprise customers and a significant revenue growth, Devin Desktop is positioned to enhance productivity and collaboration in coding projects, making it a compelling choice for developers seeking efficiency and innovation in their coding practices.

### Figure AI

**Naive (other):** Figure AI is making headlines with its innovative approach to decommissioning its F.02 humanoid robots, having them autonomously leap into a vat of molten steel in a dramatic farewell inspired by Arnold Schwarzenegger's iconic line from *Terminator 2*. This unique method not only protects the company's proprietary technology but also frees up resources for the development of the next-generation F.04 model. By transforming the remnants into limited-edition commemorative artifacts, Figure AI is turning a necessary disposal into a marketing spectacle, showcasing its commitment to cutting-edge robotics and engaging storytelling. This bold move positions Figure AI as a leader in the robotics industry, blending technology with a touch of cinematic flair.

**Ours (other):** At Figure AI, we are redefining the lifecycle of robotics with our recent dramatic retirement of the F.02 humanoid robots, showcasing our commitment to innovation and proprietary technology protection. By training these robots to autonomously leap into a molten steel furnace, we not only celebrated their achievements but also freed up resources for our next-generation F.03 models and the advanced Helix AI system. This bold move, endorsed by Arnold Schwarzenegger, highlights our ability to blend engineering prowess with captivating storytelling, ensuring that our technology remains at the forefront of the industry while creating unique commemorative artifacts from the process. Join us in this exciting journey as we continue to push the boundaries of robotics and AI.  

Learn more about our latest advancements and the F.02 retirement at [Figure AI](https://www.figure.ai/news/f-02-decommission).

### Natron Energy

**Naive (current):** Despite its recent shutdown, Natron Energy's pioneering sodium-ion battery technology remains a compelling solution for industries seeking safe, high-performance energy storage. With a unique focus on rapid charging, exceptional cycle life, and a non-flammable chemistry, Natron's batteries are designed for critical applications like data centers and industrial power systems. As the only UL-listed sodium-ion batteries on the market, they offer a sustainable alternative to lithium-ion, leveraging abundant materials and reducing supply chain risks. This technology is poised to meet the growing demand for reliable energy solutions in a rapidly electrifying world, making Natron's innovations relevant for future energy storage needs.

**Ours (current):** Despite its recent closure, Natron Energy's pioneering sodium-ion battery technology remains a compelling solution for industries seeking safer, more sustainable energy storage options. With rapid charging capabilities and a cycle life exceeding 50,000 cycles, Natron's batteries are designed for high-demand applications like data centers and electric vehicle fast-charging stations. As the market increasingly prioritizes cost-effective and environmentally friendly alternatives to lithium-ion batteries, Natron's innovative approach using abundant materials like sodium positions it as a leader in the transition to cleaner energy solutions. Companies looking to enhance their energy storage systems should consider the unique advantages of sodium-ion technology, which promises to mitigate supply chain risks and improve operational efficiency.

### Rad Power Bikes

**Naive (current):** Rad Power Bikes, once a leader in the e-bike market, is undergoing a significant transformation under new ownership after its recent acquisition by Life Electric Vehicles for $13.2 million. This transition presents a unique opportunity for potential customers to engage with a revitalized brand that aims to enhance its product offerings and customer support. With plans for U.S.-based assembly and a commitment to improving quality and service, Rad Power is poised to reclaim its position in the market while ensuring that existing customers receive the support they need. Now is the perfect time to consider investing in a Rad e-bike as the brand embarks on this exciting new chapter, promising innovation and reliability.  

For more information, visit: https://techbuzz.ai/articles/life-ev-acquires-rad-power-bikes-in-e-mobility-consolidation, https://everything.explained.today/Rad_Power_Bikes, https://techbuzz.ai/articles/rad-power-bikes-sells-for-13-2m-in-bankruptcy-fire-sale

**Ours (other):** Rad Power Bikes is back and better than ever! After a successful acquisition by Life Electric Vehicles, the brand is set to revitalize its operations with a focus on domestic assembly and enhanced customer support. With a lineup that includes the powerful Radster Road and the innovative RadRunner Max featuring rear traffic radar, Rad is committed to delivering high-quality, affordable e-bikes that cater to every rider's needs. Join the e-bike revolution and experience the reliability and performance that has made Rad a household name in the cycling community. Don't miss out on the latest models and promotions as we gear up for an exciting new chapter!

### Forward (the primary care startup)

**Naive (current):** Forward Health aimed to revolutionize primary care with its innovative CarePods, self-service AI kiosks designed to provide diagnostic services without clinician involvement. However, despite raising over $657 million and achieving a billion-dollar valuation, the company abruptly shut down in November 2024 after failing to scale its ambitious vision. The closure highlights the critical need for a human touch in healthcare, as patients ultimately seek compassionate care rather than automated solutions. For those looking for a more reliable healthcare experience, consider alternatives like One Medical or Carbon Health, which blend technology with essential human interaction.

**Ours (current):** In light of Forward's recent closure, we recognize the challenges faced by innovative healthcare startups in scaling their models effectively. At Forward, the vision was to revolutionize primary care through technology, offering a flat-fee membership for unlimited access to services. However, the ambitious rollout of CarePods, intended to automate care delivery, fell short of expectations, highlighting the complexities of merging healthcare with tech-driven solutions. As we move forward, we invite you to explore how our approach can provide sustainable, patient-centered care without the pitfalls of rapid scaling, ensuring that quality remains at the forefront of healthcare innovation.

### Notion

**Naive (current):** With Notion's recent transformation into a hub for AI agents, now is the perfect time for founders to leverage its capabilities to streamline workflows and enhance productivity. The introduction of the Developer Platform allows teams to build custom agents and automate multi-step workflows, effectively turning Notion into a central orchestrator for all your work processes. As Notion prepares to shut down its Mail feature, it emphasizes the importance of integrating AI-driven solutions that can interpret and manage tasks seamlessly. This shift not only reduces tool sprawl but also positions Notion as a vital operating layer for small teams looking to centralize their knowledge and decision-making processes. Don't miss out on the opportunity to harness this powerful tool to elevate your team's efficiency and collaboration.

**Ours (other):** With Notion's recent pivot towards becoming a comprehensive AI workspace, now is the perfect time for teams to leverage its capabilities for enhanced productivity. As Notion phases out its Mail feature, businesses can focus on integrating their workflows into a more robust system that emphasizes automation and cross-app collaboration. This shift not only streamlines operations but also empowers teams to harness AI agents for repetitive tasks, ensuring that critical information is always at their fingertips. Don't miss the opportunity to transform your workspace into a dynamic hub for innovation and efficiency.

### 80 Acres Farms

**Naive (current):** Despite the recent closure of 80 Acres Farms, which demonstrated the potential of vertical farming by supplying fresh produce to over 18,000 retail locations, the industry is still ripe for innovation and growth. With a decade of experience and advanced technology like the GroLoop farm management platform, there is an opportunity for new ventures to learn from past challenges and capitalize on the demand for sustainable, locally grown food. As the market evolves, partnering with experienced teams can help navigate the complexities of indoor agriculture and drive future success.

**Ours (current):** In light of the recent closure of 80 Acres Farms, a pioneer in vertical farming that supplied fresh produce to over 18,000 retail locations, we at [Your Company Name] see a unique opportunity to step in and fill the gap left in the market. With a proven track record of delivering high-quality, sustainable produce, we are committed to continuing the legacy of innovation and excellence in indoor agriculture. Our advanced farming solutions are designed to optimize efficiency and yield, ensuring that communities continue to have access to fresh, clean food. Let's discuss how we can collaborate to redefine the future of sustainable farming together.

### Limitless (formerly Rewind)

**Naive (current):** With the recent acquisition of Limitless by Meta, the landscape of AI-enabled wearables has shifted dramatically, leaving Plaud as the sole independent option for consumers seeking innovative recording technology. Unlike Limitless, which has ceased hardware sales and will only support existing users for a limited time, Plaud continues to thrive, offering a range of devices that not only capture conversations but also provide robust transcription services without the risk of obsolescence. As the market consolidates under big tech, choosing Plaud means investing in a future-proof solution that prioritizes user autonomy and privacy, ensuring that your data remains yours. Don't miss out on the opportunity to secure a reliable wearable that stands apart from the competition. Explore Plaud today!

**Ours (current):** With Limitless now part of Meta's innovative portfolio, we are excited to offer you a unique opportunity to leverage cutting-edge AI technology that enhances everyday productivity. Our pendant-style device, which seamlessly records and transcribes conversations, is designed to augment your memory and streamline your workflow. As we transition into this new chapter, existing users will enjoy continued support and exclusive benefits, while new customers can explore the future of AI-enabled wearables through Meta's expanding ecosystem. Don't miss out on being part of this revolutionary journey in personal superintelligence!

### Plenty (the vertical farming company)

**Naive (stale):** Plenty Unlimited Inc. is revolutionizing the agricultural landscape with its cutting-edge indoor vertical farming technology, recently highlighted by the opening of the world's first large-scale indoor strawberry farm in Richmond, Virginia. This innovative facility not only promises to produce over 4 million pounds of premium strawberries annually but also exemplifies a commitment to sustainability by utilizing advanced AI and automation to ensure year-round, peak-season flavor. As we focus on expanding our operations and partnerships, we invite you to join us in transforming the future of food production, making fresh, delicious, and pesticide-free produce accessible to everyone, right in the heart of urban communities.

**Ours (stale):** Plenty Unlimited Inc. is revolutionizing the agricultural landscape with its cutting-edge indoor vertical farming technology, recently highlighted by the opening of the world’s first large-scale indoor strawberry farm in Richmond, Virginia. This innovative facility not only promises to deliver fresh, pesticide-free strawberries year-round but also exemplifies a commitment to sustainability by reducing transportation and food waste. With strong backing from investors like Walmart, Plenty is poised to redefine fresh produce accessibility, making it an ideal partner for retailers looking to enhance their offerings with premium, locally grown products. Join us in leading the future of agriculture and ensuring that fresh food is available to everyone, everywhere.

### Northvolt

**Naive (other):** In light of recent developments, Northvolt's legacy is being revitalized under the leadership of Lyten, which has acquired key assets including the Northvolt Ett gigafactory and plans to establish a robust industrial hub in Skellefteå. With a focus on lithium-sulfur technology and a commitment to sustainability, Lyten aims to deliver commercial battery cells by the second half of 2026, creating over 600 jobs in the process. This transition not only preserves Northvolt's vision of a greener battery future but also positions Lyten as a formidable player in the European EV market, ready to meet the growing demand for sustainable energy solutions. Now is the perfect time to engage with Lyten as they embark on this ambitious journey to reshape the battery landscape in Europe and beyond.

**Ours (other):** Despite recent challenges, Northvolt's commitment to sustainable battery production remains strong, especially with the acquisition of its assets by Lyten, which aims to revive operations and establish a European EV battery hub. This transition presents a unique opportunity for investors and partners to engage with a revitalized entity focused on innovative lithium-sulfur technology, promising a greener future in the electric vehicle market. As Northvolt's legacy continues through Lyten, the potential for growth in the European battery sector is significant, making it an attractive proposition for stakeholders looking to invest in sustainable energy solutions.

### Tools for Humanity (World)

**Naive (stale):** In a world increasingly dominated by AI, Tools for Humanity is pioneering a solution to verify human identity through its innovative World ID system, co-founded by Sam Altman. With the recent launch of the World Money app, users can now enjoy a self-custodial financial super app that not only facilitates secure transactions but also integrates biometric verification to combat the rise of AI-generated scams. By partnering with major platforms like Zoom and Tinder, Tools for Humanity is positioning itself as a critical player in ensuring that online interactions are genuine, providing users with peace of mind in an era where distinguishing between humans and bots is becoming more challenging. Join us in shaping a future where your identity is secure and your transactions are seamless, all while enjoying the benefits of a decentralized financial ecosystem.  

For more information, visit: https://ranked.news/are-you-human-new-tool-aims-to-help-prove-youre-not-ai, https://api.finexus.net/api/news/events/c271ffc4-33b7-4d85-87f3-91c3e7f9d1c3/html, https://newsdive.net/2026/04/20/sam-altman-s-world-initiative-aims-to-distinguish-humans-from-bots-for-tinder-and-zoom-users.

**Ours (other):** Tools for Humanity is revolutionizing the way we verify human identity in an increasingly automated world with its innovative iris-scanning technology, now available in major U.S. cities. Backed by Sam Altman, this project not only offers participants a unique opportunity to prove their humanity but also rewards them with cryptocurrency, creating a new paradigm in digital identity verification. As we navigate the complexities of AI and digital interactions, partnering with Tools for Humanity means being at the forefront of a transformative movement that prioritizes authentic human engagement in the digital space.

### Lattice (the HR software company)

**Naive (other):** Lattice is revolutionizing performance management by integrating AI-driven insights into everyday workflows, making it easier for managers to engage with their teams and track progress in real-time. With the recent acquisition of Pando, Lattice is enhancing its capabilities to provide continuous, evidence-based performance tracking, moving away from outdated annual reviews. This strategic shift not only addresses the growing demand for real-time performance data but also positions Lattice as a leader in the AI-native HR landscape, ensuring that organizations can effectively bridge the gap between technology and employee development. Join the future of performance management with Lattice, where people and AI succeed together.

**Ours (other):** Lattice is revolutionizing performance management by integrating AI-driven insights into its platform, following its recent acquisition of Pando, which enhances real-time performance tracking and evidence-based evaluations. This strategic move positions Lattice as a leader in transforming how organizations measure and develop talent, moving away from outdated annual reviews to a continuous feedback model that aligns with the fast-paced changes in today's workforce. With a focus on building a culture where AI supports employee growth, Lattice is not just a tool but a partner in navigating the complexities of modern HR challenges, ensuring that your team thrives in a People + AI world.

### Scale AI

**Naive (other):** With the recent appointment of Francis deSouza as CEO, Scale AI is poised to leverage its substantial $500 million Pentagon contract and its growing enterprise client base, including major players like BP and Mayo Clinic. This leadership transition comes at a pivotal moment as the company expands its role in military AI applications, particularly with the development of agentic AI for the U.S. Air Force's E-4C command aircraft. As Scale AI continues to innovate and provide critical AI infrastructure, now is the perfect time for organizations to partner with a leader in reliable AI solutions that can transform decision-making processes across various sectors.

**Ours (other):** With the recent appointment of Francis deSouza as CEO, Scale AI is poised to lead the next phase of AI innovation, particularly in enterprise and government applications. As the company transitions from its roots in data labeling to becoming a critical player in AI infrastructure, including a significant $500 million contract with the Pentagon, now is the perfect time to partner with Scale AI. Their expertise in developing reliable AI systems for high-stakes decision-making can help organizations harness the power of AI to drive efficiency and effectiveness in their operations.

