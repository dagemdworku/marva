import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from core.constants import AGENT_CHOICES, AGENT_DETAILS

from core.agents.analyzer import SocialMediaAnalyzerAgent
from core.agents.comment_replier import CommentReplierAgent
from core.agents.content_creator import ContentCreatorAgent
from core.agents.strategist import MarketingStrategistAgent


@csrf_exempt
def chat_view(request):
    response = ""
    user_prompt = ""
    agent_key = "marketing_strategist"

    if request.method == "POST":
        user_prompt = request.POST.get("prompt", "")
        agent_key = request.POST.get("agent", "")

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
            raise ValueError("Invalid agent selected")

        agent = agent_cls()
        response = agent.execute(user_prompt=user_prompt)

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({
                "response": response,
                "prompt": user_prompt,
                "agent": agent_key,
            })

    return render(
        request,
        "core/chat.html", {
            "business_name": "The Comfort Alchemists",
            "agent_choices": AGENT_CHOICES,
            "agent_details": json.dumps(AGENT_DETAILS),
            "response": response,
            "agent": agent_key,
            "prompt": user_prompt
        }
    )
