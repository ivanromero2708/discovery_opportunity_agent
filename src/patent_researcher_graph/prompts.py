

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