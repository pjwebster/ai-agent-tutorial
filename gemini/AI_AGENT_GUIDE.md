# Building AI Agents from Scratch with Gemini - Complete Guide

## 📚 What You'll Learn

This guide teaches you how to build AI agents using Google's Gemini API. By the end, you'll understand:

1. What makes an agent different from a simple chatbot
2. When to use agents vs. simpler approaches
3. How to define function declarations for Gemini
4. Manual vs. automatic function calling
5. Best practices for building production agents

---

## 🎯 What is an AI Agent?

### Simple Chatbot
```
User: "What's 2+2?"
Gemini: "4"
[DONE]
```

### AI Agent
```
User: "Research quantum computing and save a summary"
Gemini: [Decides what to do]
   → Calls web_search("quantum computing")
   → Analyzes results
   → Calls save_findings(...)
[DONE - Task completed autonomously]
```

**Key difference**: The agent decides what functions to use and when, creating a multi-step workflow to accomplish complex tasks.

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
- Gemini needs to decide what to do
- Open-ended exploration
- Requires multiple functions

**Example**: "Research this topic and create a report" (Gemini decides how)

**The Four Criteria** - All must be true:
1. ✅ **Complexity**: Multi-step, hard to specify upfront
2. ✅ **Value**: Worth the higher cost
3. ✅ **Viability**: Gemini is capable at this task
4. ✅ **Error tolerance**: Mistakes can be caught/fixed

---

## 🚀 Quick Start (5 minutes)

### 1. Install the SDK

```bash
pip install google-generativeai
```

### 2. Set Your API Key

```bash
export GOOGLE_API_KEY="your-api-key-here"
```

Get your API key from: https://aistudio.google.com/app/apikey

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
- How to define function declarations
- How the agent loop works
- Function calling and responses

**Time**: 10 minutes

---

### Step 2: Study `ai_agent_tutorial.py`
**What you'll learn:**
- Manual vs automatic function calling
- Function declaration design
- Multi-turn conversations

**Time**: 30 minutes

**Key sections:**
1. Function definitions and declarations
2. Simple agent (manual loop)
3. Automatic function calling
4. Conversational agent
5. Best practices

---

### Step 3: Build Your Own Agent

Pick one of these projects:

#### Project A: Research Assistant
**Functions needed:**
- `web_search(query)` - Search the web
- `summarize(text)` - Summarize content
- `save_report(title, content)` - Save findings

**Task**: "Research the latest AI developments and create a summary report"

#### Project B: Data Analysis Agent
**Functions needed:**
- `load_csv(filename)` - Load data
- `analyze(data, type)` - Run analysis
- `create_chart(data, chart_type)` - Visualize
- `save_results(filename, data)` - Export

**Task**: "Analyze sales_data.csv and create visualizations of trends"

#### Project C: File Manager Agent
**Functions needed:**
- `list_files(directory)` - List files
- `read_file(path)` - Read content
- `search_in_files(pattern)` - Search
- `organize_by_type()` - Organize files

**Task**: "Find all Python files, check for TODOs, and create a summary"

---

## 🛠️ Two Implementation Approaches

### Approach 1: Manual Function Calling (Recommended)

**When to use:**
- You need full control
- Want to log all function calls
- Need approval gates
- Debugging or development

**Pros:**
- Complete visibility
- Can add custom logic
- Better error handling
- Easier to debug

**Example:**
```python
import google.generativeai as genai

genai.configure(api_key=None)

# Define function
def my_tool(param: str) -> str:
    """Tool description."""
    return "result"

# Create declaration
tool_declaration = genai.protos.Tool(
    function_declarations=[
        genai.protos.FunctionDeclaration(
            name="my_tool",
            description="What this tool does",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "param": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="Parameter description"
                    ),
                },
                required=["param"]
            )
        ),
    ]
)

# Create model and chat
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    tools=[tool_declaration]
)

chat = model.start_chat(enable_automatic_function_calling=False)
response = chat.send_message("Do something")

# Manual loop
while True:
    # Check for function calls
    if response.candidates[0].content.parts[0].function_call:
        fn = response.candidates[0].content.parts[0].function_call
        
        # Execute function
        result = my_tool(**dict(fn.args))
        
        # Send result back
        response = chat.send_message([
            genai.protos.Part(
                function_response=genai.protos.FunctionResponse(
                    name=fn.name,
                    response={"result": result}
                )
            )
        ])
    else:
        # Done - print response
        print(response.text)
        break
```

