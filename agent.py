"""Lab 05: A* search with a knowledge-base feasibility check."""
import heapq
from logic_engine import KnowledgeBase


class GreedyGridAgent:
    """Keep the starter class name so simulator.py still imports it."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']
        self.moves = {'Up': (0, 1), 'Down': (0, -1),
                      'Left': (-1, 0), 'Right': (1, 0)}
        self.kb = KnowledgeBase()
        self.kb.tell_rule(['TargetVisible', 'HasDust'], 'SafeToEngage')
        self.kb.tell_rule(['SafeToEngage', 'BloodseekerMissing'], 'Retreat')

    def is_feasible(self, tile, percept):
        # These demo sensors are supplied by the environment for each tile.
        self.kb.clear_facts()
        if tile in percept['target_visible_tiles']:
            self.kb.tell_fact('TargetVisible')
        if percept['has_dust']:
            self.kb.tell_fact('HasDust')
        if percept['bloodseeker_missing']:
            self.kb.tell_fact('BloodseekerMissing')
        self.kb.forward_chain()
        return 'Retreat' not in self.kb.facts

    def a_star_search(self, start, goal, percept):
        start, goal = tuple(start), tuple(goal)
        width, height = percept['grid_size']
        walls = {tuple(wall) for wall in percept['walls']}
        def inside(tile):
            return 0 <= tile[0] < width and 0 <= tile[1] < height
        if not inside(start) or not inside(goal) or start in walls or goal in walls:
            return None
        def heuristic(tile):
            return abs(tile[0] - goal[0]) + abs(tile[1] - goal[1])
        open_list = [(heuristic(start), 0, start, [])]
        best_cost = {start: 0}
        while open_list:
            _, cost, current, path = heapq.heappop(open_list)
            if cost != best_cost[current]:
                continue
            if current == goal:
                return path
            for action, (dx, dy) in self.moves.items():
                neighbor = (current[0] + dx, current[1] + dy)
                # Reachability: within the map and not a wall.
                if not inside(neighbor) or neighbor in walls:
                    continue
                # Feasibility: clear facts, sense this tile, infer, reject Retreat.
                if not self.is_feasible(neighbor, percept):
                    continue
                next_cost = cost + 1
                if next_cost < best_cost.get(neighbor, float('inf')):
                    best_cost[neighbor] = next_cost
                    heapq.heappush(open_list, (next_cost + heuristic(neighbor),
                                              next_cost, neighbor, path + [action]))
        return None

    def sense_and_act(self, percept: dict) -> str:
        # Replan on every turn so changed safety facts are used immediately.
        start = tuple(percept['agent_pos'])
        best_path = None
        for goal in sorted(percept['food_positions']):
            if tuple(goal) == start and not self.is_feasible(start, percept):
                continue
            path = self.a_star_search(start, goal, percept)
            if path is not None and (best_path is None or len(path) < len(best_path)):
                best_path = path
        # Never fall back to random movement into a rejected tile.
        return best_path[0] if best_path else 'Stay'
