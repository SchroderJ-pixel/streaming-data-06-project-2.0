import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from utils.utils_state import volume_totals

fig, ax = plt.subplots()

def update(frame):
    ax.clear()
    groups = list(volume_totals.keys())
    values = list(volume_totals.values())
    ax.bar(groups, values, color="skyblue")
    ax.set_ylabel("Training Volume (reps × weight)")
    ax.set_title("Live Workout Tracker")

ani = FuncAnimation(fig, update, interval=2000)
plt.show()
