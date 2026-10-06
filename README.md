# Summit Fence Lead Triage

An AI lead triage agent for Summit Fence Co., a fictional fencing contractor. It reads messy customer inquiries from forms, email, voicemail, and DMs, then for each one:

- scores urgency from 1 to 5 using clear business rules
- sorts it into a category (Safety / Repair, Quote, Warranty / Complaint, and so on)
- explains the score in one sentence
- drafts a warm, plain-spoken reply with one clear next step
- flags anything that needs a person: pricing, disputes, injuries, or legal issues

Every reply is a draft. A person approves or edits it before it's sent.

**Live demo:** https://hillymakes.github.io/summit-fence-lead-triage/

## Files

| File | What it is |
|---|---|
| `prompt.md` | The triage rules and reply guidelines the agent follows |
| `inquiries.json` | 15 fictional customer inquiries |
| `triage.py` | Sends each inquiry to Claude with the rules and writes `results.json` |
| `results.json` | Scored, categorized inquiries with draft replies |
| `index.html` | The review queue: filter by urgency, edit drafts, approve or escalate |

## Run it live

```
pip install anthropic
export ANTHROPIC_API_KEY=your_key
python triage.py
```

The demo page uses results generated with Claude so it works without an API key.

Companion project: [Summit Fence operating review](https://hillymakes.github.io/summit-fence-operating-review/)

Built by Hillary Hubbard with Claude Code.
