PYTHON ?= python3
ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
VENV := $(ROOT)venv
PIP := $(VENV)/bin/pip
UVICORN := $(VENV)/bin/uvicorn
HOST ?= 0.0.0.0
PORT ?= 8080
BREW ?= brew
OLLAMA ?= $(shell command -v ollama 2>/dev/null)
CHAT_MODEL ?= llama3:8b
EMBED_MODEL ?= nomic-embed-text
OLLAMA_HOME ?= $(HOME)/.ollama

.DEFAULT_GOAL := help

.PHONY: help setup install start stop restart clean ollama-install ollama-clean

help: ## Show available commands
	@echo "Local RAG App — chat with your documents offline"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@grep -E '^[a-zA-Z0-9_-]+:.*##' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "First-time workflow:"
	@echo "  make setup"
	@echo "  make ollama-install"
	@echo "  make start"
	@echo ""
	@echo "App: http://localhost:$(PORT)"

setup: ## Create venv, copy .env.sample if missing, and install dependencies
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	@test -f $(ROOT).env || (cp $(ROOT).env.sample $(ROOT).env && echo "Created .env from .env.sample")
	@$(MAKE) install

install: ## Install or upgrade packages from requirements.txt
	@test -d $(VENV) || (echo "Run 'make setup' first to create the virtual environment." && exit 1)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

start: install ## Run the FastAPI app with uvicorn (reload on port $(PORT))
	@$(MAKE) stop
	@echo "Local RAG App: http://localhost:$(PORT)"
	cd $(ROOT) && PYTHONPATH=$(ROOT) $(UVICORN) app.main:app --host $(HOST) --port $(PORT) --reload

stop: ## Stop any process listening on port $(PORT)
	@pids=$$(lsof -tiTCP:$(PORT) -sTCP:LISTEN 2>/dev/null); \
	if [ -n "$$pids" ]; then \
		echo "Stopping process on port $(PORT) ($$pids)..."; \
		kill $$pids 2>/dev/null || true; \
		sleep 1; \
		pids=$$(lsof -tiTCP:$(PORT) -sTCP:LISTEN 2>/dev/null); \
		if [ -n "$$pids" ]; then \
			kill -9 $$pids 2>/dev/null || true; \
			sleep 1; \
		fi; \
	else \
		echo "Nothing listening on port $(PORT)."; \
	fi

restart: stop start ## Stop then start the app on port $(PORT)

ollama-install: ## Install Ollama (Homebrew), start service, pull default models
	@if [ -z "$(OLLAMA)" ]; then \
		if ! command -v $(BREW) >/dev/null 2>&1; then \
			echo "Ollama not found and Homebrew is unavailable."; \
			echo "Install from https://ollama.com/download then re-run: make ollama-install"; \
			exit 1; \
		fi; \
		echo "Installing Ollama via Homebrew..."; \
		$(BREW) install ollama; \
	fi
	@command -v ollama >/dev/null 2>&1 || (echo "Ollama install failed — ollama not on PATH." && exit 1)
	@if command -v $(BREW) >/dev/null 2>&1 && $(BREW) services list 2>/dev/null | grep -q ollama; then \
		echo "Starting Ollama service..."; \
		$(BREW) services start ollama; \
		sleep 2; \
	fi
	@echo "Pulling $(CHAT_MODEL) and $(EMBED_MODEL)..."
	ollama pull $(CHAT_MODEL)
	ollama pull $(EMBED_MODEL)
	@echo "Ollama models ready:"
	@ollama list

ollama-clean: ## Remove all downloaded Ollama models (~/.ollama/models)
	@if command -v ollama >/dev/null 2>&1; then \
		echo "Removing pulled Ollama models..."; \
		ollama list -q 2>/dev/null | while read -r model; do \
			[ -n "$$model" ] && ollama rm "$$model" || true; \
		done; \
	fi
	@if command -v $(BREW) >/dev/null 2>&1 && $(BREW) services list 2>/dev/null | grep -q ollama; then \
		$(BREW) services stop ollama 2>/dev/null || true; \
	fi
	@if [ -d "$(OLLAMA_HOME)/models" ]; then \
		echo "Deleting $(OLLAMA_HOME)/models"; \
		rm -rf "$(OLLAMA_HOME)/models"; \
	fi
	@if [ -d "$(OLLAMA_HOME)/cache" ]; then \
		echo "Deleting $(OLLAMA_HOME)/cache"; \
		rm -rf "$(OLLAMA_HOME)/cache"; \
	fi
	@echo "Ollama downloads removed. Re-install with: make ollama-install"

clean: ## Remove venv and Python cache files
	rm -rf $(VENV)
	find $(ROOT) -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find $(ROOT) -type f -name '*.py[co]' -delete 2>/dev/null || true
