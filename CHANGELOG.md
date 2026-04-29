# Changelog

## v1.0.0 — 2026-04-30

- 初始版本
- 拦截 `on_llm_response`，检测 `reasoning_content` 字段
- 思考链非空时通过 `event.send()` 在正文前单独发送
