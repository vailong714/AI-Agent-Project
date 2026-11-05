# seed_rag.py
import sys
import os

# 将项目根目录加入环境变量，确保能导入 app 模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 🔥 注意这里：导入路径变了！从 app.tools.rag 导入
from app.tools.rag import add_documents

if __name__ == "__main__":
    print("开始向 Qdrant 灌入初始数据...")
    add_documents(
        [  # 直接放列表
            "AI-Agent-Project 的长期记忆模块使用 SQLAlchemy + MySQL，通过 user_id 关联对话历史。",
            "项目的流式接口基于 FastAPI 的 StreamingResponse 和 SSE 实现，DeepSeek 返回的每个 chunk 直接推给前端。",
            "Tavily 搜索接入计划在 Qdrant 检索之后完成，用于处理私有知识库覆盖不到的外部信息。",
        ],
        [  # 直接放列表
            {"source": "project_readme", "module": "memory"},
            {"source": "project_readme", "module": "streaming"},
            {"source": "project_plan", "module": "tavily"},
        ],
    )
    print("✅ 数据灌入完成！")