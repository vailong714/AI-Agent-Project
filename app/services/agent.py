from openai import OpenAI
from app.config import settings
from app.tools.rag import search_rag
from app.tools.web import search_web
import json

llm_client = OpenAI(api_key=settings.LLM_API_KEY, base_url=settings.LLM_BASE_URL)


def decide_route(question: str) -> str:
    prompt = f"""
    判断用户问题该使用哪个工具：
    - "rag"：涉及私有项目、文档。
    - "web"：涉及实时新闻、公开信息。
    - "none"：闲聊、纯推理。
    严格输出 JSON: {{"tool": "rag"}} 或 {{"tool": "web"}} 或 {{"tool": "none"}}
    用户问题：{question}
    """
    try:
        res = llm_client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        return json.loads(res.choices[0].message.content).get("tool", "none")
    except Exception:
        return "none"


def get_context_and_prompt(route: str, question: str, history_text: str) -> str:
    context_data = ""
    if route == "rag":
        chunks = search_rag(question)
        context_data = "【私有知识库结果】\n" + ("\n---\n".join(chunks) if chunks else "未检索到资料。")
    elif route == "web":
        context_data = "【全网搜索结果】\n" + search_web(question)

    return f"""
    请根据以下信息回答问题，不要编造。
    {context_data}
    【历史记录】
    {history_text}
    用户问题：{question}
    """