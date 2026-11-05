from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import json

from app.schemas import ChatRequest
from app.database import get_db
from app.services import memory, agent
from app.config import settings
from openai import OpenAI

router = APIRouter()
llm_client = OpenAI(api_key=settings.LLM_API_KEY, base_url=settings.LLM_BASE_URL)


@router.post("/chat")
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    # 1. 记忆处理
    history_text = memory.get_recent_history(db, request.user_id)
    memory.save_message(db, request.user_id, "user", request.question)

    # 2. Agent 决策与 Prompt 组装
    route = agent.decide_route(request.question)
    print(f"[Agent 路由]: {route}")
    prompt = agent.get_context_and_prompt(route, request.question, history_text)

    # 3. 流式生成器
    def event_stream():
        full_answer = []
        yield f"data: {json.dumps({'type': 'meta', 'route': route}, ensure_ascii=False)}\n\n"
        try:
            response = llm_client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                stream=True
            )
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    text = chunk.choices[0].delta.content
                    full_answer.append(text)
                    yield f"data: {json.dumps({'text': text}, ensure_ascii=False)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'text': str(e)}, ensure_ascii=False)}\n\n"
        finally:
            answer = "".join(full_answer)
            if answer:
                # 这里单独开一个 Session 存，防止流式响应时 Session 已关闭
                from app.database import SessionLocal
                db_session = SessionLocal()
                memory.save_message(db_session, request.user_id, "assistant", answer)
                db_session.close()

    return StreamingResponse(event_stream(), media_type="text/event-stream")