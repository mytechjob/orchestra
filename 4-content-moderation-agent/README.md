# Content Moderation Agent

A LangGraph-based AI agent for automated content moderation with human-in-the-loop review capabilities.

## Features

- **Automated Classification**: Categorizes content as safe, spam, inappropriate, hate_speech, misinformation, copyright, or nsfw
- **Multi-Stage Analysis**: Toxicity analysis, spam detection, and context-aware decision making
- **Human Review**: Interrupt-based workflow for moderator approval on borderline cases
- **Author History**: Considers user's past behavior and trust score
- **Auto-Actions**: Automatically approves safe content and rejects clear violations

## Architecture

```
START → ingest_content → classify_content
                                      ↓
                    ┌─────────────────┼─────────────────┐
                    ↓                 ↓                 ↓
           analyze_toxicity    analyze_spam     direct_action
                    ↓                 ↓
                    └────────┬────────┘
                             ↓
                      direct_action
                             ↓
                    ┌────────┴────────┐
                    ↓                 ↓
              human_review         publish → END
                    ↓
              ┌─────┴─────┐
              ↓           ↓
         publish    remove_content → END
```

## Workflow

1. **ingest_content** - Logs incoming content
2. **classify_content** - Uses LLM to categorize content and assess risk
3. **analyze_toxicity** - Deep analysis for harmful language (high-confidence safe content skips this)
4. **analyze_spam** - Rule-based + LLM spam detection
5. **direct_action** - Executes automatic decision or escalates to review
6. **human_review** - Pauses for moderator input on borderline cases
7. **publish** - Approves and publishes content
8. **remove_content** - Rejects and removes violating content

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

3. Run the agent:
```bash
python main.py
```

## Test Cases

The `main.py` includes 5 test scenarios:
- ✅ Safe content (auto-approve)
- 🚫 Obvious spam (auto-reject)
- ⚠️ Borderline content (human review)
- 🚩 Toxic content (flag for review)
- 📢 Mild promotional content (spam analysis)

## Customization

- Add more content types in `states.py`
- Implement real toxicity API integration in `analyze_toxicity`
- Connect to actual content platform APIs in `publish`/`remove_content`
- Add more spam indicators in `analyze_spam`
- Implement author notification system
