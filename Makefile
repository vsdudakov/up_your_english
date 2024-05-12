.PHONY: help  # Shows this message
help:
	@grep '^.PHONY: .* #' Makefile | sed 's/\.PHONY: \(.*\) # \(.*\)/\1	\2/' | expand -t20


.PHONY: install  # Install
install:
	@echo "Create virtual environment"
	cd backend && python -m venv .venv && source .venv/bin/activate

	@echo "Install backend environment"
	cd backend && make install && cp -n .env.dev .env || true

	@echo "Install frontend environment"
	cd frontend && make install && cp -n .env.dev .env || true


.PHONY: lint  # Lint
lint:
	@echo "Lint backend"
	cd backend && make lint

	@echo "Lint frontend"
	cd frontend && make lint


.PHONY: up  # Up
up:
	@echo "Up"
	@exec docker compose up --build