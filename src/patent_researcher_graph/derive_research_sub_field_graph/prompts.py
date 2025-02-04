

PROMPT_SUBDIVIDE_BY_CORE_TECHNOLOGIES = """
Refine the following candidate research sub-fields by selecting only those that are defined exclusively by their core technological process or method. Disregard any sub-fields that are primarily characterized by end-application, market focus, or competitive positioning.

# Input:

Main Domains: {main_domains}
Technology Details: {technology}
Strategic Objectives: {strategic_objectives}

Task: Review the given main domains and, using the Technology Details and Strategic Objectives, generate sub-fields that focus exclusively on the core technological process or method.

# Steps:

Examine each of the given main domains.
Compare its definition with the provided Technology Details and Strategic Objectives.
Generate sub-fields whose primary focus is the underlying technological process.
Produce a JSON object with a single key "sub_fields" whose value is an array of the selected sub-field names.
Output Format: {{ "sub_fields": ["<sub_field_1>", "<sub_field_2>", ...] }}

# Examples: 
## Example 1: Input:

Candidate Sub-Fields: ["Basic Material Processing", "Smelting & Upgrading", "Direct Acid Leaching Processes", "Advanced Coating Techniques"]
Technology Details: "Advanced metallurgical and chemical processing techniques including high-temperature smelting and novel acid leaching methods."
Strategic Objectives: "Identify innovative and efficient core processing methods." 

Output: {{ "sub_fields": ["Smelting & Upgrading", "Direct Acid Leaching Processes"] }}

## Example 2: Input:

Candidate Sub-Fields: ["Pharmaceutical Compound Synthesis", "Clinical Trial Management", "Regulatory Compliance", "AI-Reinforcement Learning for Drug Discovery"]
Technology Details: "Utilization of automated synthesis techniques and reinforcement learning algorithms for optimizing compound formulations."
Strategic Objectives: "Discover novel synthesis methods and leverage AI to improve drug formulation efficiency." 

Output: {{ "sub_fields": ["Pharmaceutical Compound Synthesis", "AI-Reinforcement Learning for Drug Discovery"] }}

# Notes:
Perform all reasoning steps internally before finalizing the output.
Do not include any additional commentary or explanatory text in the final JSON output.
The output must strictly adhere to the JSON structure provided above.
"""