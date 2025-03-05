from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from sqlalchemy import create_engine, text
import re
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def remove_markdown(query: str) -> str:
    """Loại bỏ markdown code fences khỏi truy vấn SQL."""
    query = re.sub(r"```sql|```", "", query).strip()
    return query


def create_database_chain(llm, database_url):
    """Tạo và trả về SQLDatabaseChain."""
    engine = create_engine(database_url, echo=True)
    database = SQLDatabase(engine, metadata=Base.metadata)

    sql_prompt = PromptTemplate(
        input_variables=["query", "table_info"],
        template="""
        Bạn là một chuyên gia SQL và có thể trả lời các câu hỏi về database "products".
        Bạn có quyền truy cập thông tin sau về database:
        {table_info}

        Dựa trên thông tin database này, hãy tạo ra câu lệnh SQL để trả lời câu hỏi sau:
        {query}

        Dựa trên database "products" và thông tin cột ở trên, hãy tạo ra một câu lệnh SQL **SELECT * FROM products** nếu có thể,
        nếu không thì hãy tạo ra câu lệnh SQL để trả lời câu hỏi sau:
        {query}
        Chỉ trả về câu lệnh SQL, không có bất cứ giải thích hoặc markdown nào khác.
        """
    )

    sql_llm_chain = LLMChain(llm=llm, prompt=sql_prompt)
    sql_chain = SQLDatabaseChain(llm_chain=sql_llm_chain, database=database, verbose=True)
    return sql_chain, database

def format_db_result(db_result: list) -> str:
    """Định dạng lại kết quả in ra"""
    if not db_result:
        return "Không có kết quả."

    id_width = 5
    name_width = 15
    type_width = 12
    color_width = 50
    price_width = 8

    formatted_result = f"{'ID':<{id_width}} | {'Tên':<{name_width}} | {'Loại':<{type_width}} | {'Màu':<{color_width}} | {'Giá':<{price_width}}\n"
    formatted_result += "---" * 20 + "\n"

    for row in db_result:
        if len(row) >= 5:
            formatted_result += f"{row[0]:<{id_width}} | {row[1]:<{name_width}} | {row[2]:<{type_width}} | {str(row[3]):<{color_width}} | {row[4]:<{price_width}.2f}\n"
        else:
            formatted_result += f"Hàng không đủ thông tin: {row}\n"
    return formatted_result


def execute_query(database, query: str) -> str:
    """Thực thi truy vấn SQL và trả về kết quả đã định dạng."""
    cleaned_query = remove_markdown(query)
    engine = database._engine

    try:
        with engine.connect() as connection:
            result = connection.execute(text(cleaned_query))
            db_result = result.fetchall()

        formatted_result = format_db_result(db_result)
        return formatted_result
    except Exception as e:
        return f"Lỗi khi thực thi truy vấn SQL: {e}"