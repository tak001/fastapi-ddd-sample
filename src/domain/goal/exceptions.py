class GoalValidationError(Exception):
    pass


class GoalNotFoundError(Exception):
    def __init__(self, goal_id: str) -> None:
        super().__init__(f"Goal not found: {goal_id}")
        self.goal_id = goal_id
