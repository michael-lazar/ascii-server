[![build](https://github.com/michael-lazar/ascii-server/workflows/test/badge.svg)](https://github.com/michael-lazar/ascii-server/actions?query=workflow%3Atest)

# ascii-server

This repo hosts the codebase (python, django) powering [https://ascii.mozz.us](https://ascii.mozz.us).

Even though the code is public, this is mostly a personal project and I'm not looking for outside help or ideas.

However, small issues for things like bugs & typos are welcome and very much appreciated!

## Development

```bash
# Download the source
git clone https://github.com/michael-lazar/ascii-server
cd ascii-server/

# Initialize a virtual environment and install dependencies, etc.
# (requires uv, https://docs.astral.sh/uv/)
tools/bootstrap

# Create a user account for the admin dashboard
tools/manage createsuperuser

# Initialize pre-commit hooks
uv run pre-commit install

# Launch a local server
tools/start

# Run the tests, linters, etc.
tools/pytest
tools/mypy
tools/ruff check --fix
tools/ruff format

# Rebuild the lockfile / re-sync the virtual environment
tools/uv-compile
tools/uv-install

# Find your house
telnet mapscii.me
```

## License

[The Human Software License](https://license.mozz.us)

> A hobbyist software license that promotes maintainer happiness
> through personal interactions. Non-human
> [legal entities](https://en.wikipedia.org/wiki/Legal_person) such as
> corporations and agencies aren't allowed to participate.
