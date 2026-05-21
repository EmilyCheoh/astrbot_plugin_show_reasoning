from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.message_components import Node, Plain
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

MAX_CHUNK_LEN = 2000


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
                chunks = self._split_thinking(thinking.strip())
                nodes = [
                    Node(uin=0, name="🤖💭The reasoning process (COT)", content=[Plain(chunk)])
                    for chunk in chunks
                ]
                await event.send(event.chain_result(nodes))
                resp.reasoning_content = None
        except Exception as e:
            logger.error(f"发送思考链失败: {e}")

        return resp

    @staticmethod
    def _split_thinking(text: str) -> list[str]:
        """按段落边界拆分长文本，每段不超过 MAX_CHUNK_LEN。"""
        if len(text) <= MAX_CHUNK_LEN:
            return [text]

        chunks = []
        current = ""
        for para in text.split("\n\n"):
            if current and len(current) + len(para) + 2 > MAX_CHUNK_LEN:
                chunks.append(current.strip())
                current = para
            else:
                current = f"{current}\n\n{para}" if current else para

        if current.strip():
            chunks.append(current.strip())

        return chunks or [text]
