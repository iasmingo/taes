from utils import call_llm
import json


with open("data/root.json") as f:
    root = json.load(f)

usecase = open("data/usecase.puml").read()
classes = open("data/classes.puml").read()
sequence = open("data/sequence.puml").read()

prompt = f"""
You are a FORMAL CONSISTENCY VERIFIER for UML models.

Your task is to analyze whether the provided artifacts are CONSISTENT with each other,
following strict and objective rules.

The pipeline consists of:
1) A JSON extracted directly from the case study text;
2) A USE CASE DIAGRAM derived from this JSON;
3) A CLASS DIAGRAM derived from the JSON + use case diagram;
4) A SEQUENCE DIAGRAM derived from the JSON + classes + use case diagram;

You must evaluate consistency between:
- JSON and use case diagram;
- JSON and class diagram;
- JSON and sequence diagram;
- use case diagram and class diagram;
- class diagram and sequence diagram.

# ABSOLUTE RULES FOR THE ANALYSIS

You MUST NOT:
- correct any diagrams;
- fill in gaps;
- rewrite or reformulate content;
- propose improvements;
- infer information not literally present;
- create entities that do not exist in the input;
- assume alternative names or semantic equivalence.

You MUST:
- identify ALL inconsistencies observable strictly from the provided text;
- rely ONLY on the literal content of the artifacts;
- follow the checklist below exactly as written.

# FORMAL CONSISTENCY CHECKLIST

You must verify at least the following:

## JSON and use case diagram
1) All "actors" in the JSON must appear in the use case diagram.
2) The use case diagram must NOT contain actors not present in the JSON.
3) JSON "events" (actions) must correspond to use cases.
4) The use case diagram must NOT introduce actions absent from the JSON.

## JSON and class diagram
1) All JSON "entities" must appear as classes in the class diagram.
2) The class diagram must NOT contain classes not present in the JSON.
3) Methods in the class diagram must derive from JSON "events".
4) Class relationships must correspond to JSON "textual_relations".

## JSON and sequence diagram
1) All sequence diagram participants must exist as actors or entities in the JSON.
2) All messages must correspond to JSON events.
3) The message order and flow must not contradict explicit relations in the JSON.

## Use case diagram and class diagram
1) Each functionality in the use case diagram must map to class-level operations.
2) No class operation may represent behavior absent from the use case diagram.

## Class diagram and sequence diagram
1) All sequence diagram lifelines must correspond to valid classes.
2) All messages must correspond to existing class methods.
3) The flow of the sequence diagram must be compatible with class relations.

# OUTPUT FORMAT (MANDATORY)

Return ONLY a valid JSON with the structure:

curly-brace
  "json_vs_usecase": curly-brace
    "status": "OK" or "ERROR",
    "errors": ["...", "..."]
  curly-brace,
  "json_vs_classes": curly-brace
    "status": "OK" or "ERROR",
    "errors": ["...", "..."]
  curly-brace,
  "json_vs_sequence": curly-brace
    "status": "OK" or "ERROR",
    "errors": ["...", "..."]
  curly-brace,
  "usecase_vs_classes": curly-brace
    "status": "OK" or "ERROR",
    "errors": ["...", "..."]
  curly-brace,
  "classes_vs_sequence": curly-brace
    "status": "OK" or "ERROR",
    "errors": ["...", "..."]
  curly-brace,
  "overall_status": "OK" or "ERROR"
curly-brace

Rule:
- overall_status = "ERROR" if ANY section contains an error.

# ANALYZE THE FOLLOWING ARTIFACTS:

JSON:
{json.dumps(root, indent=2)}

Use case diagram:
{usecase}

Class diagram:
{classes}

Sequence diagram:
{sequence}

DO NOT wrap the output in Markdown code fences.
DO NOT use ``` or any code block delimiters.
Return ONLY the JSON.

"""

output = call_llm(prompt)

with open("data/report.json", "w") as f:
    f.write(output)