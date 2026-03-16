import requests
import json
from langchain.tools import Tool

OPENAPI_URL = "http://127.0.0.1:8000/openapi.json"


def load_openapi():
    response = requests.get(OPENAPI_URL)
    return response.json()


def create_tools_from_openapi():
    spec = load_openapi()

    tools = []

    paths = spec["paths"]

    for path, methods in paths.items():
        for method, details in methods.items():

            name = details.get("summary", f"{method}_{path}")
            description = f"Call API {method.upper()} {path}"

            def make_api_call(path=path, method=method):
                def call_api(input=""):
                    url = f"http://127.0.0.1:8000{path}"

                    if method == "get":
                        r = requests.get(url)
                    else:
                        r = requests.post(url, json={"message": input})

                    return r.text

                return call_api

            tools.append(
                Tool(
                    name=name,
                    func=make_api_call(),
                    description=description
                )
            )

    return tools
