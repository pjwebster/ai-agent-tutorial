# AI Agent Tutorial - Container Guide

This guide shows you how to run the AI agent tutorial in a container using Podman or Docker.

---

## 🚀 Quick Start

### 1. Build the Container

```bash
# Using Podman (recommended for Fedora/RHEL)
podman build -t ai-agent-tutorial -f Containerfile .

# Or using Docker
docker build -t ai-agent-tutorial -f Containerfile .
```

### 2. Run the Container

```bash
# Replace 'your-api-key-here' with your actual Anthropic API key
podman run -it --rm -e ANTHROPIC_API_KEY="your-api-key-here" ai-agent-tutorial

# Or with Docker
docker run -it --rm -e ANTHROPIC_API_KEY="your-api-key-here" ai-agent-tutorial
```

You'll see a welcome screen and drop into an interactive shell.

---

## 📖 Container Usage

Once inside the container, you have several options:

### Option 1: Run the Simple Example

```bash
python simple_agent_example.py
```

This runs a complete working agent with math and time tools.

### Option 2: Use the Helper Script

```bash
# Run the simple example
run-tutorial simple

# Open the full tutorial in vim
run-tutorial tutorial

# Start an interactive Python session
run-tutorial interactive
```

### Option 3: Explore the Files

```bash
# Read the quick start guide
less QUICKSTART.md

# Read the complete guide
less AI_AGENT_GUIDE.md

# Edit and run your own code
vim my_agent.py
python my_agent.py
```

### Option 4: Interactive Python REPL

Start a Python session with the Anthropic SDK pre-loaded:

```bash
python-interactive.py
```

Then in Python:

```python
client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.content[0].text)
```

---

## 🔑 Setting Your API Key

### Method 1: Pass as Environment Variable (Recommended)

```bash
podman run -it --rm \
  -e ANTHROPIC_API_KEY="your-api-key-here" \
  ai-agent-tutorial
```

### Method 2: Use an Environment File

Create a file `.env`:

```bash
ANTHROPIC_API_KEY=your-api-key-here
```

Run with:

```bash
podman run -it --rm --env-file .env ai-agent-tutorial
```

### Method 3: Set After Starting

Start the container without the key:

```bash
podman run -it --rm ai-agent-tutorial
```

Then inside the container:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
python simple_agent_example.py
```

---

## 💾 Persisting Your Work

By default, any files you create are lost when the container exits. To save your work:

### Mount a Local Directory

```bash
podman run -it --rm \
  -e ANTHROPIC_API_KEY="your-api-key-here" \
  -v $(pwd)/my-agents:/app/workspace:Z \
  ai-agent-tutorial
```

Now anything you save in `/app/workspace` inside the container will be in `./my-agents` on your host.

### Save Agent Output

The container has an `/app/output` directory. Mount it to save generated files:

```bash
podman run -it --rm \
  -e ANTHROPIC_API_KEY="your-api-key-here" \
  -v $(pwd)/output:/app/output:Z \
  ai-agent-tutorial
```

---

## 🛠️ Development Workflow

Here's a typical workflow for developing agents in the container:

### 1. Start the Container with Workspace Mount

```bash
podman run -it --rm \
  -e ANTHROPIC_API_KEY="your-api-key-here" \
  -v $(pwd)/my-work:/app/workspace:Z \
  ai-agent-tutorial
```

### 2. Create Your Agent

```bash
cd /app/workspace
vim my_research_agent.py
```

### 3. Run and Test

```bash
python my_research_agent.py
```

### 4. Iterate

Edit, run, test, repeat. Your files persist in `./my-work` on your host.

---

## 📋 Advanced Usage

### Run a Specific Script Directly

```bash
# Run a single command and exit
podman run --rm \
  -e ANTHROPIC_API_KEY="your-key" \
  ai-agent-tutorial \
  python simple_agent_example.py
```

### Execute Multiple Commands

```bash
podman run --rm \
  -e ANTHROPIC_API_KEY="your-key" \
  ai-agent-tutorial \
  /bin/bash -c "python simple_agent_example.py && ls -la"
