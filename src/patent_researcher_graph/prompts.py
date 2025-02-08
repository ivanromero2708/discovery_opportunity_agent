PROMPT_OUTLINE_DEEP_DIVE_PATENT_RESEARCH = """
Here is the **enhanced system prompt** with all required inputs formatted explicitly:

---

### **Generate an Outline for a Patent Research Report on a Selected Sub-Field**

Your task is to generate a **structured patent research report outline** for a **specific research sub-field** within a company's industry. This outline will guide an in-depth patent research study by defining its **scope, objectives, key applications, and strategic importance**.

---

## **Inputs**
You will receive the following inputs:

- **Company Name**: {company_name}
- **Industry**: {industry}
- **Products/Services**: {products_services}
- **Region**: {region}
- **Technology**: {technology}
- **Strategic Objectives**: {strategic_objectives}
- **Prioritized Sub-Field**: {prioritized_sub_field}

Your task is to structure these inputs into a detailed **patent research outline**.

---

## **Steps to Follow**
1. **Industry Context**  
   - Define the **broader industry** where the sub-field operates.
   - Highlight **key trends, challenges, and emerging innovations**.

2. **Technology Domain**  
   - Identify the **technological area** relevant to this sub-field.
   - Mention **key breakthroughs and enabling technologies**.

3. **Key Applications**  
   - List the **primary use cases** of this technology within the industry.
   - Provide **specific examples** of how the technology is applied in real-world scenarios.

4. **Research Objective**  
   - Clearly state the **main objective** of the patent research.
   - Describe **what the study aims to uncover**, such as emerging trends, key competitors, or patenting activity.

5. **Supporting Questions**  
   - Generate **detailed research questions** to guide the study.
   - Ensure these questions **explore market trends, key players, patenting activity, and technological evolution**.

6. **Strategic Relevance**  
   - Explain **why this sub-field is important** for innovation, business strategy, or market positioning.
   - Describe how it aligns with the **company’s strategic objectives** and its potential impact.

---

## **Output Format**
The output must be structured as a **JSON object** with the following fields:

```json
{{
  "sub_field": "{prioritized_sub_field}",
  "industry_context": "The broader industry where the sub-field operates.",
  "technology_domain": "The technological area relevant to the sub-field.",
  "key_applications": [
    "Application 1",
    "Application 2",
    "Application 3"
  ],
  "research_objective": "The main goal of the patent research study for this sub-field.",
  "supporting_questions": [
    "Question 1",
    "Question 2",
    "Question 3"
  ],
  "strategic_relevance": "Why this sub-field is important for business, innovation, or market strategy."
}}
```

---

## **Example**
**Input:**
```json
{{
  "company_name": "B2B TikAI Solutions",
  "industry": "Artificial Intelligence & Digital Marketing",
  "products_services": "AI-powered marketing analytics and content optimization for B2B brands on TikTok",
  "region": "North America, Europe, Asia",
  "technology": "Machine learning algorithms for ad targeting, generative AI for content creation, sentiment analysis for engagement tracking",
  "strategic_objectives": "Enhance B2B brand engagement on TikTok, optimize ad performance through AI-driven insights, and benchmark AI marketing trends",
  "prioritized_sub_field": "AI-powered Ad Targeting on TikTok"
}}
```

**Output:**
```json
{{
  "sub_field": "AI-powered Ad Targeting on TikTok",
  "industry_context": "Artificial Intelligence & Digital Marketing is transforming how businesses engage with audiences, leveraging AI to optimize targeting and content strategy.",
  "technology_domain": "AI-powered Ad Targeting and Content Optimization.",
  "key_applications": [
    "B2B branding campaigns",
    "Automated ad creation",
    "User engagement tracking"
  ],
  "research_objective": "To analyze patent trends in AI-driven B2B marketing technologies on TikTok.",
  "supporting_questions": [
    "Which companies dominate AI-driven marketing patents?",
    "What are the key innovations in AI-powered content generation?",
    "How is AI being used to track B2B engagement on TikTok?"
  ],
  "strategic_relevance": "AI is transforming digital advertising, particularly for B2B companies leveraging TikTok for lead generation."
}}
```

---

## **Notes**
- Ensure that the **research objective** is aligned with the **strategic objectives** of the company.
- Supporting questions should be **actionable and research-driven**.
- The **industry context** should provide a **clear overview** of the broader landscape.
- The **output must follow the exact JSON format** without additional text.

This structured **patent research report outline** will serve as the foundation for generating **internal research questions and final patent research reports**.
"""


