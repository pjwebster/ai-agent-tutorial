"""
Simple Working Agent Example
=============================

A minimal, ready-to-run example of an AI agent using Claude.
This agent can perform calculations and get the current time.

Setup:
1. pip install anthropic
2. export ANTHROPIC_API_KEY="your-api-key"
3. python simple_agent_example.py
"""

import anthropic
from anthropic import beta_tool
from datetime import datetime
import math


# Define tools using the @beta_tool decorator
@beta_tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression.

    Args:
        expression: A mathematical expression like "2 + 2" or "sqrt(16)".
    """
    try:
        # Safe math evaluation (limited to math functions)
        result = eval(
            expression,
            {"__builtins__": {}},
            {
                "sqrt": math.sqrt,
                "pow": math.pow,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "pi": math.pi,
                "e": math.e,
            }
        )
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"


@beta_tool
def get_current_time(timezone: str = "UTC") -> str:
    """Get the current time.

    Args:
        timezone: The timezone (currently only supports UTC).
    """
    now = datetime.now()
    return f"Current time ({timezone}): {now.strftime('%Y-%m-%d %H:%M:%S')}"


def run_agent(user_query: str):
    """Run the agent with a user query."""
    print(f"\n{'='*70}")
    print(f"USER QUERY: {user_query}")
    print(f"{'='*70}\n")

    client = anthropic.Anthropic()

    # Create a tool runner - it handles the agent loop automatically
    runner = client.beta.messages.tool_runner(
        model="claude-opus-4-7",
        max_tokens=16000,
        thinking={"type": "adaptive"},
        output_config={"effort": "high"},
        tools=[calculate, get_current_time],
        messages=[{"role": "user", "content": user_query}],
    )

    # Iterate through agent responses
    iteration = 0
    for message in runner:
        iteration += 1
        print(f"--- Agent Iteration {iteration} ---\n")

        for block in message.content:
            if block.type == "thinking":
                # Show first 150 chars of thinking
                thinking = block.thinking[:150]
                if len(block.thinking) > 150:
                    thinking += "..."
                print(f"💭 [Thinking]: {thinking}\n")

            elif block.type == "text":
                print(f"💬 [Response]: {block.text}\n")

            elif block.type == "tool_use":
                print(f"🔧 [Tool Call]: {block.name}")
                print(f"   Input: {block.input}\n")

    print(f"{'='*70}")
    print(f"✓ Agent completed the task in {iteration} iteration(s)")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                   Simple AI Agent Example                        ║
    ╚══════════════════════════════════════════════════════════════════╝

    This agent can:
    - Perform mathematical calculations
    - Get the current time
    - Think through problems step-by-step
    """)

    # Example 1: Simple calculation
    run_agent("What is the square root of 144?")

    # Example 2: Complex calculation
    run_agent("Calculate the area of a circle with radius 5. Use pi = 3.14159")

    # Example 3: Time-based query
    run_agent("What time is it right now?")

    # Example 4: Multi-step reasoning
    run_agent("What time is it? Then calculate how many seconds are in a day.")

    print("\n" + "="*70)
    print("KEY TAKEAWAYS")
    print("="*70)
    print("""
    1. Tools are defined as Python functions with @beta_tool decorator
    2. The tool runner automatically handles the agent loop
    3. Claude decides which tools to call and when
    4. Adaptive thinking helps Claude reason through complex tasks
    5. The agent continues until the task is complete

    Try modifying this example:
    - Add your own tools (e.g., web search, file operations)
    - Change the user queries
    - Adjust the effort level (low, medium, high, max)
    - Add error handling and logging
    """)
