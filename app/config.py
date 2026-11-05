import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    LLM_API_KEY = os.getenv("LLM_API_KEY")
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

    # 数据库配置
    DATABASE_URL = "mysql+pymysql://root:123456@127.0.0.1:8899/agent_db?charset=utf8mb4"

    # Qdrant 配置
    QDRANT_HOST = "localhost"
    QDRANT_PORT = 6333
    COLLECTION_NAME = "private_knowledge"


settings = Settings()