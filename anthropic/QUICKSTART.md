# 🎓 AI Agent Tutorial - Quick Start Guide

Your complete learning package to build AI agents from scratch using Claude API.

---

## 📁 Files in This Tutorial

1. **`AI_AGENT_GUIDE.md`** - Your main learning resource
   - What agents are and when to use them
   - Complete decision tree
   - Best practices and patterns
   - Cost optimization strategies
   - Troubleshooting guide

2. **`simple_agent_example.py`** - Start here!
   - Ready-to-run working agent
   - Math calculator + time tools
   - Shows the complete flow
   - Takes ~5 minutes to try

3. **`ai_agent_tutorial.py`** - Deep dive
   - Three different implementation approaches
   - Tool runner vs manual loop
   - Multi-turn conversations
   - Production patterns

---

## 🚀 Quick Start (Right Now!)

```bash
# 1. Install the SDK
pip install anthropic

# 2. Set your API key
export ANTHROPIC_API_KEY="your-api-key"

# 3. Run the simple example
python simple_agent_example.py
```

Get your API key from: https://console.anthropic.com/

---

## 📖 Recommended Learning Path

### Day 1 (30 mins)
1. Read the "What is an AI Agent?" section in `AI_AGENT_GUIDE.md`
2. Run `simple_agent_example.py`
3. Modify one tool and see how it changes behavior

### Day 2 (1 hour)
1. Study `ai_agent_tutorial.py`
2. Try the different examples (simple, advanced, conversational)
3. Read the "Tool Design Best Practices" section

### Day 3 (2-3 hours)
1. Build your own agent (pick a project from the guide)
2. Implement 2-3 custom tools
3. Experiment with different effort levels and thinking modes

---

## 🎯 Key Concepts You'll Master

1. **Tool Design** - How to create functions Claude can call
2. **Agent Loop** - The request → tool call → result → repeat pattern
3. **Tool Runner** - Automatic loop handling (easiest)
4. **Manual Loop** - Fine-grained control (advanced)
5. **Best Practices** - Error handling, cost optimization, testing

---

## 💡 What Makes a Good First Project?

Start with something like:

- **File analyzer** - Read files, extract info, create summary
- **Research assistant** - Search, analyze, save findings
- **Data processor** - Load CSV, analyze, create charts

Keep it simple: 3-4 tools, clear goal, easy to test.

---

## 🔑 Core Pattern (Agent Basics)

Here's the fundamental pattern for building an agent:

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
    for block in message.content:
        if block.type == "text":
            print(block.text)
        elif block.type == "tool_use":
            print(f"Calling: {block.name}")
```

That's it! The SDK handles the complex loop logic for you.

---

## 🎨 Example: Define a Tool

```python
from anthropic import beta_tool
import json

@beta_tool
def search_products(query: str, category: str = "all") -> str:
    """Search product catalog by name or keyword.

    Args:
        query: Product name or keyword to search for.
        category: Product category filter (e.g., "electronics", "clothing", "all").

    Returns:
        JSON list of matching products with name, price, and availability.
    """
    # Your implementation here
    results = {
        "products": [
            {"name": "Widget", "price": 19.99, "available": True},
            {"name": "Gadget", "price": 29.99, "available": False}
        ],
        "count": 2
    }
    return json.dumps(results)
```

**Key points:**
- Use `@beta_tool` decorator
- Add type hints (generates better schemas)
- Write clear docstrings (Claude reads these!)
- Return JSON for structured data

---

## ⚡ Running Your First Agent

### Step 1: Create a file `my_first_agent.py`

```python
import anthropic
from anthropic import beta_tool
import math

@beta_tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression like '2 + 2' or 'sqrt(16)'."""
    try:
        result = eval(expression, {"__builtins__": {}}, {"sqrt": math.sqrt, "pi": math.pi})
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

client = anthropic.Anthropic()

runner = client.beta.messages.tool_runner(
    model="claude-opus-4-7",
    max_tokens=16000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},
    tools=[calculate],
    messages=[{"role": "user", "content": "What is the square root of 144?"}],
)

for message in runner:
    for block in message.content:
        if block.type == "text":
            print(block.text)
```

### Step 2: Run it

```bash
python my_first_agent.py
```

### Step 3: Experiment

Try changing the user query to:
- "Calculate the area of a circle with radius 5"
- "What's 15% of 200?"
- "Solve: sqrt(64) + 2^3"

---

## 🎓 What's Next?

1. ✅ **Run `simple_agent_example.py`** - See a working agent
2. ✅ **Read `AI_AGENT_GUIDE.md`** - Learn the concepts deeply
3. ✅ **Study `ai_agent_tutorial.py`** - See different patterns
4. ✅ **Build your own project** - Apply what you learned
5. ✅ **Explore advanced features** - Code execution, streaming, managed agents

---

## 🐛 Troubleshooting

### "Authentication Error"
→ Check that `ANTHROPIC_API_KEY` is set correctly
```bash
echo $ANTHROPIC_API_KEY  # Should show your key
```

### "Module not found: anthropic"
→ Install the SDK
```bash
pip install anthropic
```

### "Rate Limit Error"
→ Wait 60 seconds or add retry logic (see tutorial files)

### "Agent not calling tools"
→ Improve tool descriptions - Claude needs clear docstrings

### "Agent loops forever"
→ This shouldn't happen with tool runner, but check the advanced examples for manual loop controls

---

## 💰 Cost Awareness

**Opus 4.7 Pricing:**
- Input: $5 per 1M tokens
- Output: $25 per 1M tokens

**Typical costs for learning:**
- Simple query: ~$0.01-0.05
- Complex agent task: ~$0.10-0.50
- One hour of experimentation: ~$1-5

**Tips to save:**
- Use prompt caching for repeated context
- Set appropriate `max_tokens` limits
- Monitor usage in the Anthropic Console

---

## 📚 Additional Resources

### Official Documentation
- Claude API Docs: https://docs.anthropic.com/
- Python SDK: https://github.com/anthropics/anthropic-sdk-python
- Tool Use Guide: https://docs.anthropic.com/claude/docs/tool-use

### Get Help
- Anthropic Discord: https://anthropic.com/discord
- GitHub Issues: https://github.com/anthropics/anthropic-sdk-python/issues

---

## 🎉 You're Ready!

You now have everything you need to start building AI agents.

**Remember:**
- Start simple (use the tool runner)
- Test each tool independently
- Read error messages carefully
- Use adaptive thinking for complex tasks
- Have fun experimenting!

**Ready to start?** Open `simple_agent_example.py` and run it. You'll see a working agent in action within minutes!

---

Happy building! 🚀
