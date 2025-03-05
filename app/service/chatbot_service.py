from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from pydantic import BaseModel
from typing import List
from fastapi import HTTPException
from app.core.config import settings
from app.service.chatbot_data import create_database_chain, execute_query

class ChatbotInput(BaseModel):
    query: str

# Gemini
llm = ChatGoogleGenerativeAI(model=settings.MODEL, google_api_key=settings.API_KEY)

# OpenAI
# llm = ChatOpenAI(model_name=settings.MODEL, openai_api_key=settings.API_KEY)

chat_history = SQLChatMessageHistory(session_id="default", connection_string=settings.DATABASE_URL)
memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=chat_history, return_messages=True, llm=llm)

prompt = PromptTemplate(
    input_variables=["query", "chat_history"],
    template="""
    Bạn là một trợ lý AI thông minh.
    Lịch sử hội thoại trước đó: {chat_history}
    Người dùng hỏi: {query}
    Trả lời một cách chính xác và súc tích.
    """
)

sql_chain, database = create_database_chain(llm, settings.DATABASE_URL)

def get_response(query: str) -> str:
    try:
        table_info = database.get_table_info()
        sql_query = sql_chain.llm_chain.run({"query": query, "table_info": table_info}) 
        db_result = execute_query(database, sql_query)

        chat_history_data = memory.load_memory_variables({})
        chat_history = chat_history_data.get("chat_history", "")

        llm_chain = LLMChain(llm=llm, prompt=prompt, memory=memory)
        response = llm_chain.run({"query": query, "chat_history": chat_history})
        memory.save_context({"query": query}, {"response": response})

        
        if db_result and response:
            return f"Kết quả tìm kiếm:\n{db_result}\n\nBot: {response}"
        elif response:
            return response
        else:
            return "Không tìm thấy thông tin phù hợp."

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def get_chat_history() -> List[str]:
    return memory.load_memory_variables({}).get("chat_history", [])