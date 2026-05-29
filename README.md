# Fast Zero

A FastAPI project built from scratch following the "FastAPI do Zero" course.

## Tech Stack

- Python 3.13
- FastAPI 0.136
- Poetry (dependency management)
- Pytest + pytest-cov (testing & coverage)
- Ruff (linting & formatting)
- Taskipy (task runner)

## Setup

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

## Running

```bash
task run
```

The server starts at `http://127.0.0.1:8000`.

## Available Tasks

| Command         | Description                          |
|-----------------|--------------------------------------|
| `task run`      | Start dev server                     |
| `task test`     | Lint + run tests with coverage       |
| `task lint`     | Run Ruff linter                      |
| `task format`   | Fix lint issues + format code        |

## Testing

```bash
task test
```

## Project Structure

```
fast_zero/
├── __init__.py
├── app.py          # FastAPI application
tests/
├── __init__.py
├── test_app.py     # Application tests
pyproject.toml      # Project config & dependencies
```

