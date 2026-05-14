"""
AI Agent Tutorial: Building from Scratch
=========================================

This tutorial teaches you to build an AI agent step by step.
We'll create a research assistant that can search the web and analyze data.

Prerequisites:
- pip install anthropic
- Set ANTHROPIC_API_KEY environment variable
"""

import anthropic
from anthropic import beta_tool
import json
from typing import List, Dict

# ==============================================================================
# STEP 1: Understanding the Basics
# ==============================================================================
# An AI agent is different from a simple chatbot:
# - Chatbot: User asks → Claude answers → Done
# - Agent: User asks → Claude decides what tools to use → Executes tools →
#          Claude analyzes results → Repeats until task is complete

# ==============================================================================
# STEP 2: Define Your Tools
# ==============================================================================
# Tools are functions that Claude can call to interact with the world.
# Use the @beta_tool decorator to automatically generate schemas.

@beta_tool
def web_search(query: str, max_results: int = 5) -> str:
    """Search the web for information.

    Args:
        query: The search query string.
        max_results: Maximum number of results to return (1-10).
    """
    # In a real implementation, this would call a search API
    # For this tutorial, we'll simulate results
    return json.dumps({
        "results": [
            {
                "title": f"Result for '{query}' #{i+1}",
                "snippet": f"Information about {query}...",
                "url": f"https://example.com/result{i+1}"
            }
            for i in range(min(max_results, 3))
        ]
    })


@beta_tool
def analyze_data(data: str, analysis_type: str = "summary") -> str:
    """Analyze provided data.

    Args:
        data: The data to analyze (as JSON string or text).
        analysis_type: Type of analysis - "summary", "statistics", or "trends".
    """
    # In a real implementation, this would perform actual analysis
    # For this tutorial, we'll simulate analysis
    return f"Analysis ({analysis_type}): The data shows interesting patterns..."


@beta_tool
def save_findings(title: str, content: str, tags: List[str]) -> str:
    """Save research findings to a file.

    Args:
        title: Title of the findings.
        content: The content to save.
        tags: List of tags for categorization.
    """
    filename = f"findings_{title.replace(' ', '_').lower()}.txt"
    with open(filename, 'w') as f:
        f.write(f"Title: {title}\n")
        f.write(f"Tags: {', '.join(tags)}\n")
        f.write(f"\n{content}\n")
    return f"Findings saved to {filename}"


# ==============================================================================
# STEP 3: Create the Agent (Using Tool Runner - Recommended)
# ==============================================================================
# The tool runner automatically handles the agent loop for you.

def simple_agent_example():
    """Example using the tool runner (easiest approach)."""
    print("\n" + "="*70)
    print("SIMPLE AGENT EXAMPLE (Tool Runner)")
    print("="*70)

    client = anthropic.Anthropic()

    # Create the tool runner - it handles everything automatically
    runner = client.beta.messages.tool_runner(
        model="claude-opus-4-7",
        max_tokens=16000,
        thinking={"type": "adaptive"},  # Enable adaptive thinking
        output_config={"effort": "high"},  # Set effort level
        tools=[web_search, analyze_data, save_findings],
        messages=[{
            "role": "user",
            "content": "Research the latest developments in quantum computing and save your findings."
        }],
    )

    # The runner yields a message on each iteration
    # It automatically loops until Claude is done
    for message in runner:
        print("\n--- Agent Iteration ---")
        for block in message.content:
            if block.type == "thinking":
                print(f"[THINKING]: {block.thinking[:100]}...")
            elif block.type == "text":
                print(f"[RESPONSE]: {block.text}")
            elif block.type == "tool_use":
                print(f"[TOOL CALL]: {block.name}({block.input})")

    print("\n✓ Agent completed its task!")


# ==============================================================================
# STEP 4: Manual Agent Loop (Advanced - More Control)
# ==============================================================================
# Use this when you need fine-grained control: logging, approval gates, etc.

def advanced_agent_example():
    """Example using manual loop (maximum control)."""
    print("\n" + "="*70)
    print("ADVANCED AGENT EXAMPLE (Manual Loop)")
    print("="*70)

    client = anthropic.Anthropic()

    # Define tools as dictionaries (manual approach)
    tools = [
        {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and state, e.g., San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit"
                    }
                },
                "required": ["location"]
            }
        }
    ]

    messages = [{
        "role": "user",
        "content": "What's the weather like in San Francisco and New York? Compare them."
    }]

    iteration = 0
    max_iterations = 10  # Prevent infinite loops

    # Manual agent loop
    while iteration < max_iterations:
        iteration += 1
        print(f"\n--- Iteration {iteration} ---")

        response = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=16000,
            thinking={"type": "adaptive"},
            tools=tools,
            messages=messages
        )

        print(f"Stop reason: {response.stop_reason}")

        # If Claude is done, break
        if response.stop_reason == "end_turn":
            for block in response.content:
                if block.type == "text":
                    print(f"\n[FINAL RESPONSE]: {block.text}")
            break

        # If hit iteration limit, continue
        if response.stop_reason == "pause_turn":
            messages.append({"role": "assistant", "content": response.content})
            continue

        # Extract tool use blocks
        tool_use_blocks = [b for b in response.content if b.type == "tool_use"]

        if not tool_use_blocks:
            break

        # Append assistant's response
        messages.append({"role": "assistant", "content": response.content})

        # Execute each tool
        tool_results = []
        for tool in tool_use_blocks:
            print(f"[EXECUTING TOOL]: {tool.name}")
            print(f"[TOOL INPUT]: {tool.input}")

            # Execute tool (simplified - just return mock data)
            result = execute_tool_function(tool.name, tool.input)

            print(f"[TOOL RESULT]: {result}")

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool.id,
                "content": result
            })

        # Append tool results
        messages.append({"role": "user", "content": tool_results})

    if iteration >= max_iterations:
        print("\n⚠ Reached maximum iterations")
    else:
        print("\n✓ Agent completed its task!")


