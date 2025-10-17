.PHONY: test lint build docker

test:
	@echo "Run tests (customize per repo)"
	# e.g. npm test or pytest -q

lint:
	@echo "Run linters (customize per repo)"
	# e.g. npm run lint or flake8

build:
	@echo "Build project (customize per repo)"
	# e.g. npm run build or python -m build

docker:
	docker build -t ${USER:-app}:latest .
