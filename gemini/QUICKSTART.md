# 🎓 AI Agent Tutorial with Gemini - Quick Start Guide

Your complete learning package to build AI agents from scratch using Google Gemini API.

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
   - Manual function calling (recommended)
   - Automatic function calling
   - Multi-turn conversations
   - Production patterns

---

## 🚀 Quick Start (Right Now!)

```bash
# 1. Install the SDK
pip install google-generativeai

# 2. Set your API key
export GOOGLE_API_KEY="your-api-key"

# 3. Run the simple example
python simple_agent_example.py
```

Get your API key from: https://aistudio.google.com/app/apikey

---

## 📖 Recommended Learning Path

### Day 1 (30 mins)
1. Read the "What is an AI Agent?" section in `AI_AGENT_GUIDE.md`
2. Run `simple_agent_example.py`
3. Modify one tool and see how it changes behavior

### Day 2 (1 hour)
1. Study `ai_agent_tutorial.py`
2. Try the different examples (simple, automatic, conversational)
3. Read the "Function Declaration Design" section

### Day 3 (2-3 hours)
1. Build your own agent (pick a project from the guide)
2. Implement 2-3 custom tools
3. Experiment with different models (Pro vs Flash)

---

## 🎯 Key Concepts You'll Master

1. **Function Declarations** - How to define functions Gemini can call
2. **Agent Loop** - The request → function call → result → repeat pattern
3. **Manual vs Automatic** - Manual loop (control) vs automatic calling (convenience)
4. **Multi-turn Conversations** - Maintaining state across interactions
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
import google.generativeai as genai

# Configure API
genai.configure(api_key=None)  # Uses GOOGLE_API_KEY env var

# 1. Define your function
def my_tool(param: str) -> str:
    """What this tool does."""
    return "result"

# 2. Create function declaration
my_tool_declaration = genai.protos.Tool(
    function_declarations=[
        genai.protos.FunctionDeclaration(
            name="my_tool",
            description="Clear description of what this does",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "param": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="What this parameter is for"
                    ),
                },
                required=["param"]
            )
        ),
    ]
)

# 3. Create model with tools
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    tools=[my_tool_declaration]
)

# 4. Start chat and handle function calling
chat = model.start_chat(enable_automatic_function_calling=False)
response = chat.send_message("Do something")

# 5. Manual loop to execute functions
if response.candidates[0].content.parts[0].function_call:
    fn = response.candidates[0].content.parts[0].function_call
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

print(response.text)
```

---

## ⚡ Running Your First Agent

### Step 1: Create a file `my_first_agent.py`

```python
import google.generativeai as genai
import math

genai.configure(api_key=None)

# Define your function
def calculate(expression: str) -> str:
    """Evaluate a math expression like '2 + 2' or 'sqrt(16)'."""
    try:
        result = eval(expression, {"__builtins__": {}}, 
                     {"sqrt": math.sqrt, "pi": math.pi})
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

# Create function declaration
calc_tool = genai.protos.Tool(
    function_declarations=[
        genai.protos.FunctionDeclaration(
            name="calculate",
            description="Evaluate a mathematical expression",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "expression": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="Math expression to evaluate"
                    ),
                },
                required=["expression"]
            )
        ),
    ]
)

# Create model and chat
model = genai.GenerativeModel(model_name="gemini-1.5-pro", tools=[calc_tool])
chat = model.start_chat(enable_automatic_function_calling=False)

# Send query
response = chat.send_message("What is the square root of 144?")

# Handle function call
if fn := response.candidates[0].content.parts[0].function_call:
    result = calculate(**dict(fn.args))
    response = chat.send_message([
        genai.protos.Part(
            function_response=genai.protos.FunctionResponse(
                name=fn.name,
                response={"result": result}
            )
        )
    ])

print(response.text)
```

### Step 2: Run it

```bash
python my_first_agent.py
```

### Step 3: Experiment

Try changing the query to:
- "Calculate the area of a circle with radius 5"
- "What's 15% of 200?"
- "Solve: sqrt(64) + 2^3"

---

## 🎓 What's Next?

1. ✅ **Run `simple_agent_example.py`** - See a working agent
2. ✅ **Read `AI_AGENT_GUIDE.md`** - Learn the concepts deeply
3. ✅ **Study `ai_agent_tutorial.py`** - See different patterns
4. ✅ **Build your own project** - Apply what you learned
5. ✅ **Explore advanced features** - Multimodal, long context, code execution

---

## 🐛 Troubleshooting

### "Authentication Error" or "API key not valid"
→ Check that `GOOGLE_API_KEY` is set correctly
```bash
echo $GOOGLE_API_KEY  # Should show your key
```

### "Module not found: google.generativeai"
→ Install the SDK
```bash
pip install google-generativeai
```

### "Quota exceeded" or Rate Limit Error
→ Wait 60 seconds or check your API quota in AI Studio

### "Agent not calling functions"
→ Improve function descriptions - Gemini needs clear declarations

### "Function not found"
→ Check that function name in declaration matches your actual function

---

## 💰 Cost Awareness

**Gemini 1.5 Pro Pricing:**
- Input: $1.25 per 1M tokens (≤128K), $2.50 (128K-1M), $5.00 (1M-2M)
- Output: $5.00 per 1M tokens (≤128K), $10.00 (128K-2M)

**Gemini 1.5 Flash Pricing:**
- Input: $0.075 per 1M tokens (≤128K), $0.15 (128K-1M), $0.30 (1M-2M)
- Output: $0.30 per 1M tokens (≤128K), $0.60 (128K-2M)

**Typical costs for learning:**
- Simple query: ~$0.001-0.01
- Complex agent task: ~$0.02-0.20
- One hour of experimentation: ~$0.20-2

**Tips to save:**
- Use Flash for simple tasks
- Monitor usage in AI Studio
- Cache context when possible

---

## 📚 Additional Resources

### Official Documentation
- Gemini API Docs: https://ai.google.dev/docs
- Python SDK: https://github.com/google/generative-ai-python
- Function Calling Guide: https://ai.google.dev/docs/function_calling

### Get Help
- Google AI Discord: https://discord.gg/google-ai
- Stack Overflow: Tag `google-gemini-api`

---

## 🎉 You're Ready!

You now have everything you need to start building AI agents with Gemini.

**Remember:**
- Start with manual function calling for better control
- Test each function independently
- Read error messages carefully
- Use Flash for experimentation (cheaper)
- Have fun experimenting!

**Ready to start?** Open `simple_agent_example.py` and run it. You'll see a working agent in action within minutes!

---

Happy building! 🚀
