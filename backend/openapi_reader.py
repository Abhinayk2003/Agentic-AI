import json
import requests
from langchain_core.tools import Tool


def create_tools_from_openapi():
    tools = []

    try:
        with open("openapi.json") as f:
            spec = json.load(f)

        for path, methods in spec.get("paths", {}).items():
            for method, details in methods.items():

                def api_call(input_text, path=path, method=method):
                    url = f"http://localhost:8001{path}"

                    if method.upper() == "GET":
                        response = requests.get(url)
                    else:
                        response = requests.post(url, json={"input": input_text})

                    return response.text

                tools.append(
                    Tool(
                        name=f"{method.upper()}_{path.replace('/','_')}",
                        func=api_call,
                        description=details.get("summary", "API call")
                    )
                )

    except Exception as e:
        print("Error loading OpenAPI tools:", e)

    return tools