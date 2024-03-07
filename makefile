runserver:
	uvicorn rinha_de_backend.main:app --reload

.PHONY: lint
lint:
	ruff format .
	ruff check . --fix

.PHONY: trunc-tran
trunc-tran:
	bash scripts/truncate_transacoes.sh