from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

from tool_generator import generate_tools
from openapi_reader import create_tools_from_openapi


# Load tools
email_tools = generate_tools()
api_tools = create_tools_from_openapi()

tools = email_tools + api_tools


# Convert tools into dictionary
tool_map = {tool.name: tool for tool in tools}


# Load Ollama model
llm = OllamaLLM(model="llama3")


prompt = ChatPromptTemplate.from_template("""
You are an AI assistant that can use tools.

Available tools:
{tools}

If the user asks for something related to a tool,
respond ONLY with the tool name.

User question:
{input}
""")


def run_agent(query: str):

    tool_descriptions = "\n".join(
        [f"{t.name}: {t.description}" for t in tools]
    )

    chain = prompt | llm

    response = chain.invoke({
        "input": query,
        "tools": tool_descriptions
    })

    response_text = str(response).strip()

    # Check if response matches tool name
    if response_text in tool_map:
        tool = tool_map[response_text]
        result = tool.func(query)
        return result

    return response_text