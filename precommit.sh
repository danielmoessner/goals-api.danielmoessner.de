#!/bin/bash

printf "djlint:\n" && .venv/bin/djlint . --reformat
printf "\n\n"
printf "\nisort:\n" && .venv/bin/isort . --profile black
printf "\n\n"
printf "black:\n" && .venv/bin/black .
printf "\n\n"
printf "ruff:\n" && .venv/bin/ruff check . --fix
# printf "\n\n"
# printf "css:\n" && npm run css
# printf "mypy:\n"  && pdm run mypy .
# printf "\n\n"
