curl -sSL https://install.python-poetry.org | python3 -
poetry install
poetry run pre-commit install

echo 'export PYTHONDONTWRITEBYTECODE=1' >> ~/.zshrc
