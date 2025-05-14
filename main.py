import openai
from assistant import assistant
from functions import getProductInfo, checkStock
from dotenv import load_dotenv
import os
import time
import json

load_dotenv('.env')
openai.api_key = os.getenv("OPENAI_API_KEY")

def run_chat():
    thread = openai.beta.threads.create()

    print("ShopBot Assistant Started. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        # Enviar mensaje del usuario
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )

        # Crear ejecución
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        # Esperar hasta que esté listo
        while run.status not in ["completed", "requires_action"]:
            time.sleep(1)
            run = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        # Manejo de funciones si se requieren
        if run.status == "requires_action":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []

            for call in tool_calls:
                fn_name = call.function.name
                args = json.loads(call.function.arguments)  # más robusto que eval

                if fn_name == "getProductInfo":
                    result = getProductInfo(**args)
                elif fn_name == "checkStock":
                    result = checkStock(**args)
                else:
                    result = {"error": "Unknown function"}

                tool_outputs.append({
                    "tool_call_id": call.id,
                    "output": json.dumps(result)
                })

            # Enviar respuesta de la función
            run = openai.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

            # Esperar a que termine
            while run.status != "completed":
                time.sleep(1)
                run = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        # Mostrar respuesta del asistente
        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        for msg in messages.data[::-1]:
            if msg.role == "assistant":
                print("ShopBot:", msg.content[0].text.value)
                break

if __name__ == "__main__":
    run_chat()
