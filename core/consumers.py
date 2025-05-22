import json
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer

from core.agents.analyzer import SocialMediaAnalyzerAgent
from core.agents.comment_replier import CommentReplierAgent
from core.agents.content_creator import ContentCreatorAgent
from core.agents.strategist import MarketingStrategistAgent


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_prompt = data.get("prompt", "")
        agent_key = data.get("agent", "")

        print(f"User prompt: {user_prompt}")
        print(f"Agent key: {agent_key}")

        agent_map = {
            "content_creator": ContentCreatorAgent,
            "comment_replier": CommentReplierAgent,
            "marketing_strategist": MarketingStrategistAgent,
            "social_media_analyzer": SocialMediaAnalyzerAgent,
        }

        agent_cls = agent_map.get(agent_key)
        if not agent_cls:
            await self.send(text_data=json.dumps({
                "error": "Invalid agent selected"
            }))
            return

        async def stream_callback(payload):
            await self.send(text_data=json.dumps({
                "step": payload.get("type"),
                "data": payload
            }))

        loop = asyncio.get_running_loop()

        def sync_stream_callback(payload):
            print(f"Sync stream callback: {payload}\n-------")
            asyncio.run_coroutine_threadsafe(stream_callback(payload), loop)
            # asyncio.get_event_loop().create_task(stream_callback(payload))

        agent = agent_cls()

        final_response = await asyncio.to_thread(
            agent.execute, user_prompt=user_prompt, stream_callback=sync_stream_callback
        )
        await self.send(text_data=json.dumps({
            "step": "final_response",
            "response": final_response,
            "prompt": user_prompt,
            "agent": agent_key
        }))
