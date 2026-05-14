"""
Simple Working Agent Example - Google Gemini
=============================================

A minimal, ready-to-run example of an AI agent using Gemini.
This agent can perform calculations and get the current time.

Setup:
1. pip install google-generativeai
2. export GOOGLE_API_KEY="your-api-key"
3. python simple_agent_example.py
"""

import google.generativeai as genai
from datetime import datetime
import math
import json


# Configure the Gemini API
genai.configure(api_key=None)  # Uses GOOGLE_API_KEY env var


# Define tools using function declarations
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression.

    Args:
        expression: A mathematical expression like "2 + 2" or "sqrt(16)".

    Returns:
        str: The result of the calculation or an error message.
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


def get_current_time(timezone: str = "UTC") -> str:
    """Get the current time.

    Args:
        timezone: The timezone (currently only supports UTC).

    Returns:
        str: The current time in the specified timezone.
    """
    now = datetime.now()
    return f"Current time ({timezone}): {now.strftime('%Y-%m-%d %H:%M:%S')}"


# Create function declarations for Gemini
calculate_declaration = genai.protos.Tool(
    function_declarations=[
        genai.protos.FunctionDeclaration(
            name="calculate",
            description="Evaluate a mathematical expression like '2 + 2' or 'sqrt(16)'",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "expression": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="A mathematical expression to evaluate"
                    ),
                },
                required=["expression"]
            )
        ),
        genai.protos.FunctionDeclaration(
            name="get_current_time",
            description="Get the current time",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "timezone": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="The timezone (currently only supports UTC)"
                    ),
                },
            )
        ),
    ]
)


# Map function names to actual functions
available_functions = {
    "calculate": calculate,
    "get_current_time": get_current_time,
}


def run_agent(user_query: str):
    """Run the agent with a user query."""
    print(f"\n{'='*70}")
    print(f"USER QUERY: {user_query}")
    print(f"{'='*70}\n")

    # Initialize the model with function calling
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        tools=[calculate_declaration]
    )

    # Start a chat session
    chat = model.start_chat(enable_automatic_function_calling=False)

    # Send the initial message
    response = chat.send_message(user_query)

    iteration = 0
    max_iterations = 10

    # Agent loop - continue until no more function calls
    while iteration < max_iterations:
        iteration += 1
        print(f"--- Agent Iteration {iteration} ---\n")

        # Check if the model wants to call functions
        if response.candidates[0].content.parts[0].function_call:
            # Model is calling a function
            function_calls = []

            for part in response.candidates[0].content.parts:
                if fn := part.function_call:
                    print(f"🔧 [Tool Call]: {fn.name}")
                    print(f"   Input: {dict(fn.args)}\n")

                    # Execute the function
                    function_name = fn.name
                    function_args = dict(fn.args)

                    if function_name in available_functions:
                        function_result = available_functions[function_name](**function_args)
                        print(f"📊 [Tool Result]: {function_result}\n")

                        # Prepare function response
                        function_calls.append(
                            genai.protos.Part(
                                function_response=genai.protos.FunctionResponse(
                                    name=function_name,
                                    response={"result": function_result}
                                )
                            )
                        )

            # Send function results back to the model
            response = chat.send_message(function_calls)

        else:
            # Model has finished - print final response
            print(f"💬 [Response]: {response.text}\n")
            break

    print(f"{'='*70}")
    print(f"✓ Agent completed the task in {iteration} iteration(s)")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                Simple AI Agent Example - Gemini                  ║
    ╚══════════════════════════════════════════════════════════════════╝

    This agent can:
    - Perform mathematical calculations
    - Get the current time
    - Reason through problems step-by-step
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
    1. Tools are defined as function declarations with schemas
    2. The agent loop handles function calling manually
    3. Gemini decides which functions to call and when
    4. The agent continues until the task is complete

    Try modifying this example:
    - Add your own tools (e.g., web search, file operations)
    - Change the user queries
    - Switch to gemini-1.5-flash for faster/cheaper responses
    - Try enable_automatic_function_calling=True
    """)
