# AI Agent Tutorial Container
# Build: podman build -t ai-agent-tutorial -f Containerfile .
# Run:   podman run -it --rm -e ANTHROPIC_API_KEY="your-key" ai-agent-tutorial

FROM python:3.11-slim

# Set metadata
LABEL description="AI Agent Tutorial - Learn to build AI agents with Claude API"
LABEL maintainer="AI Agent Tutorial"
LABEL version="1.0"

# Set working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    vim \
    less \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir \
    anthropic \
    python-dotenv

# Copy tutorial files
COPY simple_agent_example.py .
COPY ai_agent_tutorial.py .
COPY AI_AGENT_GUIDE.md .
COPY QUICKSTART.md .
COPY README.md* . 2>/dev/null || true

# Create output directory for agent-generated files
RUN mkdir -p /app/output

# Create a welcome script
RUN echo '#!/bin/bash\n\
echo ""\n\
echo "╔══════════════════════════════════════════════════════════════════╗"\n\
echo "║         AI Agent Tutorial - Interactive Container               ║"\n\
echo "╚══════════════════════════════════════════════════════════════════╝"\n\
echo ""\n\
echo "📚 Available Files:"\n\
echo "   • QUICKSTART.md          - Start here! Quick guide"\n\
echo "   • AI_AGENT_GUIDE.md      - Complete learning guide"\n\
echo "   • simple_agent_example.py - Ready-to-run example"\n\
echo "   • ai_agent_tutorial.py   - Comprehensive tutorial"\n\
echo ""\n\
echo "🚀 Quick Commands:"\n\
echo "   • python simple_agent_example.py  - Run the simple example"\n\
echo "   • less QUICKSTART.md              - Read the quick start"\n\
echo "   • vim simple_agent_example.py     - Edit and experiment"\n\
echo ""\n\
echo "🔑 API Key Status:"\n\
if [ -z "$ANTHROPIC_API_KEY" ]; then\n\
    echo "   ⚠️  ANTHROPIC_API_KEY not set!"\n\
    echo "   Run with: podman run -it --rm -e ANTHROPIC_API_KEY=\"your-key\" ai-agent-tutorial"\n\
else\n\
    echo "   ✅ API key is configured"\n\
fi\n\
echo ""\n\
echo "💡 Tip: All files are in /app - use ls to see them"\n\
echo ""\n\
' > /usr/local/bin/welcome.sh && chmod +x /usr/local/bin/welcome.sh

# Create an interactive Python session script
RUN echo '#!/usr/bin/env python3\n\
import anthropic\n\
from anthropic import beta_tool\n\
import os\n\
import math\n\
from datetime import datetime\n\
\n\
print("\\n" + "="*70)\n\
print("Python Interactive Session - Anthropic SDK Pre-loaded")\n\
print("="*70)\n\
print("\\nAvailable imports:")\n\
print("  • anthropic (client ready)")\n\
print("  • beta_tool decorator")\n\
print("  • math, datetime, os")\n\
print("\\nQuick start:")\n\
print("  client = anthropic.Anthropic()")\n\
print("  # Then use client.messages.create(...)")\n\
print("\\n" + "="*70 + "\\n")\n\
\n\
if not os.getenv("ANTHROPIC_API_KEY"):\n\
    print("⚠️  Warning: ANTHROPIC_API_KEY not set\\n")\n\
\n\
# Start interactive Python\n\
import code\n\
code.interact(local=locals())\n\
' > /usr/local/bin/python-interactive.py && chmod +x /usr/local/bin/python-interactive.py

# Create a runner script for examples
RUN echo '#!/bin/bash\n\
if [ -z "$ANTHROPIC_API_KEY" ]; then\n\
    echo "❌ Error: ANTHROPIC_API_KEY environment variable is not set"\n\
    echo ""\n\
    echo "Run the container with:"\n\
    echo "  podman run -it --rm -e ANTHROPIC_API_KEY=\"your-key\" ai-agent-tutorial"\n\
    echo ""\n\
    exit 1\n\
fi\n\
\n\
echo ""\n\
echo "🤖 Running AI Agent Tutorial Examples"\n\
echo "="*70\n\
echo ""\n\
\n\
if [ "$1" == "simple" ]; then\n\
    echo "Running simple_agent_example.py..."\n\
    python simple_agent_example.py\n\
elif [ "$1" == "tutorial" ]; then\n\
    echo "Opening ai_agent_tutorial.py in interactive mode..."\n\
    echo "Uncomment the examples at the bottom to run them."\n\
    vim ai_agent_tutorial.py\n\
elif [ "$1" == "interactive" ]; then\n\
    echo "Starting Python interactive session..."\n\
    python-interactive.py\n\
else\n\
    echo "Usage: run-tutorial [simple|tutorial|interactive]"\n\
    echo ""\n\
    echo "Examples:"\n\
    echo "  run-tutorial simple       - Run the simple example"\n\
    echo "  run-tutorial tutorial     - Open the full tutorial"\n\
    echo "  run-tutorial interactive  - Start Python REPL with SDK loaded"\n\
    echo ""\n\
fi\n\
' > /usr/local/bin/run-tutorial && chmod +x /usr/local/bin/run-tutorial

# Set environment variable for output directory
ENV OUTPUT_DIR=/app/output

# Display welcome message and start bash
CMD ["/bin/bash", "-c", "welcome.sh && exec /bin/bash"]