---

### Approach 2: Automatic Function Calling

**When to use:**
- Simple use cases
- Don't need logging
- Trust Gemini's decisions

**Pros:**
- Less code
- Gemini handles the loop
- Simpler implementation

**Cons:**
- Less control
- Harder to debug
- Can't add approval gates

**Example:**
```python
# Enable automatic calling
chat = model.start_chat(enable_automatic_function_calling=True)

# Gemini handles everything
response = chat.send_message("Do something")
print(response.text)
```

**Note**: Automatic calling requires additional setup and may have limitations. See Gemini docs for details.

---

## 🎨 Function Declaration Design

### 1. Clear Structure
```python
# ❌ Bad - vague description
genai.protos.FunctionDeclaration(
    name="do_thing",
    description="Does something",
    ...
)

# ✅ Good - specific description
genai.protos.FunctionDeclaration(
    name="search_products",
    description="Search product catalog by name or keyword, returns matching products with pricing and availability",
    ...
)
```

### 2. Detailed Parameters
```python
# ✅ Good parameter schema
parameters=genai.protos.Schema(
    type=genai.protos.Type.OBJECT,
    properties={
        "query": genai.protos.Schema(
            type=genai.protos.Type.STRING,
            description="Product name or keyword to search for, e.g., 'laptop' or 'wireless mouse'"
        ),
        "category": genai.protos.Schema(
            type=genai.protos.Type.STRING,
            description="Product category filter: electronics, clothing, or all"
        ),
        "max_results": genai.protos.Schema(
            type=genai.protos.Type.INTEGER,
            description="Maximum number of results to return (1-20)"
        ),
    },
    required=["query"]
)
```

### 3. Return Structured Data
```python
import json

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
# ✅ Use Pro for complex reasoning
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

# ✅ Use Flash for speed and cost
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
```

### Safety Settings
```python
# Configure safety settings if needed
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    safety_settings={
        genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }
)
```

### Generation Config
```python
# Set temperature and other parameters
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config={
        "temperature": 0.7,
        "max_output_tokens": 2048,
    }
)
```

---

## 💰 Cost Optimization

### 1. Choose the Right Model

**Gemini 1.5 Pro:**
- Best for complex reasoning
- $1.25-$5.00/1M input tokens
- $5.00-$10.00/1M output tokens
- Context: up to 2M tokens

**Gemini 1.5 Flash:**
- 10x cheaper than Pro
- $0.075-$0.30/1M input tokens
- $0.30-$0.60/1M output tokens
- Good for simple tasks

```python
# For complex tasks
model = genai.GenerativeModel("gemini-1.5-pro")

# For simple/high-volume tasks
model = genai.GenerativeModel("gemini-1.5-flash")
```

### 2. Monitor Token Usage

```python
# Check token count
response = chat.send_message("Hello")
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
print(f"Total tokens: {response.usage_metadata.total_token_count}")
```

### 3. Use Caching

```python
# For repeated context, use caching
# Gemini supports context caching for large prompts
# See: https://ai.google.dev/docs/caching
```

---

## 🐛 Common Pitfalls

### 1. Infinite Loops
```python
# ❌ Bad - no limit
while True:
    response = chat.send_message(...)

# ✅ Good - has limit
max_iterations = 10
for i in range(max_iterations):
    response = chat.send_message(...)
```

### 2. Not Checking for Function Calls
```python
# ❌ Bad - assumes text response
print(response.text)

# ✅ Good - checks for function calls first
if response.candidates[0].content.parts[0].function_call:
    # Handle function call
    pass
else:
    print(response.text)
```

### 3. Poor Function Descriptions
```python
# ❌ Bad - Gemini won't know when to use this
genai.protos.FunctionDeclaration(
    name="tool",
    description="Does stuff",
    ...
)

# ✅ Good - clear purpose
genai.protos.FunctionDeclaration(
    name="validate_email",
    description="Check if an email address has valid format and domain. Returns validation status and error message if invalid.",
    ...
)
```

