# Changelog

## v2.1.0 — 2026-10-05（笨咪）

- 增加 `_llm_reasoning_content` 兜底读取
- 增加 `<think>` 与 `<thinking>` 标签兼容解析
- 成功发送后同时清理响应字段和事件 extra，避免重复发送
- 保持使用 AstrBot 标准 `event.send()` 消息链，兼容 Den 前端

## v2.0.0 — 2026-05-20

- 转发思考链


## v1.0.0 — 2026-04-30

- 初始版本
- 拦截 `on_llm_response`，检测 `reasoning_content` 字段
- 思考链非空时通过 `event.send()` 在正文前单独发送
