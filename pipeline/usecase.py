from utils import call_llm
import json


root = json.load(open("data/root.json", "r"))

prompt = f"""
Generate a USE CASE diagram in PlantUML based EXCLUSIVELY on the JSON below.
DO NOT add new elements.

JSON:
{json.dumps(root, indent=2)}

The final result must be a valid UML diagram in PlantUML, with no additional explanations or comments.

DO NOT wrap the output in Markdown code fences.
DO NOT use ``` or any code block delimiters.
Return ONLY a valid PlantUML code.
"""

puml = call_llm(prompt)

open("data/usecase.puml", "w").write(puml)