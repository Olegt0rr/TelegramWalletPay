.PHONY: *

install:
	pip install -e ."[dev,test]" -U --upgrade-strategy=eager
	pre-commit install

mypy:
	mypy -p telegram_wallet_pay
	mypy -p tests

ruff:
	ruff check telegram_wallet_pay --fix
	ruff check tests --fix
	ruff check examples --fix

lint: ruff mypy
