"""最小接入示例 — audited_post 一行替换 httpx.post."""
import httpx

from llm_audit import audited_post


def chat(api_key: str, prompt: str) -> str:
    url = "https://api.example.com/v1/chat/completions"
    body = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 256,
    }
    resp = audited_post(
        url,
        headers={"Authorization": f"Bearer {api_key}"},
        json=body,
        timeout=45,
        source="demo.chat",          # 审计事件来源标识
    )
    return resp.json()["choices"][0]["message"]["content"]


if __name__ == "__main__":
    # 无真实 API key 时仅演示审计写入
    import json
    try:
        chat("sk-test", "你好")
    except httpx.HTTPError:
        pass
    with open("llm_audit.jsonl", encoding="utf-8") as f:
        lines = [json.loads(l) for l in f if l.strip()]
    print(f"审计记录: {len(lines)} 条, 示例: {lines[-1]['source']} / prompt_hash={lines[-1]['prompt_hash'][:20]}...")
