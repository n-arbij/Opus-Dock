from models.goal import Goal, CreateGoal, UpdateGoal, GoalResponse

class GoalService:
    def __init__(self, db):
        self.db = db

    def create_goal(self, goal_data: CreateGoal, current_user_id: int):
        new_goal = Goal(
            user_id=current_user_id,
            title=goal_data.title,
            description=goal_data.description,
            start_at=goal_data.start_at,
            end_at=goal_data.end_at,
            achieved=goal_data.achieved
        )
        self.db.add(new_goal)
        self.db.commit()
        self.db.refresh(new_goal)

        return new_goal
    
    def get_goal_by_id(self, goal_id):
        return self.db.query(Goal).filter(Goal.id == goal_id).first()
    
    def update_goal(self, goal_id, goal_data: UpdateGoal):
        goal = self.get_goal_by_id(goal_id)
        if not goal:
            raise ValueError("Goal not found")
        
        goal.title = goal_data.title or goal.title
        goal.description = goal_data.description or goal.description
        goal.start_at = goal_data.start_at or goal.start_at
        goal.end_at = goal_data.end_at or goal.end_at
        goal.achieved = goal_data.achieved if goal_data.achieved is not None else goal.achieved
        
        self.db.commit()
        self.db.refresh(goal)
        
        return goal
    
    def delete_goal(self, goal_id):
        goal = self.get_goal_by_id(goal_id)
        if not goal:
            raise ValueError("Goal not found")
        
        self.db.delete(goal)
        self.db.commit()
        
        return goal