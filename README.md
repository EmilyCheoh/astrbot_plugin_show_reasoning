# astrbot_plugin_show_reasoning

在正文之前单独发送 LLM 思考链。

## 功能

当 LLM 返回包含思考链（`reasoning_content`）时，插件会在正文回复之前，先发送一条以 `💭 思考链` 开头的消息，将模型的推理过程完整展示出来。

- 仅在思考链非空时触发，不影响正常对话
- 无需配置，装上即用

## 安装

将 `show_reasoning/` 文件夹放入 AstrBot 插件目录（如 `/data/astrbot/plugins/show_reasoning/`），重启 AstrBot。