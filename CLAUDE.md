# Project Context

- This is a modern Django project with linters and type checking.
- Test coverage should focus on broad, integration style tests.
    - Use class-based tests for views (from django.test import TestCase).
    - Use pytest-style functional tests for methods & classes.
- Do not make large, sweeping changes that cannot be easily verified.
- DO NOT USE broad try..catch.. blocks to hide bugs. ALLOW UNHANDLED ERRORS TO PROPAGATE.
- AVOID _hacky_ patches that mock out functions or have other unintuitive side effects.
- Add comments when it makes sense to do so, but do not comment trivial behavior.
- When committing changes, the commit message should be a single sentence.
- The tools/ directory contains bash aliases to commands and will activate the correct
  virtual environment before running.

## Development tools

```
# Run django management commands
tools/manage

# Run the tests, linters, etc.
tools/pytest
tools/mypy
tools/ruff check --fix
tools/ruff format

# Rebuild requirements
tools/pip-compile
tools/pip-install
```
