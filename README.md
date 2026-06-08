# TestMu AI — Automation Assignment

Mini parallel execution testing framework for the TestMu AI Solutions Engineer assignment.

| Feature | Status |
|---------|--------|
| Amazon search → add-to-cart → price (iPhone + Galaxy) | ✅ |
| Parallel execution (pytest-xdist) | ✅ |
| Chrome + Edge support | ✅ |
| Page Object Model | ✅ |
| Configurable threads, browsers, waits via YAML | ✅ |
| LambdaTest cloud integration | ✅ (toggle in config.yaml) |
| Dockerized | ✅ |
| AI-assisted development | ✅ (entire project built via AI) |

## Quick Start — Local

### Install

```bash
pip install -r requirements.txt
```

### Run — Sequential

```bash
pytest tests/ -v --tb=short
```

### Run — Parallel (2 workers)

```bash
pytest tests/ -n 2 -v --tb=short
```

### Run — Both browsers, parallel (4 workers total: 2 tests × 2 browsers)

```bash
pytest tests/ -n 4 -v --tb=short
```

### Run — Single browser

```bash
pytest tests/ -k chrome -n 2 -v
```

### Run — LambdaTest Cloud

```bash
set LT_USERNAME=your_username
set LT_ACCESS_KEY=your_access_key
pytest tests/ --lt -n 4 -v --tb=short
```

## Docker

### Build and run

```bash
docker build -t testmu-assignment .
docker run --rm testmu-assignment
```

Default command: 4 parallel workers (2 tests × 2 browsers).

### Override workers

```bash
docker run --rm testmu-assignment pytest tests/ -n 2 -v --tb=short
```

### LambdaTest from Docker

```bash
docker run --rm -e LT_USERNAME=... -e LT_ACCESS_KEY=... testmu-assignment pytest tests/ --lt -n 4 -v
```

## Configuration

Edit `config/config.yaml`:

```yaml
browsers: [chrome, edge]        # test both, or just one
parallel_threads: 2              # pytest -n value
default_wait: 10                 # seconds
lambdatest:
  enabled: false                 # set true for cloud execution
```

## Project Structure

```
testmu-assignment/
├── config/
│   └── config.yaml              # All config: browsers, threads, URLs, LT
├── pages/
│   ├── base_page.py             # Base page — wait, click, type
│   └── amazon_page.py           # Amazon POM — search, add-to-cart, price
├── tests/
│   ├── conftest.py              # Fixtures, browser parametrization, --lt flag
│   └── test_amazon.py           # TC1 (iPhone) + TC2 (Galaxy)
├── utils/
│   ├── driver_factory.py        # Local + LambdaTest WebDriver factory
│   └── logger.py                # Logging utility
├── Dockerfile                   # Chrome + Edge + pytest in one image
├── pytest.ini
├── requirements.txt
└── README.md
```

## Key Design Decisions

| Decision | Why |
|----------|-----|
| Python + Selenium | Most widely supported; LambdaTest docs are Selenium-first |
| pytest-xdist | Simplest parallel execution — just `-n` flag. Configurable in YAML. |
| Page Object Model | Industry standard; separates locators from test logic |
| YAML config | Change browsers/threads/URLs without touching code |
| Chrome + Edge in Docker | Both modern browsers in one image; parametrized via conftest |
| LambdaTest via `--lt` flag | One flag toggles local ↔ cloud. No code changes needed. |
| Headless mode | Works in Docker without display server |
