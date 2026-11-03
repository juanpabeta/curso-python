def conversion_rate(won: int, lost: int) -> float:
    return won / (won + lost) if won + lost else 0.0
