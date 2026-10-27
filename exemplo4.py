from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.chroma import ChromaDb
from agno.os import AgentOS

import os
from dotenv import load_dotenv

load_dotenv()


#RAG
vector_db = ChromaDb(collection="pdf_agent", path="tmp/chromadb", persistent_client=True)
knowledge = Knowledge(vector_db=vector_db)

"""knowledge.add_content(
    path="GlobalEVOutlook2025.pdf",
    content=None,
    content_type=None,
    metadata=None,
    metadata_field="content",
    skip_existing=True,
    debug_mode=True 
)
    

"""
db = SqliteDb(session_table="agent_session", db_file="tmp/agent.db")

agent = Agent(
    id="agente_pdf",
    name="Agente de PDF",
    model=OpenAIChat(id="gpt-5-nano", api_key=os.getenv("OPENAI_API_KEY")),
    db=db,
    knowledge=knowledge,
    enable_agentic_memory=True, #memoria do agente
    instructions="Você deve chamar o usuário de senhor e busque informações no PDF",
    description="",
    add_history_to_context=True,
    search_knowledge=True, 
    num_history_runs=3,
    debug_mode=True 
)

#AGENTOS ====================================
agent_os = AgentOS(
    name="Agente de PDF",
    agents=[agent]
    ) 

app = agent_os.get_app()

#RUN =========================================

if __name__ == "__main__":

    knowledge.insert(
        url="https://static.poder360.com.br/uploads/2026/08/Programa-Governo-LULA-2026.pdf",
        metadata={"title": "Proposta de Governo Lula 2026"},
        skip_if_exists=True,
        reader=PDFReader()
    )
    agent_os.serve(app="exemplo4:app", host="0.0.0.0", port=7777, reload=True)
