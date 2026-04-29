from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger


@register(
    "astrbot_plugin_show_reasoning",
    "Felis Abyssalis & Abyss AI",
    "在正文之前单独发送 LLM 思考链",
    "1.0.0",
)
class ShowReasoningPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.on_llm_response()
    async def show_reasoning(self, event: AstrMessageEvent, resp):
        try:
            thinking = getattr(resp, "reasoning_content", None)
            if thinking and isinstance(thinking, str) and thinking.strip():
                await event.send(event.plain_result(f"💭 思考链\n\n{thinking.strip()}"))
                logger.info(f"已将思考链发送给 Felis Abyssalis。💜")
        except Exception as e:
            logger.error(f"发送思考链失败: {e}")

        return resp