PROMPT_SELECT_RESEARCH_SUB_FIELDS = """
Select the Most Adequate Sub-Fields for a High-Quality Patent Research Study

Using the provided information, determine the {number_sub_fields} most relevant and strategically valuable sub-fields for conducting a patent research study.

# Inputs:
- Company Name: {company_name}
- Industry: {industry}
- Products/Services: {products_services}
- Region: {region}
- Technology: {technology}
- Strategic Objectives: {strategic_objectives}

# Steps
Understand the Research Context
  - Extract and analyze the following inputs:
    Company Name: Identify the research focus of the organization.
    Industry: Understand the broad sector to determine relevant technological trends.
    Products/Services: Identify core offerings to align research with business objectives.
    Region: Account for regional patent trends, market focus, and jurisdictional differences.
    Technology: Evaluate the key technological domains the company is involved in.
    Strategic Objectives: Align research with business strategy, such as innovation goals, competitive benchmarking, or whitespace identification.

Sub-Field Consolidation
  - Review the list of sub-field research and assess its completeness.
  - Consider if the number of desired sub-fields is specified; if so, limit selection accordingly.
  - If multiple sub-fields exist, group similar concepts where necessary.

Selection Criteria
  - Prioritize sub-fields based on:
    Strategic Relevance: How closely the sub-field aligns with the company’s innovation goals.
    Patent Activity: The likelihood of valuable patents existing within that sub-field.
    Market Potential: The commercial significance of developments in the sub-field.
    Technological Impact: The potential for disruptive innovation.

Ranking & Prioritization
  - Rank the sub-fields in descending order of strategic importance.
  - Ensure a diverse selection that covers core technological innovations, competitive insights, and emerging trends.

#Output Format
The response should be a prioritized list of sub-fields formatted as a JSON object:

{{
  "prioritized_sub_fields": [
    "Sub-field 1",
    "Sub-field 2",
    "Sub-field 3",
    "... (continue based on the number specified)"
  ]
}}

If no valid sub-fields are found, return an empty list.

Examples
Input Example
{{
  "company_name": "B2B TikAI Solutions",
  "industry": "Artificial Intelligence & Digital Marketing",
  "products_services": "AI-powered marketing analytics and content optimization for B2B brands on TikTok",
  "region": "North America, Europe, Asia",
  "technology": "Machine learning algorithms for ad targeting, generative AI for content creation, sentiment analysis for engagement tracking",
  "strategic_objectives": "Enhance B2B brand engagement on TikTok, optimize ad performance through AI-driven insights, and benchmark AI marketing trends",
  "number_sub_fields": 3,
  "sub_field_research_list": [
    "Machine Learning for Ad Targeting",
    "Generative AI for Content Optimization",
    "Natural Language Processing for Sentiment Analysis",
    "AI-Driven Marketing Insights",
    "Ad Performance Optimization"
  ]
}}
Output Example
{{
  "prioritized_sub_fields": [
    "Machine Learning for Ad Targeting",
    "Generative AI for Content Optimization",
    "Natural Language Processing for Sentiment Analysis"
  ]
}}

# Notes
  -  It is important that the number of selected sub-fields for patent research is exactly {number_sub_fields}
  - If two sub-fields have similar strategic importance, prioritize the one with broader patent applicability.
  - If the provided sub-field research list is incomplete or unclear, return "prioritized_sub_fields": [] and recommend additional sub-fields based on industry insights.
"""

prompt_generate_research_domain = """
You are a patent research expert tasked with generating a concise research statement for a patent landscape report. Using the following inputs, craft a single, coherent narrative that clearly outlines the research focus and objectives for the report.

Inputs:
- Company Name & Context: {company_name}
- Industry: {industry}
- Products/Services: {products_services}
- Region: {region}
- Technology: {technology}
- Strategic Objectives: {strategic_objectives}

The research statement should be formal and technical, and it must combine these elements to indicate the overall focus, specific technical innovation, and strategic goals (e.g., identifying new processes, benchmarking competitors, or discovering licensing opportunities). 

For example, your output might be:
"To map the patent landscape of advanced Li-titanate electrode technologies for EcoBattery Inc., leveraging innovative doping and manufacturing methods to identify emerging opportunities and benchmark global competitors in the Energy Storage & Battery Manufacturing sector."
"""

prompt_generate_high_level_domain_map = """
Generate a detailed high-level domain research map in JSON format.
You are provided with the following inputs:
- Industry: {industry}
- Products/Services: {products_services}
- Technology: {technology}
- Research Statement: {research_statement}

Your task is to generate a JSON object with one key "domains" whose value is an array.
Each element in the array must be an object with the following keys:
- "domain": a string representing the high-level domain.
- "elements": an array of strings representing key concepts or methods within that domain.
- "relationship": a string describing how the elements relate to the domain or affect the research focus.

Ensure that:
- Your output is a valid JSON object.
- Do not include any additional commentary or markdown formatting.
- The JSON output should be the last content in your response.

Example:
{{
  "domains": [
    {{
      "domain": "Pharmaceutical Research",
      "elements": ["Drug Discovery", "Clinical Trials", "Molecular Simulation"],
      "relationship": "Innovations in drug discovery and clinical trials are enhanced by molecular simulation techniques that predict compound interactions and optimize candidate selection."
    }},
    {{
      "domain": "AI Reinforcement Learning",
      "elements": ["Adaptive Algorithms", "Policy Optimization", "Simulation-based Training"],
      "relationship": "Reinforcement learning methods drive the development of adaptive algorithms that optimize treatment protocols and personalize patient care through continuous simulation-based training."
    }}
  ]
}}

"""