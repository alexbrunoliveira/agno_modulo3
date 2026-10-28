# 1 - IMPORTS ==================================================
from prompt_toolkit import prompt
import requests
import json
import streamlit as st
#import sys
from streamlit.runtime.scriptrunner import get_script_run_ctx

AGENT_ID = "agente_pdf"
ENDPOINT = f"https://modulo3-api-ojva.onrender.com/{AGENT_ID}/runs"
#ENDPOINT = f"http://localhost:7777/agents/{AGENT_ID}/runs"


# 2 - Conexao com o Agno e Streaming ===========================

def stream_response(message: str):
    """
    Função geradora que conecta ao endpoint com streaming
    e entrega os fragmentos (yield) linha a linha.
    """
    try:
        response = requests.post(
            url=ENDPOINT,
            data={
                "message": message,
                "stream": "true"
            },
            stream=True
        )
    except requests.exceptions.ConnectionError:
        error_msg = "Erro: Servidor não encontrado na porta 7777! Inicie primeiro o backend (ex: uv run exemplo4.py)."
        yield error_msg
        return

    # 2.1 - Processamento do Streaming
    for line in response.iter_lines():
        if line:
            try:
                decoded_line = line.decode('utf-8')

                # Suporte para formato SSE (Server-Sent Events)
                if decoded_line.startswith("data: "):
                    decoded_line = decoded_line[6:]

                data = json.loads(decoded_line)

                # Extrai o conteúdo emitido pelo agente
                content = data.get("content") or data.get("delta") or data.get("response") or ""
                if content:
                    yield content
            except json.JSONDecodeError:
                continue


# 3 - Execução no Streamlit ou no Terminal =====================

# Detecta com segurança se o script está rodando dentro do Streamlit
is_running_in_streamlit = get_script_run_ctx() is not None

if is_running_in_streamlit:
    st.title("Chat com Agente PDF")

    prompt_user = st.chat_input("Digite sua mensagem:")

    if prompt_user:
        with st.chat_message("user"):
            st.write(prompt_user)

        with st.chat_message("assistant"):
            st.write_stream(stream_response(prompt_user))

else:
    # Modo Terminal (quando executado com: python exemplo3.py)
    if __name__ == "__main__":
        print("--- Modo Terminal ---")
        message = prompt("Digite sua mensagem: ")
        print("Resposta: ", end="", flush=True)
        for chunk in stream_response(message):
            print(chunk, end="", flush=True)
        print()