from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse  # 👈 新增这行
from app.database import engine, Base
from app.routers import chat
import os
# 自动在 MySQL 里建表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Agent 工业级双引擎助手")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# 挂载路由
app.include_router(chat.router, prefix="/api", tags=["Chat"])

# 👇 新增下面这个路由，把前端页面返回给浏览器
@app.get("/")
async def serve_frontend():
    # 确保 index.html 在项目根目录
    return FileResponse(os.path.join(os.path.dirname(__file__), "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)