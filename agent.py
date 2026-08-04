# agent.py
class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)

class SimpleReflexAgent:

    def sense_and_act(self, percept):

        # Rule 1: Eat food if it is here
        if percept["food_here"]:
            return "EAT"

        # Rule 2: Move right if there is no wall
        if not percept["wall_right"]:
            return "RIGHT"

        # Rule 3: Otherwise move down
        if not percept["wall_down"]:
            return "DOWN"

        # Rule 4: Otherwise move left
        if not percept["wall_left"]:
            return "LEFT"

        # Rule 5: Otherwise move up
        if not percept["wall_up"]:
            return "UP"

        # If surrounded by walls
        return "STAY"

class ModelBasedAgent:

    def __init__(self):
        # Memory of places the agent has already visited
        self.visited_cells = set()

    def sense_and_act(self, percept):

        # Get current position if available
        current_position = tuple(percept.get("agent_pos", ()))

        # Update memory
        if current_position:
            self.visited_cells.add(current_position)

        # Rule 1: Eat food if it is here
        if percept["food_here"]:
            return "EAT"

        # Rule 2: Choose a direction that is not blocked
        # (Later you can improve this by checking visited cells.)

        if not percept["wall_right"]:
            return "RIGHT"

        if not percept["wall_down"]:
            return "DOWN"

        if not percept["wall_left"]:
            return "LEFT"

        if not percept["wall_up"]:
            return "UP"

        return "STAY"        