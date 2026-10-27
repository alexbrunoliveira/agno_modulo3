# 1 - IMPORTS ==================================================
from prompt_toolkit import prompt
import requests
import json
from pprint import pprint

AGENT_ID = "agente_pdf"
ENDPOINT = f"http://localhost:7777/agents/{AGENT_ID}/runs" # Adicionar /runs para iniciar o chat



# 2 - Conexao com o Agno =======================================

def get_response_stream(message:str):
    response = requests.post(
        url=ENDPOINT,
        data={
            "message":message,
            "stream": "true"
        },
        stream=True
    )

    return response
# 3 - Streaming (Processamento) ================================

# 4 - Run (loop) ================================================

if __name__ == "__main__":
    message = prompt("Digite sua mensagem: ")
    response = get_response_stream(message)  
    print(response)