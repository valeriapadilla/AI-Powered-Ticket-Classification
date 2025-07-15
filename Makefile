# Makefile – Fullstack orchestration for Next.js frontend and FastAPI backend

#* --- Frontend (Next.js) ---
FRONT_DIR     := frontend
NODE_VERSION  := 22.17.0
NVM           := export NVM_DIR="$$HOME/.nvm"; [ -s "$$NVM_DIR/nvm.sh" ] && . "$$NVM_DIR/nvm.sh" && nvm use $(NODE_VERSION)

#* --- Backend (FastAPI) ---
BACKEND_DIR   := backend
VENV          := .venv

PYTHON_BIN    := $(BACKEND_DIR)/$(VENV)/bin/python
PIP_BIN       := $(BACKEND_DIR)/$(VENV)/bin/pip
UVICORN       := $(BACKEND_DIR)/$(VENV)/bin/uvicorn
BLACK         := $(BACKEND_DIR)/$(VENV)/bin/black
RUFF          := $(BACKEND_DIR)/$(VENV)/bin/ruff
PYTEST        := $(BACKEND_DIR)/$(VENV)/bin/pytest

.DEFAULT_GOAL := help

## Show available commands with descriptions
help:
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-24s\033[0m %s\n", $$1, $$2}'
	@echo ""

#* --- Frontend Commands ---

frontend-install:        ## Install frontend dependencies using npm
	$(NVM) && cd $(FRONT_DIR) && npm install

frontend-dev:            ## Run the Next.js development server
	$(NVM) && cd $(FRONT_DIR) && npm run dev

frontend-build:          ## Build the Next.js application for production
	$(NVM) && cd $(FRONT_DIR) && npm run build

frontend-lint:           ## Run ESLint to analyze and report code quality issues
	$(NVM) && cd $(FRONT_DIR) && npm run lint

frontend-typecheck:      ## Perform TypeScript type checking (no code emitted)
	$(NVM) && cd $(FRONT_DIR) && npx tsc --noEmit

frontend-clean:          ## Remove frontend build artifacts (e.g. .next/)
	cd $(FRONT_DIR) && rm -rf .next

frontend-init:           ## Run install, lint, and typecheck in sequence
	make frontend-install
	make frontend-lint
	make frontend-typecheck

#* --- Backend Commands ---

backend-install:         ## Create venv (if missing) and install backend dependencies
	cd $(BACKEND_DIR) && \
	if [ ! -x "$(VENV)/bin/pip" ]; then \
		echo "🔧 Creating virtual environment..."; \
		python -m venv $(VENV); \
	fi && \
	$(VENV)/bin/pip install --upgrade pip && \
	$(VENV)/bin/pip install -r requirements.txt

backend-run:             ## Run FastAPI app with Uvicorn
	cd $(BACKEND_DIR) && $(VENV)/bin/uvicorn app.main:app --reload

backend-lint:            ## Lint and format backend code with Ruff and Black
	cd $(BACKEND_DIR) && $(VENV)/bin/ruff check . && $(VENV)/bin/black .

backend-test:            ## Run backend tests using Pytest
	cd $(BACKEND_DIR) && $(VENV)/bin/pytest

backend-clean:           ## Remove Python cache and compiled files
	find $(BACKEND_DIR) -type d -name "__pycache__" -exec rm -r {} + || true
	find $(BACKEND_DIR) -type f -name "*.py[co]" -delete || true
	rm -f $(BACKEND_DIR)/.coverage

backend-init:            ## Lint, test, and clean backend
	make backend-lint
	make backend-test
	make backend-clean

#* --- Project Commands ---

project-install:         ## Install all frontend and backend dependencies
	make frontend-install
	make backend-install

project-dev:             ## Run both frontend and backend servers concurrently
	@echo "🚀 Starting development servers..."
	@echo "  Frontend: http://localhost:3000"
	@echo "  Backend : http://localhost:8000"
	@echo ""
	@$(MAKE) --no-print-directory -j2 frontend-dev backend-run
