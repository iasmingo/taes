from utils import call_llm
from scoring import generate_report
import json


with open("data/root.json") as f:
    root = json.load(f)

usecase = open("data/usecase.puml").read()
classes = open("data/classes.puml").read()
sequence = open("data/sequence.puml").read()

prompt = f"""
You are a FORMAL CONSISTENCY VERIFIER for UML models.

Your task is to identify and categorize ALL inconsistencies between artifacts.
DO NOT evaluate severity - just report what you find objectively.

# ARTIFACTS TO ANALYZE

The pipeline consists of:
1) A JSON extracted from case study text
2) A USE CASE DIAGRAM derived from JSON
3) A CLASS DIAGRAM derived from JSON + use case
4) A SEQUENCE DIAGRAM derived from JSON + classes + use case

# RULES

You MUST:
- Report ONLY literal inconsistencies found
- Use EXACTLY the error types specified below
- Count ALL elements accurately
- NOT assume, infer, or fill gaps

You MUST NOT:
- Correct diagrams
- Propose improvements
- Create missing information
- Assume semantic equivalence

# ERROR TYPES YOU CAN REPORT

For json_vs_usecase:
- "missing_actor": Actor from JSON not in use case
- "extra_actor": Actor in use case not in JSON
- "missing_usecase": Event from JSON not mapped to use case
- "extra_usecase": Use case not in JSON events

For json_vs_classes:
- "missing_entity": Entity from JSON not as class
- "extra_class": Class not in JSON entities
- "missing_relation": JSON relation not in class diagram
- "missing_method": JSON event not mapped to method

For json_vs_sequence:
- "missing_participant": Actor/Entity not in sequence
- "extra_participant": Participant not in JSON
- "missing_message": Event not as message
- "wrong_message_order": Order contradicts JSON

For usecase_vs_classes:
- "usecase_not_mapped": Use case without method
- "method_without_usecase": Method without use case

For classes_vs_sequence:
- "lifeline_without_class": Lifeline without class
- "message_without_method": Message without method
- "incompatible_flow": Flow incompatible with classes

# OUTPUT FORMAT

Return ONLY valid JSON:

{{
  "json_vs_usecase": {{
    "status": "OK" or "ERROR",
    "errors": [
      {{
        "type": "one of the types above",
        "element": "element name",
        "details": "brief description"
      }}
    ],
    "counts": {{
      "total_actors_json": number,
      "found_actors_usecase": number,
      "total_events_json": number,
      "found_usecases": number
    }}
  }},
  "json_vs_classes": {{
    "status": "OK" or "ERROR",
    "errors": [...],
    "counts": {{
      "total_entities_json": number,
      "found_classes": number,
      "total_relations_json": number,
      "found_relations": number
    }}
  }},
  "json_vs_sequence": {{
    "status": "OK" or "ERROR",
    "errors": [...],
    "counts": {{
      "total_participants_expected": number,
      "found_participants": number,
      "total_events_json": number,
      "found_messages": number
    }}
  }},
  "usecase_vs_classes": {{
    "status": "OK" or "ERROR",
    "errors": [...],
    "counts": {{
      "total_usecases": number,
      "found_methods": number
    }}
  }},
  "classes_vs_sequence": {{
    "status": "OK" or "ERROR",
    "errors": [...],
    "counts": {{
      "total_lifelines": number,
      "valid_lifelines": number,
      "total_messages": number,
      "valid_messages": number
    }}
  }},
  "overall_status": "OK" or "ERROR"
}}

# ARTIFACTS

JSON:
{json.dumps(root, indent=2)}

Use case diagram:
{usecase}

Class diagram:
{classes}

Sequence diagram:
{sequence}

Return ONLY the JSON. No markdown, no code fences.
"""

output = call_llm(prompt)

# Salvar verificação bruta
with open("data/report.json", "w") as f:
    f.write(output)

# Calcular scores e gerar relatório completo
verification_result = json.loads(output)
generate_report(verification_result, "data/score_report.json")