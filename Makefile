.PHONY: *

pre-commit:
	pre-commit install
	pre-commit autoupdate

mypy:
	mypy -p telegram_wallet_pay

ruff:
	ruff check telegram_wallet_pay --fix
	ruff check tests --fix
