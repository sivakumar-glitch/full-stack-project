import json
import os

import requests
from django.db.models import Avg, Count
from django.db.models.functions import TruncDate
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Ticket
from .serializers import TicketSerializer


LLM_PROMPT = (
    "You are a support ticket classifier. "
    "Given a ticket description, choose exactly one category and one priority. "
    "Valid categories: billing, technical, account, general. "
    "Valid priorities: low, medium, high, critical. "
    "Return ONLY valid JSON with no extra text: {\"category\": \"...\", \"priority\": \"...\"}"
)


def _normalize_choice(value, choices):
    if value is None:
        return None
    value = str(value).strip().lower()
    return value if value in choices else None


def classify_description(description):
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        return None, None

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"{LLM_PROMPT}\n\nTicket Description: {description}"
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code != 200:
            return None, None
        
        data = response.json()
        text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        
        # Extract JSON from response
        import re
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if not json_match:
            return None, None
        
        payload = json.loads(json_match.group())
    except Exception:
        return None, None

    category = _normalize_choice(payload.get("category"), Ticket.Category.values)
    priority = _normalize_choice(payload.get("priority"), Ticket.Priority.values)
    return category, priority


class TicketViewSet(viewsets.ModelViewSet):
	serializer_class = TicketSerializer
	queryset = Ticket.objects.all().order_by("-created_at")
	filterset_fields = ["category", "priority", "status"]
	search_fields = ["title", "description"]


class TicketStatsView(APIView):
	def get(self, request):
		total_tickets = Ticket.objects.count()
		open_tickets = Ticket.objects.filter(status=Ticket.Status.OPEN).count()

		per_day = (
			Ticket.objects.annotate(day=TruncDate("created_at"))
			.values("day")
			.annotate(count=Count("id"))
		)
		avg_tickets_per_day = per_day.aggregate(avg=Avg("count"))["avg"] or 0

		priority_counts = Ticket.objects.values("priority").annotate(count=Count("id"))
		category_counts = Ticket.objects.values("category").annotate(count=Count("id"))

		priority_breakdown = {item["priority"]: item["count"] for item in priority_counts}
		category_breakdown = {item["category"]: item["count"] for item in category_counts}

		for value in Ticket.Priority.values:
			priority_breakdown.setdefault(value, 0)
		for value in Ticket.Category.values:
			category_breakdown.setdefault(value, 0)

		return Response(
			{
				"total_tickets": total_tickets,
				"open_tickets": open_tickets,
				"avg_tickets_per_day": round(float(avg_tickets_per_day), 2),
				"priority_breakdown": priority_breakdown,
				"category_breakdown": category_breakdown,
			}
		)


class TicketClassifyView(APIView):
	def post(self, request):
		description = str(request.data.get("description", "")).strip()
		if not description:
			return Response(
				{"detail": "description is required"},
				status=status.HTTP_400_BAD_REQUEST,
			)

		category, priority = classify_description(description)
		return Response(
			{
				"suggested_category": category,
				"suggested_priority": priority,
			}
		)

# Create your views here.
