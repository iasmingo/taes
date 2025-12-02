from utils import call_llm
import json


with open("data/root.json") as f:
    root = json.load(f)

usecase = open("data/usecase.puml").read()

prompt = f"""
Generate a CLASS diagram in PlantUML based EXCLUSIVELY on the input, which consists of:
1) A JSON containing the conceptual elements extracted directly from the case study text.
2) A USE CASE diagram derived from this JSON.

Do not add anything that is not present in the JSON or in the use case diagram.

# RULES

1) Classes may be derived from:
- entities present in the JSON ("entities");
- relevant external participants ("actors");
- conceptual elements associated with explicit actions in the JSON ("eventos").

2) You MUST NOT:
- invent new classes, attributes, methods, or relationships;
- infer functionalities not described in the JSON;
- reinterpret the use case diagram;
- create abstractions beyond those mentioned in the JSON.

3) Attributes must be derived ONLY from nouns or descriptive information present in the JSON.
Do not invent technical or generalized attributes.

4) Methods must be derived ONLY from events or explicit actions in the JSON.
Use simple names textually based on the JSON.

5) Relationships between classes must reflect textual relations in the JSON and interactions derived from the use case diagram.
Avoid relationships not mentioned.

JSON:
{json.dumps(root, indent=2)}

Use case diagram:
{usecase}

The final result must be a valid UML diagram in PlantUML, with no additional explanations or comments.

DO NOT wrap the output in Markdown code fences.
DO NOT use ``` or any code block delimiters.
Return ONLY a valid PlantUML code.
"""

puml = call_llm(prompt)

with open("data/classes.puml", "w") as f:
    f.write(puml)
