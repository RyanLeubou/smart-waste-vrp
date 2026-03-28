"""
Exécution du VRP en arrière-plan (
"""

from celery import Celery
from vrp.solver import solve_vrp

app = Celery(
    "vrp_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@app.task
def compute_routes(data, time_windows):
    """
    Lance le solveur VRP avec contraintes complètes
    """
    return solve_vrp(data, time_windows)