### 4. Missing Error Handling
```python
# ✅ Good - handles errors
def my_tool(param: str) -> str:
    try:
        # Implementation
        return json.dumps({"result": "success"})
    except Exception as e:
        return json.dumps({"error": str(e)})
```

---

## 📊 Example: Complete Production Agent

```python
import google.generativeai as genai
import json
from typing import Dict

genai.configure(api_key=None)

class ProductionAgent:
    """A production-ready agent with error handling and logging."""

    def __init__(self, max_iterations: int = 10):
        self.max_iterations = max_iterations
        self.setup_tools()
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            tools=[self.tools]
        )

    def setup_tools(self):
        """Define function declarations."""
        self.tools = genai.protos.Tool(
            function_declarations=[
                genai.protos.FunctionDeclaration(
                    name="search_database",
                    description="Search the product database by query",
                    parameters=genai.protos.Schema(
                        type=genai.protos.Type.OBJECT,
                        properties={
                            "query": genai.protos.Schema(
                                type=genai.protos.Type.STRING,
                                description="Search query"
                            ),
                        },
                        required=["query"]
                    )
                ),
            ]
        )

    def search_database(self, query: str) -> str:
        """Search implementation."""
        try:
            results = {"products": [], "count": 0}
            return json.dumps(results)
        except Exception as e:
            return json.dumps({"error": str(e)})

    def run(self, user_query: str) -> str:
        """Run the agent with error handling."""
        try:
            chat = self.model.start_chat(enable_automatic_function_calling=False)
            response = chat.send_message(user_query)

            for iteration in range(self.max_iterations):
                # Check for function calls
                has_function_call = any(
                    part.function_call 
                    for part in response.candidates[0].content.parts
                )

                if has_function_call:
                    # Execute functions
                    function_responses = []
                    
                    for part in response.candidates[0].content.parts:
                        if fn := part.function_call:
                            # Execute
                            result = self.search_database(**dict(fn.args))
                            
                            function_responses.append(
                                genai.protos.Part(
                                    function_response=genai.protos.FunctionResponse(
                                        name=fn.name,
                                        response={"result": result}
                                    )
                                )
                            )

                    response = chat.send_message(function_responses)
                else:
                    return response.text

            raise RuntimeError("Max iterations reached")

        except Exception as e:
            return f"Error: {str(e)}"

# Usage
agent = ProductionAgent()
result = agent.run("Search for laptops")
print(result)
```

---

## 🎓 Next Steps

1. ✅ Run the examples in this guide
2. ✅ Build one of the suggested projects
3. ✅ Read the official documentation:
   - https://ai.google.dev/docs
4. ✅ Explore advanced features:
   - Multimodal input (images, video, audio)
   - Long context (up to 2M tokens)
   - Code execution via custom tools
5. ✅ Join the community:
   - https://discord.gg/google-ai

---

## 📚 Additional Resources

### Files in This Tutorial
- `simple_agent_example.py` - Ready-to-run minimal example
- `ai_agent_tutorial.py` - Comprehensive tutorial with 3 approaches
- `QUICKSTART.md` - Quick start guide

### Official Documentation
- Gemini API Docs: https://ai.google.dev/docs
- Python SDK: https://github.com/google/generative-ai-python
- Function Calling Guide: https://ai.google.dev/docs/function_calling

### Example Projects
- Research assistant with web search
- Data analysis pipeline
- File management automation
- Customer support chatbot
- Code review agent

---

## ❓ Troubleshooting

### "API key not valid"
→ Check that `GOOGLE_API_KEY` is set correctly

### "Quota exceeded"
→ Check your API quota in AI Studio or wait for reset

### "Agent not calling functions"
→ Improve function descriptions, add examples in docstrings

### "Agent loops forever"
→ Add `max_iterations` limit and check for function calls properly

### "High costs"
→ Switch to Flash model, reduce max_output_tokens

---

## 🎉 You're Ready!

You now have everything you need to build AI agents from scratch with Gemini.

**Remember:**
- Start with manual function calling for control
- Test each function independently
- Use Flash for experimentation (cheaper)
- Monitor costs in AI Studio
- Have fun experimenting!

Happy building! 🚀
