"""
AI Agent Tutorial: Building from Scratch with Google Gemini
===========================================================

This tutorial teaches you to build an AI agent step by step using Gemini API.
We'll create a research assistant that can search the web and analyze data.

Prerequisites:
- pip install google-generativeai
- Set GOOGLE_API_KEY environment variable
"""

import google.generativeai as genai
import json
from typing import List, Dict
from datetime import datetime

# Configure Gemini API (uses GOOGLE_API_KEY env var)
genai.configure(api_key=None)

# ==============================================================================
# STEP 1: Understanding the Basics
# ==============================================================================
# An AI agent is different from a simple chatbot:
# - Chatbot: User asks → Gemini answers → Done
# - Agent: User asks → Gemini decides what tools to use → Executes tools →
#          Gemini analyzes results → Repeats until task is complete

# ==============================================================================
# STEP 2: Define Your Tools
# ==============================================================================
# Tools are functions that Gemini can call to interact with the world.
# Unlike Anthropic's @beta_tool decorator, we manually create function declarations.

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


def analyze_data(data: str, analysis_type: str = "summary") -> str:
    """Analyze provided data.

    Args:
        data: The data to analyze (as JSON string or text).
        analysis_type: Type of analysis - "summary", "statistics", or "trends".
    """
    # In a real implementation, this would perform actual analysis
    # For this tutorial, we'll simulate analysis
    return f"Analysis ({analysis_type}): The data shows interesting patterns..."


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


# Create function declarations for Gemini
research_tools = genai.protos.Tool(
    function_declarations=[
        genai.protos.FunctionDeclaration(
            name="web_search",
            description="Search the web for information on a given query",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "query": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="The search query string"
                    ),
                    "max_results": genai.protos.Schema(
                        type=genai.protos.Type.INTEGER,
                        description="Maximum number of results to return (1-10)"
                    ),
                },
                required=["query"]
            )
        ),
        genai.protos.FunctionDeclaration(
            name="analyze_data",
            description="Analyze provided data with specified analysis type",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "data": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="The data to analyze (JSON string or text)"
                    ),
                    "analysis_type": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="Type of analysis: summary, statistics, or trends"
                    ),
                },
                required=["data"]
            )
        ),
        genai.protos.FunctionDeclaration(
            name="save_findings",
            description="Save research findings to a file",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "title": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="Title of the findings"
                    ),
                    "content": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="The content to save"
                    ),
                    "tags": genai.protos.Schema(
                        type=genai.protos.Type.ARRAY,
                        items=genai.protos.Schema(type=genai.protos.Type.STRING),
                        description="List of tags for categorization"
                    ),
                },
                required=["title", "content", "tags"]
            )
        ),
    ]
)

# Map function names to implementations
available_functions = {
    "web_search": web_search,
    "analyze_data": analyze_data,
    "save_findings": save_findings,
}


# ==============================================================================
# STEP 3: Create the Agent (Manual Loop)
# ==============================================================================
# Gemini requires manual loop implementation for function calling.

def simple_agent_example():
    """Example of a basic agent with manual function calling loop."""
    print("\n" + "="*70)
    print("SIMPLE AGENT EXAMPLE")
    print("="*70)

    # Initialize the model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        tools=[research_tools]
    )

    # Start chat session
    chat = model.start_chat(enable_automatic_function_calling=False)

    # Send initial message
    user_message = "Research the latest developments in quantum computing and save your findings."
    print(f"\n[USER]: {user_message}\n")

    response = chat.send_message(user_message)

    iteration = 0
    max_iterations = 10

    # Agent loop
    while iteration < max_iterations:
        iteration += 1
        print(f"--- Agent Iteration {iteration} ---\n")

        # Check if model wants to call functions
        function_call_exists = any(
            part.function_call for part in response.candidates[0].content.parts
        )

        if function_call_exists:
            # Execute function calls
            function_responses = []

            for part in response.candidates[0].content.parts:
                if fn := part.function_call:
                    print(f"🔧 [Tool Call]: {fn.name}")
                    function_args = dict(fn.args)
                    print(f"   Input: {function_args}\n")

                    # Execute the function
                    if fn.name in available_functions:
                        result = available_functions[fn.name](**function_args)
                        print(f"📊 [Tool Result]: {result[:100]}...\n")

                        function_responses.append(
                            genai.protos.Part(
                                function_response=genai.protos.FunctionResponse(
                                    name=fn.name,
                                    response={"result": result}
                                )
                            )
                        )

            # Send results back to model
            response = chat.send_message(function_responses)

        else:
            # Model is done - print final response
            print(f"💬 [RESPONSE]: {response.text}\n")
            break

    print(f"✓ Agent completed its task in {iteration} iteration(s)!\n")


# ==============================================================================
# STEP 4: Automatic Function Calling
# ==============================================================================
# Gemini can automatically execute functions, but you lose visibility.

