# llm-audit — Model-visible = Logged 运行时不变量

> 任何发送给模型的请求，其完整输入必须在调用前落盘。模型能看到的，审计必须能重建。

`llm-audit` 是一个零依赖（纯标准库）的 Python 组件，实现 **model-visible = logged** 审计不变量：每次 LLM 调用的完整 prompt 在发送前写入本地审计日志，从而做到：

- **可重建**：审计日志可 100% 重建模型当时所见的输入（prompt 全量 + 元数据）
- **可追溯**：每个回答都能追溯到其输入来源与上下文
- **可证明**：向监管/客户/审计方证明"系统对模型的每次暴露都有记录"

## 为什么需要它

企业 LLM 应用的最大信任缺口不是"模型答错"，而是**无法证明模型看到了什么**。人工检查、采样日志、事后从服务器日志拼接 —— 这些都无法保证完整性和时序性（调用前 vs 调用后）。

`model-visible = logged` 把审计从"事后取证"变成"调用前强制"：不落盘，不调用。这不是采样，是 100% 全量。

## 安装与使用

```bash
# 直接拷贝 llm_audit.py 到你的项目即可 (零依赖, 零安装)
```

接入（对调用方透明 —— 一行替换）：

```python
import httpx
from llm_audit import audited_post

# 原来: resp = httpx.post(url, headers=headers, json=body, timeout=45)
resp = audited_post(url, headers=headers, json=body, timeout=45, source="subagent.review")
```

审计日志追加到 `LLM_AUDIT_PATH`（默认 `./llm_audit.jsonl`），每条记录包含：

```json
{
  "ts": 1787568711.123,
  "source": "subagent.review",
  "prompt_hash": "sha256:...",
  "prompt": "...完整请求体...",
  "url": "https://api.example.com/v1/chat",
  "method": "POST"
}
```

### 压缩审计 (Compaction)

上下文压缩是 LLM 应用中最危险的"看不见的操作"—— 历史被折叠，模型看到的上下文被改写。`compact_and_audit` 把压缩变成强制审计事件：

```python
from llm_audit import compact_and_audit
rec = compact_and_audit(messages, history, trigger="token_limit", source="main.agent")
# rec.compacted / rec.dropped / rec.compaction_id
```

压缩发生时自动记录：丢弃了哪些消息、压缩后模型将看到什么、以及 **PostCompact 规则重灌**（压缩后机械注入硬约束，防止软提示词压缩失效）。

### 熔断 (LoopGuard)

检测同源重复 prompt（循环死锁）并抛 `LoopGuardError`：

```python
from llm_audit import audited_post, LoopGuardError
try:
    resp = audited_post(...)
except LoopGuardError:
    # 熔断: 同源同 prompt 连续重复, 停止
    break
```

## 审计验证

```python
# 可重建率检查: 读取审计日志, 验证每条记录完整性
from llm_audit import audit_reconstruct  # 或你的 CI 脚本
```

CI 门禁模式：可重建率非 100% 即失败 —— 审计不变量是系统属性，不是最佳实践。

## 设计原则

1. **调用前落盘**：不是采样、不是事后拼接 —— 发送前写盘，时序不可逆
2. **审计失败不阻塞业务**：写盘失败仅告警，绝不打断模型调用（审计是元操作，不能成为单点故障）
3. **纯标准库**：无框架绑定，任何 Python LLM 应用可接入
4. **线程安全**：多线程调用下追加写入有锁保护

## License

MIT

---

*构建于企业 AI 合规证据链实践。配套能力: 双库隔离问答、引用溯源、法规情报持续更新。*
