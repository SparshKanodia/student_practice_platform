from typing import Dict, List


def categorize_skills(skills_dict: Dict[str, int]) -> Dict[str, List[str]]:
    weak = []
    medium = []
    strong = []

    for topic, score in skills_dict.items():
        if score < 40:
            weak.append(topic)
        elif score < 70:
            medium.append(topic)
        else:
            strong.append(topic)

    return {
        "weak": weak,
        "medium": medium,
        "strong": strong,
    }


def update_skill_score(old_score: int, correct: bool) -> int:
    change = 5 if correct else -5
    new_score = old_score + change
    return max(0, min(100, new_score))


def calculate_level(xp: int) -> int:
    return (xp // 100) + 1
