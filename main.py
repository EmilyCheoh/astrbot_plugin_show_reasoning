import re

from astrbot.api import logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.message_components import Node, Plain
from astrbot.api.star import Context, Star, register


@register(
    "astrbot_plugin_show_reasoning",
    "Felis Abyssalis & Abyss AI",
    "以合并转发消息的形式发送 LLM 思考链",
    "2.1.0",
)
class ShowReasoningPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.on_llm_response(priority=-9999)
    async def show_reasoning(self, event: AstrMessageEvent, resp):
        try:
            thinking = getattr(resp, "reasoning_content", None)

            # AstrBot copies reasoning_content here before running this hook.
            if not thinking:
                thinking = event.get_extra("_llm_reasoning_content")

            # Compatibility fallback for providers that place reasoning in text.
            if not thinking:
                completion_text = getattr(resp, "completion_text", None)
                if isinstance(completion_text, str):
                    pattern = re.compile(
                        r"<(think|thinking)>(.*?)</\1>",
                        re.DOTALL | re.IGNORECASE,
                    )
                    matches = pattern.findall(completion_text)
                    if matches:
                        thinking = "\n".join(
                            content.strip() for _, content in matches if content.strip()
                        )
                        resp.completion_text = pattern.sub("", completion_text).strip()

            if not thinking:
                return resp

            thinking_text = str(thinking).strip()
            if not thinking_text:
                return resp

            nodes = [
                Node(
                    uin=0,
                    name="🤖💭The reasoning process (COT)",
                    content=[Plain(thinking_text)],
                )
            ]
            await event.send(event.chain_result(nodes))

            # Prevent AstrBot's result decoration stage from sending it again.
            if hasattr(resp, "reasoning_content"):
                resp.reasoning_content = None
            event.set_extra("_llm_reasoning_content", None)
        except Exception as e:
            logger.error(f"发送思考链失败: {e}")

        return resp
