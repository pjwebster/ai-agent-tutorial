# AI Agent Tutorial - Google Gemini

Build AI agents from scratch using Google's Gemini API and Python.

## 🚀 Quick Start

```bash
# Install dependencies
pip install google-generativeai

# Set your API key
export GOOGLE_API_KEY="your-api-key-here"

# Run the simple example
python simple_agent_example.py
```

Get your API key from: https://aistudio.google.com/app/apikey

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
3. Try manual and automatic function calling

### Advanced (4+ hours)
1. Build your own agent project
2. Implement custom functions
3. Experiment with different models (Pro vs Flash)

## 🔑 Core Pattern

```python
import google.generativeai as genai

# Configure API
genai.configure(api_key=None)  # Uses GOOGLE_API_KEY env var

# 1. Define your function
def my_tool(param: str) -> str:
    """What this tool does."""
    return "result"

# 2. Create function declaration
tool_declaration = genai.protos.Tool(
    function_declarations=[
        genai.protos.FunctionDeclaration(
            name="my_tool",
            description="Clear description",
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

# 3. Create model and chat
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    tools=[tool_declaration]
)

chat = model.start_chat(enable_automatic_function_calling=False)
response = chat.send_message("Do something")

# 4. Handle function calling
if fn := response.candidates[0].content.parts[0].function_call:
    result = my_tool(**dict(fn.args))
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

## 🐳 Container Support

```bash
# Build the container
podman build -t ai-agent-gemini -f Containerfile .

# Run it
podman run -it --rm -e GOOGLE_API_KEY="your-key" ai-agent-gemini
```

See `CONTAINER_GUIDE.md` for detailed container usage.

## 💰 Cost Awareness

**Gemini 1.5 Pro:**
- Input: $1.25-$5.00 per 1M tokens (based on context length)
- Output: $5.00-$10.00 per 1M tokens

**Gemini 1.5 Flash:**
- Input: $0.075-$0.30 per 1M tokens
- Output: $0.30-$0.60 per 1M tokens

**Typical costs for learning:**
- Simple query: ~$0.001-0.01
- Complex agent task: ~$0.02-0.20
- One hour of experimentation: ~$0.20-2

## 🎯 Key Features

- **Manual Function Calling**: Full control over execution
- **Automatic Function Calling**: Gemini handles the loop
- **Long Context**: Up to 2M tokens
- **Multimodal**: Text, images, video, audio
- **Multiple Models**: Pro (capable), Flash (fast/cheap)

## 📚 Additional Resources

- [Gemini API Docs](https://ai.google.dev/docs)
- [Python SDK](https://github.com/google/generative-ai-python)
- [Function Calling Guide](https://ai.google.dev/docs/function_calling)
- [Google AI Studio](https://aistudio.google.com/)

## 🎉 Ready to Begin?

1. **Quick Start**: Read `QUICKSTART.md` and run `simple_agent_example.py`
2. **Deep Dive**: Study `AI_AGENT_GUIDE.md` for complete understanding
3. **Build**: Create your own agent using the patterns you learned

---

**Looking for Anthropic Claude?** See the [`../anthropic/`](../anthropic/) directory for the Claude version of this tutorial.

Happy building! 🚀
