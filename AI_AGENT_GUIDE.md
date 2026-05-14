# Building AI Agents from Scratch - Complete Guide

## 📚 What You'll Learn

This guide teaches you how to build AI agents using Claude API. By the end, you'll understand:

1. What makes an agent different from a simple chatbot
2. When to use agents vs. simpler approaches
3. How to define tools for Claude to use
4. Two implementation approaches: Tool Runner (easy) and Manual Loop (advanced)
5. Best practices for building production agents

---

## 🎯 What is an AI Agent?

### Simple Chatbot
```
User: "What's 2+2?"
Claude: "4"
[DONE]
```

### AI Agent
```
User: "Research quantum computing and save a summary"
Claude: [Thinks: I need to search, then analyze, then save]
   → Calls web_search("quantum computing")
   → Analyzes results
   → Calls save_findings(...)
[DONE]
```

**Key difference**: The agent decides what tools to use and when, creating a multi-step workflow to accomplish complex tasks.

---

## 🤔 Should You Build an Agent?

Not every task needs an agent! Use this decision tree:

### Use a **Simple API Call** if:
- Single question/answer
- Classification task
- Simple extraction
- No tools needed

**Example**: "Summarize this document" → One API call

### Use a **Workflow** if:
- Multi-step process
- **You** control the flow
- Predetermined sequence

**Example**: Extract data → Validate → Save (you orchestrate each step)

### Use an **Agent** if:
- Multi-step with **unknown** sequence
- Claude needs to decide what to do
- Open-ended exploration
- Requires multiple tools

**Example**: "Research this topic and create a report" (Claude decides how)

**The Four Criteria** - All must be true:
1. ✅ **Complexity**: Multi-step, hard to specify upfront
2. ✅ **Value**: Worth the higher cost
3. ✅ **Viability**: Claude is capable at this task
4. ✅ **Error tolerance**: Mistakes can be caught/fixed

---

## 🚀 Quick Start (5 minutes)

### 1. Install the SDK

```bash
pip install anthropic
```

### 2. Set Your API Key

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Get your API key from: https://console.anthropic.com/

### 3. Run the Simple Example

```bash
python simple_agent_example.py
```

This shows a working agent with math calculations and time tools.

---

## 📖 Learning Path

Follow this sequence to build up your understanding:

### Step 1: Run `simple_agent_example.py`
**What you'll learn:**
- How to define tools with `@beta_tool`
- How the tool runner works
- Agent iteration and decision-making

**Time**: 10 minutes

---

### Step 2: Study `ai_agent_tutorial.py`
**What you'll learn:**
- Three different agent patterns
- Tool design best practices
- Manual loop vs. tool runner
- Multi-turn conversations

**Time**: 30 minutes

**Key sections:**
1. Tool definitions (`@beta_tool`)
2. Simple agent (tool runner)
3. Advanced agent (manual loop)
4. Conversational agent
5. Best practices

---

### Step 3: Build Your Own Agent

Pick one of these projects:

#### Project A: Research Assistant
**Tools needed:**
- `web_search(query)` - Search the web
- `summarize(text)` - Summarize content
- `save_report(title, content)` - Save findings

**Task**: "Research the latest AI developments and create a summary report"

#### Project B: Data Analysis Agent
**Tools needed:**
- `load_csv(filename)` - Load data
- `analyze(data, type)` - Run analysis
- `create_chart(data, chart_type)` - Visualize
- `save_results(filename, data)` - Export

**Task**: "Analyze sales_data.csv and create visualizations of trends"

#### Project C: File Manager Agent
**Tools needed:**
- `list_files(directory)` - List files
- `read_file(path)` - Read content
- `search_in_files(pattern)` - Search
- `organize_by_type()` - Organize files

**Task**: "Find all Python files, check for TODOs, and create a summary"

---

## 🛠️ Two Implementation Approaches

### Approach 1: Tool Runner (Recommended)

**When to use:**
- Most use cases
- You want simplicity
- Standard tool execution

**Pros:**
- Automatic loop handling
- Type-safe with decorators
- Less code to write

**Example:**
```python
from anthropic import beta_tool

@beta_tool
def my_tool(param: str) -> str:
    """Tool description."""
    return "result"

runner = client.beta.messages.tool_runner(
    model="claude-opus-4-7",
    max_tokens=16000,
    tools=[my_tool],
    messages=[{"role": "user", "content": "Do something"}],
)

for message in runner:
    # Handle each iteration
    pass
```

---

### Approach 2: Manual Loop (Advanced)

**When to use:**
- Need approval gates ("confirm before executing")
- Custom logging/monitoring
- Conditional tool execution
- Integration with existing systems

