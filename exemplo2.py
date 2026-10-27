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
)


"""
db = SqliteDb(session_table="agent_session", db_file="tmp/agent.db")

agent = Agent(
    id="agente_pdf",
    name="Agente de PDF",
    model=OpenAIChat(id="gpt-5-nano", api_key=os.getenv("OPENAI_API_KEY")),
    db=db,
    knowledge=knowledge,
    instructions="Você deve chamar o usuário de senhor",
    description="",
    add_history_to_context=True,
    search_knowledge=True, 
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
    agent_os.serve(app=app) 