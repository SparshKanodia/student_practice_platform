def select_adaptive_topics(skills: dict, limit: int = 3) -> list[str]:
    if not skills:
        return []

    ordered_topics = sorted(skills.items(), key=lambda item: item[1])
    return [topic for topic, _score in ordered_topics[:limit]]


def generate_placeholder_questions(topics: list[str]) -> list[dict]:
    questions = []
    for topic in topics:
        questions.append(
            {
                "topic": topic,
                "question": f"Practice question for {topic}",
                "options": ["A", "B", "C", "D"],
                "answer": "A",
            }
        )
    return questions
