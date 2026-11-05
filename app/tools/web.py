from tavily import TavilyClient
from app.config import settings

tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)

def search_web(query: str, max_results: int = 3) -> str:
    try:
        response = tavily_client.search(query=query, search_depth="basic", max_results=max_results)
        results = response.get("results", [])
        if not results: return "全网未找到相关结果。"
        return "\n\n".join([f"标题: {res.get('title')}\n内容: {res.get('content')}" for res in results])
    except Exception as e:
        print(f"[Web Tool Error]: {e}")
        return "搜索服务暂时不可用。"