from collections import defaultdict

# Dictionary for running totals
volume_totals = defaultdict(int)

def update_volume(muscle_group: str, reps: int, weight: int):
    volume_totals[muscle_group] += reps * weight
    return volume_totals