def execute_tool_function(tool_name: str, tool_input: Dict) -> str:
    """Execute a tool function and return the result."""
    if tool_name == "get_weather":
        location = tool_input.get("location", "Unknown")
        unit = tool_input.get("unit", "fahrenheit")
        # Mock weather data
        temp = "72°F" if unit == "fahrenheit" else "22°C"
        return f"Weather in {location}: {temp}, partly cloudy"

    return f"Tool {tool_name} not implemented"


# ==============================================================================
# STEP 5: Multi-Turn Conversation Agent
# ==============================================================================

class ConversationalAgent:
    """An agent that maintains conversation state across multiple interactions."""

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.messages = []
        self.tools = [web_search, analyze_data, save_findings]

    def chat(self, user_message: str) -> str:
        """Send a message to the agent and get a response."""
        print(f"\n[USER]: {user_message}")

        # Add user message
        self.messages.append({
            "role": "user",
            "content": user_message
        })

        # Run the agent
        runner = self.client.beta.messages.tool_runner(
            model="claude-opus-4-7",
            max_tokens=16000,
            thinking={"type": "adaptive"},
            output_config={"effort": "high"},
            tools=self.tools,
            messages=self.messages,
        )

        final_message = None
        for message in runner:
            final_message = message
            # You could stream updates here

        # Extract final response
        response_text = ""
        for block in final_message.content:
            if block.type == "text":
                response_text += block.text

        # Update conversation history
        self.messages.append({
            "role": "assistant",
            "content": final_message.content
        })

        print(f"[AGENT]: {response_text}")
        return response_text


def conversational_agent_example():
    """Example of a multi-turn conversational agent."""
    print("\n" + "="*70)
    print("CONVERSATIONAL AGENT EXAMPLE")
    print("="*70)

    agent = ConversationalAgent()

    # Have a multi-turn conversation
    agent.chat("Search for information about AI agents.")
    agent.chat("Now analyze what you found and identify the key concepts.")
    agent.chat("Save your analysis with tags 'AI', 'agents', 'tutorial'.")


# ==============================================================================
# STEP 6: Best Practices & Tips
# ==============================================================================

def best_practices():
    """Print best practices for building agents."""
    print("\n" + "="*70)
    print("BEST PRACTICES FOR BUILDING AI AGENTS")
    print("="*70)

    practices = """
    1. START SIMPLE
       - Use the tool runner (beta_tool) for most cases
       - Only use manual loops when you need fine-grained control

    2. TOOL DESIGN
       - Make tools focused and single-purpose
       - Use clear, descriptive names and docstrings
       - Include type hints - they generate better schemas
       - Return JSON for structured data

    3. ERROR HANDLING
       - Always validate tool inputs
       - Return clear error messages to Claude
       - Use is_error flag in tool results
       - Set max_iterations to prevent infinite loops

    4. COST OPTIMIZATION
       - Use prompt caching for repeated context
       - Start with claude-opus-4-7 for best results
       - Use adaptive thinking instead of fixed budgets
       - Set appropriate effort levels (high for complex tasks)

    5. TESTING
       - Test each tool independently first
       - Start with simple queries before complex ones
       - Monitor token usage and costs
       - Log agent behavior for debugging

    6. WHEN TO USE AGENTS
       ✓ Multi-step tasks that need dynamic planning
       ✓ Tasks requiring multiple tool calls
       ✓ Open-ended exploration and research
       ✗ Simple classification or extraction
       ✗ Single-step operations
       ✗ Tasks that can be hard-coded
    """
    print(practices)


# ==============================================================================
# MAIN: Run the Tutorial
# ==============================================================================

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║         AI AGENT TUTORIAL - Building Agents from Scratch         ║
    ╚══════════════════════════════════════════════════════════════════╝

    This tutorial demonstrates three approaches to building AI agents:

    1. Simple Agent (Tool Runner) - RECOMMENDED for most use cases
    2. Advanced Agent (Manual Loop) - For fine-grained control
    3. Conversational Agent - For multi-turn interactions

    Make sure you have:
    - Installed: pip install anthropic
    - Set environment variable: ANTHROPIC_API_KEY
    """)

    # Print best practices
    best_practices()

    print("\n" + "="*70)
    print("READY TO RUN EXAMPLES")
    print("="*70)
    print("""
    Uncomment the examples below to run them:

    # simple_agent_example()           # Easiest - let the SDK handle the loop
    # advanced_agent_example()          # More control - manual loop
    # conversational_agent_example()    # Multi-turn conversations

    Note: These examples use mock data. Replace the tool implementations
    with real API calls for production use.
    """)

    # Uncomment to run examples:
    # simple_agent_example()
    # advanced_agent_example()
    # conversational_agent_example()
