# ADOPTION-EVIDENCE — no-mistakes (2026-08-31)

> 吞噬证据链 (用户 2026-08-11 要求全仓建立)。本文件记录本仓库对 no-mistakes 吞噬轮次的借鉴证据。

## 统一头部

- 来源: [kunchenguid/no-mistakes](https://github.com/kunchenguid/no-mistakes) (MIT, 8,067⭐, 活跃)
- 方法: harness-devour skill, 吞噬报告 `harness-devour/docs/no-mistakes-devour-report.md` (评分卡 96.0/100)
- 模式库: `harness-devour/patterns/` — push_gate / findings_disposition (migrated), intent_conformance (experiment), evidence_branch (watch)
- 核心模式: **push 前置门禁** (流水线全绿才转发远端 + 自动干净 PR) / **findings 分流** (机械修复自动, 意图判断留人) / **fail closed** (无法验证 = 拒绝 + 大声失败) / **证据附着** (run 证据文件 + PR 引用)
- 落地: YYW0228/pregate (Python 重写, 零重依赖)

## 本仓库定制借鉴条目

| fail closed 对齐 | 关联适用 | model-visible=logged 不变量与 pregate fail closed 同源 (无法验证 = 拒绝) | ✅ 方法论一致 |
| 审计闭环 | 关联适用 | LLM 调用审计可与 pregate review 步骤叠加 | ⏳ 待评估 |
