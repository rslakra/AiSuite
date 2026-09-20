PYTHON ?= python3
ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
VENV := $(ROOT)venv
PIP := $(VENV)/bin/pip
UVICORN := $(VENV)/bin/uvicorn
PYTHONPATH := $(ROOT)

.DEFAULT_GOAL := help

.PHONY: help setup install clean

help: ## Show available commands
	@echo "RL-Demo — Reinforcement Learning notebooks"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@grep -E '^[a-zA-Z0-9_-]+:.*##' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'


install: ## Install or upgrade packages from requirements.txt
	@test -d $(VENV) || (echo "Run 'make setup' first to create the virtual environment." && exit 1)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

setup: ## Create venv/ and install requirements.txt
	$(PYTHON) -m venv $(VENV)
	@$(MAKE) install
	# Register venv as the "Python (RL-Demo)" Jupyter kernel for Cursor/VS Code notebooks
	$(VENV)/bin/python -m ipykernel install --user --name=rl-demo --display-name="Python (RL-Demo)"

clean: ## Remove venv and Python/Jupyter cache files
	rm -rf $(VENV)
	find $(ROOT) -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find $(ROOT) -type d -name .ipynb_checkpoints -exec rm -rf {} + 2>/dev/null || true
	find $(ROOT) -type f -name '*.py[co]' -delete 2>/dev/null || true
