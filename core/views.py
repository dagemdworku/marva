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
