# Facts For Elder Scrolls

![Deploy](https://github.com/mastash3ff/Alexa-ElderScrollsFacts/actions/workflows/deploy.yml/badge.svg)

An Alexa skill that delivers random lore facts from the Elder Scrolls universe, spanning Arena through ESO.

## Usage

**Invocation:** `facts for elder scrolls`

| Say... | Response |
|--------|----------|
| "Alexa, open facts for elder scrolls" | Speaks a random fact and closes |
| "Tell me a fact" | Delivers another fact |
| "Help" | Lists available commands |
| "Stop" / "Exit" | Ends the skill |

## Development

**Stack:** Python 3.12 · ASK SDK v2 · AWS Lambda (us-east-1)

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
PYTHONPATH=. pytest tests/ -v

# Deploy — automatic on push to master via GitHub Actions
```

## Project structure

```
lambda_function.py      Intent handlers and fact bank (70 facts)
requirements.txt        ask-sdk-core dependency
tests/test_skill.py     Unit tests
.github/workflows/      CI/CD — tests gate deployment to Lambda
```
