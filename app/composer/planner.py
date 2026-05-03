from typing import List, Dict, Any
from app.state.models import EngagementAction

class EngagementPlanner:
    """
    Plans the sequence of engagement actions.
    """
    def plan_next_step(self, actions: List[EngagementAction]) -> List[EngagementAction]:
        # Currently just returns prioritized actions
        return actions

planner = EngagementPlanner()