```

### Copy Files Out of Container

If you create files and need to extract them:

```bash
# Start container with a name
podman run -it --name my-tutorial \
  -e ANTHROPIC_API_KEY="your-key" \
  ai-agent-tutorial

# In another terminal, copy files out
podman cp my-tutorial:/app/output/findings.txt ./

# Clean up
podman rm my-tutorial
```

### Use with Docker Compose / Podman Compose

Create `compose.yml`:

```yaml
version: '3.8'

services:
  tutorial:
    build:
      context: .
      dockerfile: Containerfile
    image: ai-agent-tutorial
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./workspace:/app/workspace
      - ./output:/app/output
    stdin_open: true
    tty: true
```

Run:

```bash
# Set your API key
export ANTHROPIC_API_KEY="your-key-here"

# Start the service
podman-compose up -d

# Attach to it
podman-compose exec tutorial /bin/bash

# Stop when done
podman-compose down
```

---

## 🐛 Troubleshooting

### "Error: ANTHROPIC_API_KEY not set"

Make sure you're passing the API key when running:

```bash
podman run -it --rm -e ANTHROPIC_API_KEY="sk-ant-..." ai-agent-tutorial
```

### Permission Denied on Mounted Volumes

If you get permission errors with SELinux (Fedora/RHEL), add `:Z` to your volume mount:

```bash
-v $(pwd)/workspace:/app/workspace:Z
```

### Container Build Fails

Make sure all tutorial files are in the current directory:

```bash
ls -la *.py *.md
# Should show: simple_agent_example.py, ai_agent_tutorial.py, AI_AGENT_GUIDE.md, QUICKSTART.md
```

### Python Module Not Found

If you get "No module named 'anthropic'", rebuild the container:

```bash
podman build --no-cache -t ai-agent-tutorial -f Containerfile .
```

---

## 📊 Container Details

### What's Included

- **Base**: Python 3.11 slim
- **Packages**: anthropic SDK, python-dotenv
- **Tools**: vim, less
- **Scripts**: 
  - `welcome.sh` - Welcome message
  - `run-tutorial` - Helper to run examples
  - `python-interactive.py` - Pre-configured REPL

### Directories

- `/app` - Main working directory (contains tutorial files)
- `/app/output` - For agent-generated files
- `/app/workspace` - Mount your workspace here

---

## 🎯 Example Workflows

### Workflow 1: Learn the Basics

```bash
# Start container
podman run -it --rm -e ANTHROPIC_API_KEY="your-key" ai-agent-tutorial

# Inside container:
less QUICKSTART.md          # Read the guide
python simple_agent_example.py   # Run the example
exit
```

### Workflow 2: Develop Your Agent

```bash
# Start with workspace mounted
podman run -it --rm \
  -e ANTHROPIC_API_KEY="your-key" \
  -v $(pwd)/agents:/app/workspace:Z \
  ai-agent-tutorial

# Inside container:
cd /app/workspace
vim my_agent.py             # Create your agent
python my_agent.py          # Test it
# Files saved in ./agents on host
exit
```

### Workflow 3: Quick Test

```bash
# Run simple example without entering container
podman run --rm \
  -e ANTHROPIC_API_KEY="your-key" \
  ai-agent-tutorial \
  python simple_agent_example.py
```

---

## 🎓 Next Steps

After getting familiar with the container:

1. **Customize the Containerfile** - Add your own tools or dependencies
2. **Build a Project** - Use the mounted workspace for a real project
3. **Automate with Scripts** - Create shell scripts to run your agents
4. **Deploy** - Use this container as a base for production agents

---

## 📝 Notes

- The container runs as root by default (standard for learning containers)
- For production, create a non-root user in the Containerfile
- API keys are passed as environment variables - never bake them into the image
- All changes inside the container are lost unless mounted to a volume

---

## 🎉 You're Ready!

Your containerized AI agent tutorial environment is ready to use.

**Quick start:**

```bash
podman build -t ai-agent-tutorial -f Containerfile .
podman run -it --rm -e ANTHROPIC_API_KEY="your-key" ai-agent-tutorial
python simple_agent_example.py
```

Happy building! 🚀
