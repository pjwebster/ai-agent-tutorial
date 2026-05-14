# AI Agent Tutorial - Anthropic Claude

Build AI agents from scratch using Claude API and Python.

## 🚀 Quick Start

```bash
# Install dependencies
pip install anthropic

# Set your API key
export ANTHROPIC_API_KEY="your-api-key-here"

# Run the simple example
python simple_agent_example.py
```

Get your API key from: https://console.anthropic.com/

## 📚 Tutorial Files

| File | Description | Start Here? |
|------|-------------|-------------|
| **QUICKSTART.md** | Quick reference guide | ✅ Yes |
| **simple_agent_example.py** | Ready-to-run minimal agent | ✅ Yes |
| **AI_AGENT_GUIDE.md** | Complete learning guide | After QUICKSTART |
| **ai_agent_tutorial.py** | Comprehensive tutorial code | After simple example |
| **CONTAINER_GUIDE.md** | Container usage guide | If using containers |

## 📖 Learning Path

### Beginner (30 minutes)
1. Read `QUICKSTART.md`
2. Run `simple_agent_example.py`
3. Modify a tool and see what changes

### Intermediate (2 hours)
1. Read `AI_AGENT_GUIDE.md`
2. Study `ai_agent_tutorial.py`
3. Try all three patterns (simple, advanced, conversational)

### Advanced (4+ hours)
1. Build your own agent project
2. Implement custom tools
3. Experiment with different configurations

## 🔑 Core Pattern

```python
from anthropic import beta_tool
import anthropic

# 1. Define tools Claude can use
@beta_tool
def my_tool(param: str) -> str:
    """Clear description of what this does."""
    return "result"

# 2. Create agent with tools
client = anthropic.Anthropic()

runner = client.beta.messages.tool_runner(
    model="claude-opus-4-7",
    max_tokens=16000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},
    tools=[my_tool],
    messages=[{"role": "user", "content": "Do something"}]
)

# 3. Let Claude work
for message in runner:
    # Claude automatically calls tools until done
    pass
```

## 🐳 Container Support

```bash
# Build the container
podman build -t ai-agent-anthropic -f Containerfile .

# Run it
podman run -it --rm -e ANTHROPIC_API_KEY="your-key" ai-agent-anthropic
```

See `CONTAINER_GUIDE.md` for detailed container usage.

## 💰 Cost Awareness

**Opus 4.7 Pricing:**
- Input: $5 per 1M tokens
- Output: $25 per 1M tokens

**Typical costs for learning:**
- Simple query: ~$0.01-0.05
- Complex agent task: ~$0.10-0.50
- One hour of experimentation: ~$1-5

## 🎯 Key Features

- **Tool Runner**: Automatic loop handling
- **Adaptive Thinking**: Claude dynamically decides when to think
- **Code Execution**: Built-in server-side code execution
- **Managed Agents**: Server-hosted agent sessions
- **Prompt Caching**: Up to 90% cost savings on repeated context

## 📚 Additional Resources

- [Claude API Docs](https://docs.anthropic.com/)
- [Python SDK](https://github.com/anthropics/anthropic-sdk-python)
- [Tool Use Guide](https://docs.anthropic.com/claude/docs/tool-use)
- [Anthropic Discord](https://anthropic.com/discord)

## 🎉 Ready to Begin?

1. **Quick Start**: Read `QUICKSTART.md` and run `simple_agent_example.py`
2. **Deep Dive**: Study `AI_AGENT_GUIDE.md` for complete understanding
3. **Build**: Create your own agent using the patterns you learned

---

**Looking for Google Gemini?** See the [`../gemini/`](../gemini/) directory for the Gemini version of this tutorial.

Happy building! 🚀
