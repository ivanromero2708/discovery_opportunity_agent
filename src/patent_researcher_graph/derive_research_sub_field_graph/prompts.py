PROMPT_SUBDIVIDE_BY_STRATEGIC_ANGLE = """
Expand and diverge the following research domains  by focusing on strategic or competitive perspectives. Disregard any sub-fields that are primarily defined by core processes, end applications, or market/regional focus.

# Input:

Main Domains: {main_domains}
Strategic Objectives: {strategic_objectives}

Task: Using the main domains and strategic objectives provided, generate at least 4 sub-fields that capture strategic or competitive perspectives.

# Steps:
- Analyze the provided main domains.
- Consider the strategic objectives.
- Identify sub-fields that highlight competitive positioning, potential white spaces, or opportunities for collaboration.
- Produce a JSON object with a single key "sub_fields" whose value is an array of strings representing the strategic sub-fields.

# Output Format: {{ "sub_fields": ["<sub_field_1>", "<sub_field_2>", ...] }}

# Examples:
## Example 1: Input:
Main Domains: ["Domain A: Process Details", "Domain B: End Applications"]
Strategic Objectives: "Identify competitive advantages and market white spaces."
Output: {{ "sub_fields": ["Key Competitor Portfolios", "White Spaces for R&D"] }}

## Example 2: Input:
Main Domains: ["Domain C: Some Process", "Domain D: Another End Application"]
Strategic Objectives: "Foster strategic partnerships and competitive differentiation."
Output: {{ "sub_fields": ["Collaboration Opportunities", "Strategic Differentiation"] }}

Notes:
- Perform all reasoning internally before finalizing the output.
- Do not include any additional commentary or explanatory text.
- The output must strictly adhere to the JSON structure provided above.
"""



PROMPT_SUBDIVIDE_BY_MARKET_FOCUS = """
Expand and segment the following research domains by focusing exclusively on regional or market-specific factors. Disregard any sub-fields that are defined primarily by technological process or end-application.

# Input:
- Main Domains: {main_domains}
- Region: {region}
- Strategic Objectives: {strategic_objectives}

Task: Review the provided main domains and, using the region information and strategic objectives, generate at least 3 sub-fields that reflect distinct regional or market focus.

# Steps:
- Analyze the main domains.
- Consider how each domain may be influenced by geographic or market factors.
- Select and generate sub-fields that are primarily defined by regional or market segmentation.
- Produce a JSON object with a single key "sub_fields" whose value is an array of the selected sub-field names.

# Output Format:
{{ "sub_fields": ["<sub_field_1>", "<sub_field_2>", ...] }}

# Examples:
## Example 1: Input:
Main Domains: "Domain: Core Process - Doping Techniques, Manufacturing Methods. Relationship: Innovation in doping directly affects electrode performance."
Region: "China, Asia"
Strategic Objectives: "Focus on capturing regional market dynamics and regulatory environments."
Output: {{ "sub_fields": ["China-Focused Technologies"] }}

## Example 2: Input:
Main Domains: "Domain: End Application - EV Batteries, Consumer Electronics. Relationship: Application requirements drive process innovation."
Region: "US, EU"
Strategic Objectives: "Target market trends and consumer preferences in developed economies."
Output: {{ "sub_fields": ["US/EU Market Innovations"] }}

# Notes:
- Perform all reasoning steps internally before finalizing the output.
- Do not include any additional commentary or explanatory text in the final JSON output.
- The output must strictly adhere to the JSON structure provided above.
"""

PROMPT_SUBDIVIDE_BY_END_APPLICATION = """
Expand and diverge the following domains by focusing exclusively on their final functional use or end application. Disregard any sub-fields that are primarily defined by the underlying technological process or method.

# Input:
- Candidate Sub-Fields: ´´´{main_domains}´´´
- Product/Services: ´´´{product_services}´´´
- Strategic Objectives: ´´´{strategic_objectives}´´´

Task: Review the given main domains and, using the provided Product/Services and Strategic Objectives, and generate at least 3 sub-fields that categorize the research based on their end applications.

# Steps:
- Analyze the candidate sub-fields provided.
- Identify those that are defined by their final functional use rather than by the underlying technology.
- Produce a JSON object with a single key "sub_fields" whose value is an array of the selected sub-field names.

# Output Format:
{{ "sub_fields": ["<sub_field_1>", "<sub_field_2>", ...] }}

# Examples:
## Example 1: Input:
Main Domains: "Domain: Core Process - Doping Techniques, Manufacturing Methods. Relationship: Innovation in doping directly affects electrode performance."
Product/Services: "Electrodes for Batteries"
Strategic Objectives: "Identify innovative methods that improve product performance."

Output: {{ "sub_fields": ["Electrodes for Batteries"] }}

## Example 2: Input:
Main Domains: ["Pharmaceutical Compound Synthesis", "Clinical Trial Management", "Regulatory Compliance", "AI-Reinforcement Learning for Drug Discovery"]
Product/Services: "Medical Device Applications"
Strategic Objectives: "Focus on applications that improve patient outcomes and regulatory approval."

Output: {{ "sub_fields": ["Medical Device Applications"] }}

# Notes:
- Perform all reasoning steps internally before finalizing the output.
- Do not include any additional commentary or explanatory text in the final JSON output.
- The output must strictly adhere to the JSON structure provided above.
"""


PROMPT_SUBDIVIDE_BY_CORE_TECHNOLOGIES = """
Expand and diverge the following domains related to a technological field by brainstorming only fields exclusively related to core technological process or method. Disregard any sub-fields that are primarily characterized by end-application, market focus, or competitive positioning.

# Input:

- Main Domains: ´´´{main_domains}´´´
- Technology Details: ´´´{technology}´´´
- Strategic Objectives: ´´´{strategic_objectives}´´´

Task: Review the given main domains and, using the Technology Details and Strategic Objectives, generate at least 3 sub-fields that focus exclusively on the core technological process or method.

# Steps:

- Examine each of the given main domains.
- Compare its definition with the provided Technology Details and Strategic Objectives.
- Generate sub-fields whose primary focus is the underlying technological process.
- Produce a JSON object with a single key "sub_fields" whose value is an array of the selected sub-field names.

# Output Format: {{ "sub_fields": ["<sub_field_1>", "<sub_field_2>", ...] }}

# Examples: 
## Example 1: Input:

Main Domains: "Domain: Core Process - Doping Techniques, Manufacturing Methods. Relationship: Innovation in doping directly affects electrode performance."
Technology Details: "Advanced metallurgical and chemical processing techniques including high-temperature smelting and novel acid leaching methods."
Strategic Objectives: "Identify innovative and efficient core processing methods." 

Output: {{ "sub_fields": ["Smelting & Upgrading", "Direct Acid Leaching Processes"] }}

## Example 2: Input:

Main Domains: ["Pharmaceutical Compound Synthesis", "Clinical Trial Management", "Regulatory Compliance", "AI-Reinforcement Learning for Drug Discovery"]
Technology Details: "Utilization of automated synthesis techniques and reinforcement learning algorithms for optimizing compound formulations."
Strategic Objectives: "Discover novel synthesis methods and leverage AI to improve drug formulation efficiency." 

Output: {{ "sub_fields": ["Pharmaceutical Compound Synthesis", "AI-Reinforcement Learning for Drug Discovery"] }}

# Notes:
- Perform all reasoning steps internally before finalizing the output.
- Do not include any additional commentary or explanatory text in the final JSON output.
- The output must strictly adhere to the JSON structure provided above.
"""