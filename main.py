from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.message_components import Node, Plain
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

@register(
    "astrbot_plugin_show_reasoning",
    "Felis Abyssalis & Abyss AI",
    "以合并转发消息的形式发送 LLM 思考链",
    "2.0.0",
)
class ShowReasoningPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.on_llm_response()
    async def show_reasoning(self, event: AstrMessageEvent, resp):
        try:
            thinking = getattr(resp, "reasoning_content", None)
            if thinking and isinstance(thinking, str) and thinking.strip():
                nodes = [
                    Node(uin=0, name="🤖💭The reasoning process (COT)", content=[Plain(thinking.strip())])
                ]
                await event.send(event.chain_result(nodes))
                resp.reasoning_content = None
        except Exception as e:
            logger.error(f"发送思考链失败: {e}")

        return resp

