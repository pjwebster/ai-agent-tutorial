# AI Agent Tutorial - Build Agents from Scratch

A comprehensive, hands-on tutorial for building AI agents using Claude API and Python.

## 🎯 What You'll Learn

- What AI agents are and when to use them
- How to design and implement tools for Claude
- Two approaches: Tool Runner (easy) and Manual Loop (advanced)
- Best practices for production agents
- Cost optimization and error handling

## 🚀 Quick Start

### Option 1: Run Locally

```bash
# Install dependencies
pip install anthropic

# Set your API key
export ANTHROPIC_API_KEY="your-api-key-here"

# Run the simple example
python simple_agent_example.py
```

### Option 2: Use Container

```bash
# Build the container
podman build -t ai-agent-tutorial -f Containerfile .

# Run it
podman run -it --rm -e ANTHROPIC_API_KEY="your-key" ai-agent-tutorial
```

See [CONTAINER_GUIDE.md](CONTAINER_GUIDE.md) for detailed container usage.

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

## 🛠️ Project Ideas

Start with one of these to practice:

### 1. Research Assistant
**Tools**: `web_search`, `analyze_data`, `save_findings`

**Task**: "Research the latest developments in quantum computing and save a summary"

### 2. File Analyzer
**Tools**: `list_files`, `read_file`, `analyze_content`, `create_summary`

**Task**: "Find all Python files in this directory and create a report of TODOs"

### 3. Data Processor
**Tools**: `load_csv`, `analyze_statistics`, `create_chart`, `save_results`

**Task**: "Analyze sales_data.csv and create visualizations of trends"

## 🔑 Getting Your API Key

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new key
5. Copy and save it securely

**Cost Awareness:**
- Simple examples: ~$0.01-0.05 each
- Complex agent tasks: ~$0.10-0.50 each
- One hour of learning: ~$1-5 total

## 📦 What's Included

### Tutorial Files
- ✅ Step-by-step guides (Markdown)
- ✅ Working code examples (Python)
- ✅ Production patterns and best practices
- ✅ Containerfile for isolated environment

### Code Examples
- ✅ Simple agent (tool runner)
- ✅ Advanced agent (manual loop)
- ✅ Conversational agent (multi-turn)
- ✅ Error handling patterns
- ✅ Cost optimization techniques

## 🎓 Key Concepts

### What is an AI Agent?

**Simple Chatbot:**
```
User: "What's 2+2?"
Claude: "4"
[DONE]
```

**AI Agent:**
```
User: "Research quantum computing and save a summary"
Claude: [Decides what to do]
   → Calls web_search("quantum computing")
   → Analyzes results
   → Calls save_findings(...)
[DONE - Task completed autonomously]
```

### Core Pattern

```python
from anthropic import beta_tool

# 1. Define tools
@beta_tool
def my_tool(param: str) -> str:
    """What this tool does."""
    return "result"

# 2. Create agent
runner = client.beta.messages.tool_runner(
    model="claude-opus-4-7",
    tools=[my_tool],
    messages=[{"role": "user", "content": "Task"}]
)

# 3. Run until done
for message in runner:
    # Claude automatically calls tools
    pass
```

## 🐛 Troubleshooting

### Authentication Error
```bash
# Check API key is set
echo $ANTHROPIC_API_KEY

# Should output: sk-ant-api...
```

### Module Not Found
```bash
pip install anthropic
```

### Rate Limit Error
Wait 60 seconds and try again, or implement retry logic (see tutorial).

### Agent Not Using Tools
Improve tool descriptions - Claude needs clear docstrings explaining when and how to use each tool.

## 📚 Additional Resources

### Official Documentation
- [Claude API Docs](https://docs.anthropic.com/)
- [Python SDK](https://github.com/anthropics/anthropic-sdk-python)
- [Tool Use Guide](https://docs.anthropic.com/claude/docs/tool-use)

### Community
- [Anthropic Discord](https://anthropic.com/discord)
- [GitHub Issues](https://github.com/anthropics/anthropic-sdk-python/issues)

## 🎯 Prerequisites

- **Python**: 3.10 or higher
- **API Key**: From console.anthropic.com
- **Basic Python**: Functions, decorators, type hints
- **Optional**: Docker/Podman for containerized environment

## 💡 Tips for Success

1. **Start Simple** - Use the tool runner, not manual loops
2. **Test Tools First** - Verify each tool works independently
3. **Read Errors** - Error messages are helpful
4. **Monitor Costs** - Check usage in Anthropic Console
5. **Iterate** - Build, test, improve, repeat

## 🎉 Ready to Begin?

1. **Quick Start**: Read `QUICKSTART.md` and run `simple_agent_example.py`
2. **Deep Dive**: Study `AI_AGENT_GUIDE.md` for complete understanding
3. **Build**: Create your own agent using the patterns you learned

## 📄 License

This tutorial is provided as educational material. The code examples can be freely used and modified for your projects.

---

**Questions?** Check the troubleshooting sections in the guides or refer to the official Claude API documentation.

**Ready to build?** Start with `QUICKSTART.md` → Run `simple_agent_example.py` → Build your own agent!

Happy building! 🚀
