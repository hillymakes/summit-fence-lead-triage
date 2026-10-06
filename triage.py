"""Summit Fence Co. lead triage agent.

Reads inquiries.json, sends each inquiry to Claude with the rules in prompt.md,
and writes scored, categorized inquiries with draft replies to results.json,
sorted by urgency. Every reply is a draft for a person to review.

Usage:
    pip install anthropic
    export ANTHROPIC_API_KEY=your_key
    python triage.py
"""
import json
import anthropic

MODEL = "claude-sonnet-5-5"
FIELDS = ["urgency", "category", "reason", "needs_human", "reply"]


def triage(client, rules, inquiry):
    response = client.messages.create(
        model=MODEL,
        max_tokens=800,
        system=rules + "\n\nRespond with only a JSON object with these keys: " + ", ".join(FIELDS) + ".",
        messages=[{
            "role": "user",
            "content": f"From: {inquiry['name']} via {inquiry['channel']}\n\n{inquiry['message']}",
        }],
    )
    text = response.content[0].text.strip()
    start, end = text.find("{"), text.rfind("}") + 1
    result = json.loads(text[start:end])
    missing = [f for f in FIELDS if f not in result]
    if missing:
        raise ValueError(f"Inquiry {inquiry['id']} missing fields: {missing}")
    return {**inquiry, **{f: result[f] for f in FIELDS}}


def main():
    client = anthropic.Anthropic()
    rules = open("prompt.md", encoding="utf-8").read()
    inquiries = json.load(open("inquiries.json", encoding="utf-8"))
    results = []
    for inquiry in inquiries:
        print(f"Triaging #{inquiry['id']} from {inquiry['name']}...")
        results.append(triage(client, rules, inquiry))
    results.sort(key=lambda r: -int(r["urgency"]))
    json.dump(results, open("results.json", "w", encoding="utf-8"), indent=2)
    print(f"Done. {len(results)} inquiries triaged.")


if __name__ == "__main__":
    main()
