def calculate_level(xp: int) -> int:
    if xp < 0:
        return 1
    return (xp // 100) + 1


def update_skill_score(current_score: int, is_correct: bool) -> int:
    if is_correct:
        return min(100, current_score + 5)
    return max(0, current_score - 3)