def automatic_agent_example():
    """Example using automatic function calling."""
    print("\n" + "="*70)
    print("AUTOMATIC AGENT EXAMPLE")
    print("="*70)

    # Define simpler tools for automatic calling
    def get_weather(location: str) -> str:
        """Get weather for a location."""
        return f"Weather in {location}: 72°F, sunny"

    weather_tool = genai.protos.Tool(
        function_declarations=[
            genai.protos.FunctionDeclaration(
                name="get_weather",
                description="Get current weather for a location",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "location": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="City and state, e.g., San Francisco, CA"
                        ),
                    },
                    required=["location"]
                )
            ),
        ]
    )

    # Register functions for automatic calling
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        tools=[weather_tool]
    )

    # Enable automatic function calling
    chat = model.start_chat(enable_automatic_function_calling=True)

    # Note: For automatic calling to work, you need to provide actual callable functions
    # This is a simplified example - see Gemini docs for full implementation
    print("\n[USER]: What's the weather in San Francisco?\n")
    print("Note: Automatic function calling requires additional setup.")
    print("See simple_agent_example() for manual control.\n")


# ==============================================================================
# STEP 5: Multi-Turn Conversation Agent
# ==============================================================================

class ConversationalAgent:
    """An agent that maintains conversation state across multiple interactions."""

    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            tools=[research_tools]
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=False)

    def chat_turn(self, user_message: str) -> str:
        """Send a message to the agent and get a response."""
        print(f"\n[USER]: {user_message}")

        response = self.chat.send_message(user_message)

        # Handle function calling loop
        max_iterations = 10
        for iteration in range(max_iterations):
            function_call_exists = any(
                part.function_call for part in response.candidates[0].content.parts
            )

            if function_call_exists:
                function_responses = []
                for part in response.candidates[0].content.parts:
                    if fn := part.function_call:
                        print(f"  [Calling: {fn.name}]")
                        function_args = dict(fn.args)

                        if fn.name in available_functions:
                            result = available_functions[fn.name](**function_args)
                            function_responses.append(
                                genai.protos.Part(
                                    function_response=genai.protos.FunctionResponse(
                                        name=fn.name,
                                        response={"result": result}
                                    )
                                )
                            )

                response = self.chat.send_message(function_responses)
            else:
                break

        final_response = response.text
        print(f"[AGENT]: {final_response}")
        return final_response


def conversational_agent_example():
    """Example of a multi-turn conversational agent."""
    print("\n" + "="*70)
    print("CONVERSATIONAL AGENT EXAMPLE")
    print("="*70)

    agent = ConversationalAgent()

    # Have a multi-turn conversation
    agent.chat_turn("Search for information about AI agents.")
    agent.chat_turn("Now analyze what you found and identify the key concepts.")
    agent.chat_turn("Save your analysis with tags 'AI', 'agents', 'tutorial'.")


# ==============================================================================
# STEP 6: Best Practices & Tips
# ==============================================================================

def best_practices():
    """Print best practices for building agents."""
    print("\n" + "="*70)
    print("BEST PRACTICES FOR BUILDING AI AGENTS WITH GEMINI")
    print("="*70)

    practices = """
    1. START SIMPLE
       - Manual function calling gives you more control
       - Automatic calling is convenient but less transparent

    2. FUNCTION DECLARATION DESIGN
       - Use clear, descriptive names
       - Provide detailed parameter descriptions
       - Specify required vs optional parameters
       - Return JSON for structured data

    3. ERROR HANDLING
       - Validate function inputs
       - Return clear error messages
       - Set max_iterations to prevent infinite loops
       - Check for function_call in response parts

    4. MODEL SELECTION
       - gemini-1.5-pro: Best for complex reasoning (2M context)
       - gemini-1.5-flash: Faster, cheaper, good for simple tasks
       - gemini-pro: Stable, production-ready

    5. COST OPTIMIZATION
       - Use Flash for high-volume tasks
       - Pro for balanced cost/quality
       - Monitor token usage via API response

    6. TESTING
       - Test each function independently first
       - Start with simple queries before complex ones
       - Log all function calls for debugging
       - Use manual mode during development

    7. WHEN TO USE AGENTS
       ✓ Multi-step tasks that need dynamic planning
       ✓ Tasks requiring multiple function calls
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
    ║      AI AGENT TUTORIAL - Building Agents with Gemini            ║
    ╚══════════════════════════════════════════════════════════════════╝

    This tutorial demonstrates building AI agents with Google Gemini:

    1. Simple Agent - Manual function calling loop
    2. Automatic Agent - Gemini handles function execution
    3. Conversational Agent - Multi-turn interactions

    Make sure you have:
    - Installed: pip install google-generativeai
    - Set environment variable: GOOGLE_API_KEY
    """)

    # Print best practices
    best_practices()

    print("\n" + "="*70)
    print("READY TO RUN EXAMPLES")
    print("="*70)
    print("""
    Uncomment the examples below to run them:

    # simple_agent_example()           # Manual loop - full control
    # automatic_agent_example()         # Auto execution (limited demo)
    # conversational_agent_example()    # Multi-turn conversations

    Note: These examples use mock data. Replace the function implementations
    with real API calls for production use.
    """)

    # Uncomment to run examples:
    # simple_agent_example()
    # conversational_agent_example()