**Pros:**
- Complete control
- Can add middleware
- Custom error handling

**Example:**
```python
while True:
    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=16000,
        tools=tools,
        messages=messages
    )

    if response.stop_reason == "end_turn":
        break  # Done

    # Extract tool calls
    tool_blocks = [b for b in response.content if b.type == "tool_use"]

    # Execute tools (with custom logic)
    for tool in tool_blocks:
        if needs_approval(tool.name):
            if not get_user_approval():
                continue
        result = execute_tool(tool.name, tool.input)
        # ... append results and continue
```

---

## 🎨 Tool Design Best Practices

### 1. Single Responsibility
```python
# ❌ Bad - does too much
@beta_tool
def process_data(data: str, mode: str):
    """Process data in various ways."""
    pass

# ✅ Good - focused purpose
@beta_tool
def validate_data(data: str) -> str:
    """Validate data format."""
    pass

@beta_tool
def transform_data(data: str) -> str:
    """Transform data to new format."""
    pass
```

### 2. Clear Descriptions
```python
# ❌ Bad - vague
@beta_tool
def search(query: str):
    """Search for stuff."""
    pass

# ✅ Good - specific
@beta_tool
def search_products(query: str, category: str = "all") -> str:
    """Search product catalog by name or keyword.

    Args:
        query: Product name or keyword to search for.
        category: Product category filter (e.g., "electronics", "clothing", "all").

    Returns:
        JSON list of matching products with name, price, and availability.
    """
    pass
```

### 3. Type Hints
```python
# ✅ Type hints generate better schemas
@beta_tool
def book_flight(
    destination: str,
    date: str,
    passengers: int,
    class_type: str = "economy"
) -> str:
    """Book a flight."""
    pass
```

### 4. Return Structured Data
```python
import json

@beta_tool
def get_weather(location: str) -> str:
    """Get weather for a location."""
    result = {
        "location": location,
        "temperature": 72,
        "conditions": "sunny",
        "humidity": 45
    }
    return json.dumps(result)  # ✅ Return JSON
```

---

## ⚙️ Configuration Best Practices

### Model Selection
```python
# ✅ Default to Opus 4.7 for best results
model = "claude-opus-4-7"  # $5/$25 per 1M tokens

# Use Sonnet for high-volume production
model = "claude-sonnet-4-6"  # $3/$15 per 1M tokens

# Use Haiku only for simple tasks
model = "claude-haiku-4-5"  # $1/$5 per 1M tokens
```

### Thinking & Effort
```python
# ✅ Use adaptive thinking for complex tasks
thinking={"type": "adaptive"}

# ✅ Set effort level
output_config={"effort": "high"}  # low | medium | high | max | xhigh

# high = good balance for most tasks
# max = best quality, higher cost (Opus only)
# xhigh = optimal for coding on Opus 4.7
```

### Max Tokens
```python
# ✅ Set appropriately for your task
max_tokens=16000  # For detailed responses
max_tokens=4000   # For concise responses
max_tokens=1024   # For simple extractions
```

### Error Prevention
```python
# ✅ Always set iteration limits
max_iterations = 10  # Prevent infinite loops

# ✅ Handle all stop reasons
if response.stop_reason == "end_turn":
    # Success
elif response.stop_reason == "max_tokens":
    # Increase max_tokens
elif response.stop_reason == "pause_turn":
    # Continue iteration
```

---

## 💰 Cost Optimization

### 1. Use Prompt Caching
```python
# Cache large context (e.g., documentation, code)
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=16000,
    cache_control={"type": "ephemeral"},  # Auto-cache
    system=large_system_prompt,
    messages=[{"role": "user", "content": query}]
)

# First call: Full cost
# Subsequent calls: ~90% cheaper for cached portion
```

### 2. Choose the Right Model
- **Opus 4.7**: Best for complex reasoning, agentic tasks, coding
- **Sonnet 4.6**: Good for production workloads, standard tasks
- **Haiku 4.5**: Fast and cheap for simple classification

### 3. Monitor Token Usage
```python
count = client.messages.count_tokens(
    model="claude-opus-4-7",
    messages=messages,
    system=system
)
print(f"Input tokens: {count.input_tokens}")
print(f"Estimated cost: ${count.input_tokens * 0.000005:.4f}")
```

---

## 🐛 Common Pitfalls

### 1. Infinite Loops
```python
# ❌ Bad - no limit
while True:
    response = client.messages.create(...)

# ✅ Good - has limit
max_iterations = 10
for i in range(max_iterations):
    response = client.messages.create(...)
```

