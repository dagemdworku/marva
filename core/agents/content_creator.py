from core.agents.base import AbstractAgent
from core.constants import AGENT_DETAILS
from core.tools.pdf_reader import read_company_bio
from core.tools.db_query_tool import get_post_insights


class ContentCreatorAgent(AbstractAgent):
    def __init__(self):
        tools = [read_company_bio, get_post_insights]
        super().__init__(tools=tools)

    def execute(self, user_prompt: str, stream_callback=None) -> str:
        system_prompt = AGENT_DETAILS["content_creator"]["system_prompt"]
        return self.run(system_prompt=system_prompt, user_prompt=user_prompt, stream_callback=stream_callback)
