from utils import call_llm
import json


with open("data/root.json") as f:
    root = json.load(f)

usecase = open("data/usecase.puml").read()
classes = open("data/classes.puml").read()

prompt = f"""
Consider the following use case scenario (for use case “place order”):
Use case scenario — “place order”:
Ali is an existing customer of the order processing company described earlier, registered with their website. Also assume that, having browsed the printed catalogue he owns, he has already identified the two items (including their prices) he wants to buy from the company’s website using their product numbers (i.e., #2 and #9).
First, he tries to buy one unit of product #2, but it is listed as unavailable in the inventory.
Then, he adds two units of product #9, which turns out to be available, to his basket.
He is then asked to confirm his registered shipping and billing addresses and credit card information from the customer database.
He completes the order by clicking the Submit button.
You may ignore customer authentication processing.

Generate a SEQUENCE diagram in PlantUML based EXCLUSIVELY on the above scenario and the input, which consists of:

1) A JSON containing the conceptual elements extracted directly from the case study text.
2) A USE CASE diagram derived from this JSON.
3) A CLASS diagram derived from the use case and the JSON entities.

The sequence diagram must reflect:
- the functional flow indicated by the USE CASE diagram;
- the possible interactions defined by the classes, methods, and relationships in the CLASS diagram;
- the textual relationships and events present in the JSON;
- and the event flow described in the scenario above.

# RULES

1) Do not create new actors, classes, objects, or entities.
Use ONLY the elements present in the inputs.

2) Do not invent methods.
Use ONLY the methods already present in the class diagram.

3) Do not create messages, operations, or interactions that are not compatible with the:
- JSON,
- use case diagram,
- class diagram, or
- scenario text.

4) The sequence must represent a coherent flow that:
- begins with the main actor of the use case;
- follows the actions textually mentioned in the scenario and JSON;
- uses valid methods from the classes.

5) Preserve all names exactly as they appear.

JSON:
{json.dumps(root, indent=2)}

Use case diagram:
{usecase}

Class diagram:
{classes}

The final result must be a valid UML diagram in PlantUML, with no additional explanations or comments.

DO NOT wrap the output in Markdown code fences.
DO NOT use ``` or any code block delimiters.
Return ONLY a valid PlantUML code.
"""

puml = call_llm(prompt)

with open("data/sequence.puml", "w") as f:
    f.write(puml)