import openai
import os
from dotenv import load_dotenv

load_dotenv('.env')
openai.api_key = os.getenv("OPENAI_API_KEY")

assistant_name = "ShopBot"

existing_assistants = openai.beta.assistants.list().data
assistant = next((a for a in existing_assistants if a.name == assistant_name), None)

if assistant:
    print(f"✅ Using existing assistant: {assistant.id}")
else:
    print("🆕 Creating new assistant...")
    assistant = openai.beta.assistants.create(
        name=assistant_name,
        instructions="""
        You are ShopBot, an AI assistant that helps users with product queries in an e-commerce store.
        You MUST always use the available functions to retrieve product information or check stock availability whenever the user asks about a product.
        Do not respond from your own knowledge. Always call a function when product-related questions are asked.
        """,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "getProductInfo",
                    "description": "Returns product details when the user mentions a product name.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "productName": {
                                "type": "string",
                                "description": "The exact or partial name of the product."
                            }
                        },
                        "required": ["productName"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "checkStock",
                    "description": "Checks whether a product is currently in stock.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "productName": {
                                "type": "string",
                                "description": "The product to check availability for."
                            }
                        },
                        "required": ["productName"]
                    }
                }
            }
        ],
        model="gpt-4o"
    )
    print(f"✅ Assistant created: {assistant.id}")

# Save the assistant ID to a file so main.py can reuse it
with open("assistant_id.txt", "w") as f:
    f.write(assistant.id)
