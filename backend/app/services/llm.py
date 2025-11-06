from __future__ import annotations

from typing import List, Dict
import os
import json


def build_prompt(lat: float, lon: float, max_time_min: int, preferences: List[str], context: Dict[str, object], poi_context: List[Dict[str, object]]) -> str:
    lines = [
        "Ты — локальный гид по Астане. Дай краткие и точные рекомендации.",
        f"Координаты пользователя: {lat:.5f}, {lon:.5f}",
        f"Время: до {max_time_min} минут",
        f"Предпочтения: {', '.join(preferences) if preferences else 'не указаны'}",
        f"Контекст: {json.dumps(context, ensure_ascii=False)}",
        "Доступные POI рядом (название | описание | расстояние м | теги):",
    ]
    for p in poi_context:
        lines.append(f"- {p['name']} | {p.get('desc','')} | {int(p['distance_m'])} | {', '.join(p.get('tags', []))}")
    lines.extend([
        "Сгенерируй 1–3 рекомендаций JSON-массивом со свойствами: name, why, actions, visit_min, confidence.",
        "Пиши только JSON, без лишнего текста.",
    ])
    return "\n".join(lines)


def generate_with_mock(prompt: str, response_count: int) -> List[Dict[str, object]]:
    # Simple rule-based output for demo
    base = [
        {
            "name": "Кафе рядом",
            "why": "Тихое место для отдыха",
            "actions": "Возьмите капучино и десерт",
            "visit_min": 40,
            "confidence": "medium",
        },
        {
            "name": "Прогулка по набережной",
            "why": "Живописный маршрут вдоль реки",
            "actions": "Пройдитесь 2-3 км и сделайте фото",
            "visit_min": 60,
            "confidence": "medium",
        },
        {
            "name": "Музей поблизости",
            "why": "Интересная экспозиция",
            "actions": "Зайдите на временную выставку",
            "visit_min": 50,
            "confidence": "low",
        },
    ]
    return base[: max(1, min(response_count, 3))]

from typing import List, Dict
import json

from ..schemas.models import POI, RecommendationItem


class MockLLM:
    def generate(self, prompt: str, count: int = 3) -> List[RecommendationItem]:
        try:
            # Extract a JSON block if present (robustness not critical for mock)
            # Fall back to trivial generation when parsing fails
            pass
        except Exception:
            pass
        # Simple mock: produce generic items to demonstrate the flow
        items: List[RecommendationItem] = []
        for i in range(count):
            items.append(
                RecommendationItem(
                    name=f"Рекомендация #{i+1}",
                    distance_m=400 + i * 100,
                    why="Подходит под указанные предпочтения",
                    visit_min=45,
                    actions="Оцените атмосферу и сделайте пару фото",
                    confidence="medium",
                    source="RAG",
                )
            )
        return items


def build_prompt(lat: float, lon: float, max_time_min: int, preferences: List[str], context: Dict[str, object], candidate_pois: List[Dict[str, object]]) -> str:
    return (
        "Вы — локальный эксперт по Астане. На основе списка POI предложите 1–3 рекомендации.\n"
        f"Пользователь сейчас находится по координатам {lat}, {lon}.\n"
        f"У него есть {max_time_min} минут, он ищет {preferences}.\n"
        f"Контекст: {json.dumps(context, ensure_ascii=False)}\n"
        "POI-кандидаты (название, описание, расстояние, теги):\n"
        f"{json.dumps(candidate_pois, ensure_ascii=False)}\n\n"
        "Формат ответа: JSON-массив объектов со свойствами name, why, actions, visit_min, confidence."
    )
