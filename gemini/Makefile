# AI Agent Tutorial - Makefile (Gemini)
# Quick commands for building and running the tutorial

.PHONY: help build run clean test install check

# Default target
help:
	@echo "AI Agent Tutorial (Gemini) - Available Commands"
	@echo "================================================"
	@echo ""
	@echo "Container Commands:"
	@echo "  make build      - Build the container image"
	@echo "  make run        - Run the container interactively"
	@echo "  make shell      - Start container with bash shell"
	@echo "  make simple     - Run simple_agent_example.py in container"
	@echo "  make clean      - Remove the container image"
	@echo ""
	@echo "Local Commands:"
	@echo "  make install    - Install Python dependencies locally"
	@echo "  make test       - Run simple example locally"
	@echo "  make check      - Check if API key is set"
	@echo ""
	@echo "Development:"
	@echo "  make workspace  - Run container with workspace mounted"
	@echo ""
	@echo "Note: Set GOOGLE_API_KEY environment variable before running"

# Container commands
build:
	@echo "Building AI Agent Tutorial (Gemini) container..."
	podman build -t ai-agent-gemini -f Containerfile .
	@echo "✓ Build complete!"

run:
	@if [ -z "$$GOOGLE_API_KEY" ]; then \
		echo "❌ Error: GOOGLE_API_KEY not set"; \
		echo "Run: export GOOGLE_API_KEY='your-key'"; \
		exit 1; \
	fi
	podman run -it --rm -e GOOGLE_API_KEY="$$GOOGLE_API_KEY" ai-agent-gemini

shell:
	@if [ -z "$$GOOGLE_API_KEY" ]; then \
		echo "⚠️  Warning: GOOGLE_API_KEY not set"; \
		echo "Set it inside the container with: export GOOGLE_API_KEY='your-key'"; \
	fi
	podman run -it --rm -e GOOGLE_API_KEY="$$GOOGLE_API_KEY" ai-agent-gemini /bin/bash

simple:
	@if [ -z "$$GOOGLE_API_KEY" ]; then \
		echo "❌ Error: GOOGLE_API_KEY not set"; \
		exit 1; \
	fi
	podman run --rm -e GOOGLE_API_KEY="$$GOOGLE_API_KEY" ai-agent-gemini python simple_agent_example.py

clean:
	@echo "Removing AI Agent Tutorial (Gemini) container image..."
	podman rmi ai-agent-gemini || true
	@echo "✓ Clean complete!"

# Local commands
install:
	@echo "Installing Python dependencies..."
	pip install google-generativeai python-dotenv
	@echo "✓ Installation complete!"

test:
	@if [ -z "$$GOOGLE_API_KEY" ]; then \
		echo "❌ Error: GOOGLE_API_KEY not set"; \
		echo "Run: export GOOGLE_API_KEY='your-key'"; \
		exit 1; \
	fi
	@echo "Running simple_agent_example.py locally..."
	python simple_agent_example.py

check:
	@if [ -z "$$GOOGLE_API_KEY" ]; then \
		echo "❌ GOOGLE_API_KEY is not set"; \
		echo "Set it with: export GOOGLE_API_KEY='your-key'"; \
		exit 1; \
	else \
		echo "✓ GOOGLE_API_KEY is set"; \
		echo "Key starts with: $${GOOGLE_API_KEY:0:10}..."; \
	fi

# Development
workspace:
	@if [ -z "$$GOOGLE_API_KEY" ]; then \
		echo "❌ Error: GOOGLE_API_KEY not set"; \
		exit 1; \
	fi
	@mkdir -p workspace
	podman run -it --rm \
		-e GOOGLE_API_KEY="$$GOOGLE_API_KEY" \
		-v $$(pwd)/workspace:/app/workspace:Z \
		ai-agent-gemini

# Docker variants (if user prefers docker over podman)
build-docker:
	docker build -t ai-agent-gemini -f Containerfile .

run-docker:
	@if [ -z "$$GOOGLE_API_KEY" ]; then \
		echo "❌ Error: GOOGLE_API_KEY not set"; \
		exit 1; \
	fi
	docker run -it --rm -e GOOGLE_API_KEY="$$GOOGLE_API_KEY" ai-agent-gemini
