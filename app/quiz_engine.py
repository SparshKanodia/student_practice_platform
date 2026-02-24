from typing import Dict, List

from app.skill_engine import categorize_skills


def select_adaptive_topics(skills_dict: Dict[str, int]) -> List[str]:
    categories = categorize_skills(skills_dict)
    ordered_topics = categories["weak"] + categories["medium"] + categories["strong"]

    if not ordered_topics:
        return ["tenses"]

    return ordered_topics


def generate_placeholder_questions(topics: List[str]) -> List[dict]:
    questions = []

    for i in range(10):
        topic = topics[i % len(topics)]
        questions.append(
            {
                "question": f"Placeholder question {i + 1} on {topic}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_index": 0,
                "topic": topic,
            }
        )

    return questions
