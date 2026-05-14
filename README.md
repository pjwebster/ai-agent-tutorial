# AI Agent Tutorial - Build Agents from Scratch

A comprehensive, hands-on tutorial for building AI agents using either **Claude API (Anthropic)** or **Gemini API (Google)**. Learn the fundamentals with your preferred LLM provider!

## 🎯 What You'll Learn

- What AI agents are and when to use them
- How to design and implement tools
- Different agent patterns and approaches
- Best practices for production agents
- Cost optimization and error handling

## 📁 Choose Your Tutorial

This project contains **two complete tutorials**, one for each LLM provider:

### 🤖 [Anthropic Claude Tutorial](./anthropic/)
Build agents with Claude API using the Anthropic SDK
- Tool runner with `@beta_tool` decorator
- Adaptive thinking and extended thinking
- Code execution and managed agents
- **Start here**: [`anthropic/QUICKSTART.md`](./anthropic/QUICKSTART.md)

### 🔷 [Google Gemini Tutorial](./gemini/)
Build agents with Gemini API using Google's SDK
- Function calling with schema declarations
- Gemini Pro and Gemini Flash models
- Vertex AI integration options
- **Start here**: [`gemini/QUICKSTART.md`](./gemini/QUICKSTART.md)

## 🚀 Quick Start

### For Claude/Anthropic:

```bash
cd anthropic
pip install anthropic
export ANTHROPIC_API_KEY="your-key"
python simple_agent_example.py
```

See: [`anthropic/QUICKSTART.md`](./anthropic/QUICKSTART.md)

### For Gemini/Google:

```bash
cd gemini
pip install google-generativeai
export GOOGLE_API_KEY="your-key"
python simple_agent_example.py
```

See: [`gemini/QUICKSTART.md`](./gemini/QUICKSTART.md)

## 📊 Feature Comparison

| Feature | Anthropic Claude | Google Gemini |
|---------|-----------------|---------------|
| **Tool Definition** | `@beta_tool` decorator | Schema dictionaries |
| **Automatic Loop** | Tool runner | Manual implementation |
| **Thinking Mode** | Adaptive thinking | Native reasoning |
| **Models** | Opus, Sonnet, Haiku | Gemini Pro, Flash, Ultra |
| **Code Execution** | Built-in server-side | Via custom tools |
| **Pricing** | $5-25/1M tokens | $0.50-7/1M tokens |
| **Context** | 200K-1M tokens | 128K-2M tokens |

## 🎓 Learning Path

Both tutorials follow the same structure:

1. **Quick Start** (30 min)
   - Read QUICKSTART.md
   - Run simple_agent_example.py
   - Modify a tool

2. **Deep Dive** (2 hours)
   - Read AI_AGENT_GUIDE.md
   - Study ai_agent_tutorial.py
   - Try different patterns

3. **Build** (4+ hours)
   - Create your own agent
   - Implement custom tools
   - Deploy to production

## 📦 What's Included (Per Tutorial)

Each directory contains:

- ✅ **Complete guides** (QUICKSTART, comprehensive guide, README)
- ✅ **Working examples** (simple and advanced)
- ✅ **Container support** (Containerfile, compose)
- ✅ **Development tools** (Makefile, scripts)

## 🔑 Getting API Keys

### Anthropic Claude:
1. Visit https://console.anthropic.com/
2. Create account and navigate to API Keys
3. Create a new key
4. Export: `export ANTHROPIC_API_KEY="sk-ant-..."`

### Google Gemini:
1. Visit https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Export: `export GOOGLE_API_KEY="AI..."`

## 🐳 Container Support

Both tutorials include containerized environments:

```bash
# Anthropic version
cd anthropic
podman build -t ai-agent-anthropic -f Containerfile .
podman run -it --rm -e ANTHROPIC_API_KEY="your-key" ai-agent-anthropic

# Gemini version
cd gemini
podman build -t ai-agent-gemini -f Containerfile .
podman run -it --rm -e GOOGLE_API_KEY="your-key" ai-agent-gemini
```

## 🎨 Example Projects (Work with Both)

### 1. Research Assistant
**Tools**: `web_search`, `analyze_data`, `save_findings`
**Task**: Research a topic and create a summary report

### 2. File Analyzer
**Tools**: `list_files`, `read_file`, `analyze_content`
**Task**: Analyze code files and generate documentation

### 3. Data Processor
**Tools**: `load_csv`, `analyze`, `create_chart`
**Task**: Process data and generate visualizations

## 🤔 Which Should I Choose?

### Choose **Anthropic Claude** if:
- ✅ You want the most capable reasoning (Opus)
- ✅ You need built-in code execution
- ✅ You prefer automatic tool runner
- ✅ You value extended thinking modes

### Choose **Google Gemini** if:
- ✅ You want lower cost (especially Flash)
- ✅ You need longer context (2M tokens)
- ✅ You're already using Google Cloud
- ✅ You prefer multimodal capabilities

### Try Both!
The tutorials teach the same concepts - you can learn with one and switch to the other easily.

## 📚 Resources

### Anthropic Claude
- [Claude API Docs](https://docs.anthropic.com/)
- [Python SDK](https://github.com/anthropics/anthropic-sdk-python)
- [Anthropic Discord](https://anthropic.com/discord)

### Google Gemini
- [Gemini API Docs](https://ai.google.dev/docs)
- [Python SDK](https://github.com/google/generative-ai-python)
- [Google AI Studio](https://aistudio.google.com/)

## 🛠️ Project Structure

```
ai-agent-tutorial/
├── README.md                 # This file
├── .gitignore               # Git ignore rules
├── anthropic/               # Claude/Anthropic tutorial
│   ├── QUICKSTART.md
│   ├── AI_AGENT_GUIDE.md
│   ├── README.md
│   ├── simple_agent_example.py
│   ├── ai_agent_tutorial.py
│   ├── Containerfile
│   └── ...
└── gemini/                  # Gemini/Google tutorial
    ├── QUICKSTART.md
    ├── AI_AGENT_GUIDE.md
    ├── README.md
    ├── simple_agent_example.py
    ├── ai_agent_tutorial.py
    ├── Containerfile
    └── ...
```

## 🐛 Troubleshooting

### Authentication Errors
- **Claude**: Check `ANTHROPIC_API_KEY` is set correctly
- **Gemini**: Check `GOOGLE_API_KEY` is set correctly

### Module Not Found
- **Claude**: `pip install anthropic`
- **Gemini**: `pip install google-generativeai`

### Rate Limits
- Both providers have rate limits - add retry logic
- See respective QUICKSTART guides for details

## 💰 Cost Estimates (Learning)

### Anthropic Claude:
- Simple examples: ~$0.01-0.05 each
- Complex tasks: ~$0.10-0.50 each
- One hour: ~$1-5 total

### Google Gemini:
- Simple examples: ~$0.001-0.01 each
- Complex tasks: ~$0.02-0.20 each
- One hour: ~$0.20-2 total

## 🎉 Get Started!

1. **Choose your provider** (Claude or Gemini)
2. **Navigate to that directory** (`cd anthropic` or `cd gemini`)
3. **Follow the QUICKSTART.md** in that directory
4. **Build your first agent!**

Both tutorials are complete and ready to use. Pick one and start learning! 🚀

## 📝 License

Educational material - code examples can be freely used and modified for your projects.

---

**Questions?** Check the troubleshooting sections in each tutorial's guide or refer to the official documentation.