### 2. Not Handling All Stop Reasons
```python
# ❌ Bad - only checks end_turn
if response.stop_reason == "end_turn":
    break

# ✅ Good - handles all cases
if response.stop_reason == "end_turn":
    break
elif response.stop_reason == "pause_turn":
    continue
elif response.stop_reason == "max_tokens":
    print("Warning: Hit token limit")
    break
```

### 3. Poor Tool Descriptions
```python
# ❌ Bad - Claude won't know when to use this
@beta_tool
def do_thing(data: str):
    """Does a thing."""
    pass

# ✅ Good - clear purpose and usage
@beta_tool
def validate_email(email: str) -> str:
    """Check if an email address is valid.

    Args:
        email: Email address to validate (e.g., "user@example.com").

    Returns:
        JSON with {"valid": bool, "reason": str}.
    """
    pass
```

### 4. Forgetting to Preserve Full Content
```python
# ❌ Bad - loses compaction state
messages.append({
    "role": "assistant",
    "content": response.content[0].text  # Only text!
})

# ✅ Good - preserves all blocks
messages.append({
    "role": "assistant",
    "content": response.content  # Full content
})
```

---

## 📊 Example: Complete Agent Implementation

Here's a complete, production-ready agent:

```python
import anthropic
from anthropic import beta_tool
import json
from typing import List

class ProductionAgent:
    """A production-ready agent with error handling and logging."""

    def __init__(self, max_iterations: int = 10):
        self.client = anthropic.Anthropic()
        self.max_iterations = max_iterations
        self.conversation_history = []

    @beta_tool
    def search_database(query: str, limit: int = 10) -> str:
        """Search the product database."""
        try:
            # Your search logic here
            results = {"products": [], "count": 0}
            return json.dumps(results)
        except Exception as e:
            return json.dumps({"error": str(e)})

    def run(self, user_query: str) -> str:
        """Run the agent with error handling."""
        try:
            runner = self.client.beta.messages.tool_runner(
                model="claude-opus-4-7",
                max_tokens=16000,
                thinking={"type": "adaptive"},
                output_config={"effort": "high"},
                tools=[self.search_database],
                messages=[{"role": "user", "content": user_query}],
            )

            iteration = 0
            final_message = None

            for message in runner:
                iteration += 1
                final_message = message

                if iteration >= self.max_iterations:
                    raise RuntimeError("Max iterations reached")

            # Extract response
            response_text = ""
            for block in final_message.content:
                if block.type == "text":
                    response_text += block.text

            return response_text

        except anthropic.BadRequestError as e:
            return f"Error: Invalid request - {e.message}"
        except anthropic.RateLimitError as e:
            return "Error: Rate limited. Please try again later."
        except Exception as e:
            return f"Error: {str(e)}"
```

---

## 🎓 Next Steps

1. ✅ Run the examples in this guide
2. ✅ Build one of the suggested projects
3. ✅ Read the official documentation:
   - https://docs.anthropic.com/
4. ✅ Explore advanced features:
   - Streaming responses
   - Managed Agents (server-hosted agents)
   - Code execution tool
   - Structured outputs
5. ✅ Join the community:
   - https://github.com/anthropics/anthropic-sdk-python

---

## 📚 Additional Resources

### Files in This Tutorial
- `simple_agent_example.py` - Ready-to-run minimal example
- `ai_agent_tutorial.py` - Comprehensive tutorial with 3 approaches
- `AI_AGENT_GUIDE.md` - This guide

### Official Documentation
- Claude API Docs: https://docs.anthropic.com/
- Python SDK: https://github.com/anthropics/anthropic-sdk-python
- Tool Use Guide: https://docs.anthropic.com/claude/docs/tool-use

### Example Projects
- Research assistant with web search
- Data analysis pipeline
- File management automation
- Customer support chatbot
- Code review agent

---

## ❓ Troubleshooting

### "Authentication Error"
→ Check that `ANTHROPIC_API_KEY` is set correctly

### "Rate Limit Error"
→ Add exponential backoff retry logic or wait 60 seconds

### "Agent not calling tools"
→ Improve tool descriptions, add examples in docstrings

### "Agent loops forever"
→ Add `max_iterations` limit and check stop reasons

### "High costs"
→ Use prompt caching, choose cheaper model, reduce max_tokens

---

## 🎉 You're Ready!

You now have everything you need to build AI agents from scratch. Start with the simple example, experiment with different tools, and gradually build more complex agents.

**Remember:**
- Start simple (use tool runner)
- Test each tool independently
- Monitor costs and token usage
- Use adaptive thinking for complex tasks
- Handle errors gracefully

Happy building! 🚀
