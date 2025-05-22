from core.agents.base import AbstractAgent
from core.constants import AGENT_DETAILS
from core.tools.db_query_tool import get_post_insights


class SocialMediaAnalyzerAgent(AbstractAgent):
    def __init__(self):
        tools = [get_post_insights]
        super().__init__(tools=tools)

    def execute(self, user_prompt: str, stream_callback=None) -> str:
        system_prompt = AGENT_DETAILS["social_media_analyzer"]["system_prompt"]
        return self.run(system_prompt=system_prompt, user_prompt=user_prompt, stream_callback=stream_callback)
