[![build](https://github.com/michael-lazar/ascii-server/workflows/test/badge.svg)](https://github.com/michael-lazar/ascii-server/actions?query=workflow%3Atest)

# ascii-server

This repo hosts the codebase (python, django) powering [https://ascii.mozz.us](https://ascii.mozz.us).

Even though the code is public, this is mostly a personal project and I'm not looking for outside help or ideas.

However, small issues for things like bugs & typos are welcome and very much appreciated!

## Requirements

- python3.11

## Quickstart

```bash
# Download the source
git clone https://github.com/michael-lazar/ascii-server
cd ascii-server/

# Initialize a virtual environment and install pip dependencies, etc.
tools/boostrap

# Create a user account for the admin dashboard
tools/manage createsuperuser

# Launch a local server
tools/start

# Initialize pre-commit hooks
pre-commit install

# Run the tests, linters, etc.
tools/pytest
tools/mypy
tools/ruff check --fix
tools/ruff format

# Rebuild requirements
tools/pip-compile
tools/pip-install

# Find your house
telnet mapscii.me
```

## License

[The Human Software License](https://license.mozz.us)

> A hobbyist software license that promotes maintainer happiness
> through personal interactions. Non-human
> [legal entities](https://en.wikipedia.org/wiki/Legal_person) such as
> corporations and agencies aren't allowed to participate.
