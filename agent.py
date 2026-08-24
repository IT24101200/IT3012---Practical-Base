import random
from collections import deque
import heapq
import math

class SimpleReflexAgent:
    """
    Simple Reflex Agent from previous practicals.

    It reacts only to the current percept.
    """

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:

        # If food is here, move randomly
        # because there is no complete world model.
        if percept.get('food_here', False):
            return random.choice(self.actions_pool)

        # If there is a wall, choose another direction
        if percept.get('wall_ahead', False):
            return random.choice(
                ['Left', 'Right', 'Up', 'Down']
            )

        # Otherwise move randomly
        return random.choice(self.actions_pool)


class ModelBasedAgent:
    """
    Model-Based Agent from previous practicals.

    This agent keeps simple internal memory.
    """

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']
        self.previous_action = None

    def sense_and_act(self, percept: dict) -> str:

        possible_actions = self.actions_pool.copy()

        # If there is a wall, try a different action
        if percept.get('wall_ahead', False):

            if self.previous_action in possible_actions:
                possible_actions.remove(self.previous_action)

        # Avoid returning the same action twice
        # when possible.
        if self.previous_action in possible_actions and len(possible_actions) > 1:
            possible_actions.remove(self.previous_action)

        action = random.choice(possible_actions)

        self.previous_action = action

        return action


class SearchAgent:
    """
    Goal-Based Search Agent.

    This agent uses:
        1. Breadth-First Search (BFS)
        2. Depth-First Search (DFS)
        3. Uniform-Cost Search (UCS)

    The agent creates an offline plan first and
    then executes the actions one by one.
    """

    def __init__(self):

        # Stores the planned actions
        self.plan = []

        # Select the active search algorithm
        # Change to 'DFS' or 'UCS' when testing.
        self.active_algo = 'AStar'
        
        # Testing Checkpoint
        print(f"Manhattan distance from (0,0) to (3,4): {self.manhattan_distance((0,0), (3,4))}")
        print(f"Euclidean distance from (0,0) to (3,4): {self.euclidean_distance((0,0), (3,4))}")


    def get_neighbors(self, state, walls, grid_size):

        x, y = state

        width, height = grid_size

        possible_moves = [
            ((x, y + 1), 'Up'),
            ((x + 1, y), 'Right'),
            ((x, y - 1), 'Down'),
            ((x - 1, y), 'Left')
        ]

        neighbors = []

        for next_state, action in possible_moves:

            nx, ny = next_state

            # Check grid boundaries
            if nx < 0 or nx >= width:
                continue

            if ny < 0 or ny >= height:
                continue

            # Check walls
            if next_state in walls:
                continue

            neighbors.append(
                (next_state, action)
            )

        return neighbors

    def manhattan_distance(self, pos, goal):
        x_1, y_1 = pos
        x_2, y_2 = goal
        return abs(x_1 - x_2) + abs(y_1 - y_2)

    def euclidean_distance(self, pos, goal):
        x_1, y_1 = pos
        x_2, y_2 = goal
        return math.sqrt((x_1 - x_2)**2 + (y_1 - y_2)**2)

    def astar_search(self, start_pos, goal_pos, walls, grid_size, heuristic_type='manhattan'):
        frontier = []
        reached_states = set()

        g_n = 0
        if heuristic_type == 'manhattan':
            h_n = self.manhattan_distance(start_pos, goal_pos)
        else:
            h_n = self.euclidean_distance(start_pos, goal_pos)
        f_n = g_n + h_n

        heapq.heappush(frontier, (f_n, g_n, start_pos, []))

        while frontier:
            f_cost, g_cost, current_pos, path_taken = heapq.heappop(frontier)

            if current_pos == goal_pos:
                return path_taken

            if current_pos not in reached_states:
                reached_states.add(current_pos)

                for next_state, action in self.get_neighbors(current_pos, walls, grid_size):
                    if next_state not in reached_states:
                        g_new = g_cost + 1
                        if heuristic_type == 'manhattan':
                            h_new = self.manhattan_distance(next_state, goal_pos)
                        else:
                            h_new = self.euclidean_distance(next_state, goal_pos)
                        f_new = g_new + h_new
                        
                        heapq.heappush(frontier, (f_new, g_new, next_state, path_taken + [action]))

        return []


    def bfs_search(self, start, goal, walls, grid_size):
        """
        Breadth-First Search.

        BFS uses a FIFO queue.

        popleft() removes the first item from
        the queue.

        BFS finds the shortest path when every
        movement has the same cost.
        """

        # Queue:
        # (state, path)
        frontier = deque()

        frontier.append(
            (start, [])
        )

        # Reached set prevents revisiting states
        reached = set()

        reached.add(start)

        while frontier:

            # FIFO
            current, path = frontier.popleft()

            # Goal found
            if current == goal:
                return path

            # Explore neighbours
            for next_state, action in self.get_neighbors(
                    current,
                    walls,
                    grid_size):

                if next_state not in reached:

                    reached.add(next_state)

                    new_path = path + [action]

                    frontier.append(
                        (next_state, new_path)
                    )

        # Goal cannot be reached
        return []


    def dfs_search(self, start, goal, walls, grid_size):
        """
        Depth-First Search.

        DFS uses a LIFO stack.

        pop() removes the last item.
        """

        # Stack:
        # (state, path)
        frontier = []

        frontier.append(
            (start, [])
        )

        # Reached set
        reached = set()

        reached.add(start)

        while frontier:

            # LIFO
            current, path = frontier.pop()

            # Goal found
            if current == goal:
                return path

            # Explore neighbours
            for next_state, action in self.get_neighbors(
                    current,
                    walls,
                    grid_size):

                if next_state not in reached:

                    reached.add(next_state)

                    new_path = path + [action]

                    frontier.append(
                        (next_state, new_path)
                    )

        # Goal cannot be reached
        return []


    def ucs_search(self, start, goal, walls, grid_size):
        """
        Uniform-Cost Search.

        UCS uses a priority queue.

        The node with the lowest total path
        cost is expanded first.
        """

        # Priority queue:
        #
        # (cost, counter, state, path)
        #
        # counter is used to avoid comparing
        # states when costs are equal.

        frontier = []

        counter = 0

        heapq.heappush(
            frontier,
            (0, counter, start, [])
        )

        # Store cheapest cost found
        # for each state
        reached = {}

        reached[start] = 0

        while frontier:

            cost, _, current, path = heapq.heappop(
                frontier
            )

            # Goal found
            if current == goal:
                return path

            # Explore neighbours
            for next_state, action in self.get_neighbors(
                    current,
                    walls,
                    grid_size):

                # Every movement costs 1
                new_cost = cost + 1

                # If this state is new
                # or we found a cheaper path
                if (
                    next_state not in reached
                    or new_cost < reached[next_state]
                ):

                    reached[next_state] = new_cost

                    counter += 1

                    new_path = path + [action]

                    heapq.heappush(
                        frontier,
                        (
                            new_cost,
                            counter,
                            next_state,
                            new_path
                        )
                    )

        # Goal cannot be reached
        return []


    def find_closest_food(
            self,
            start,
            all_food,
            walls,
            grid_size):

        if not all_food:
            return None

        closest_food = None
        shortest_path = None

        # Check every food position
        for food in all_food:

            path = self.bfs_search(
                start,
                food,
                walls,
                grid_size
            )

            # Ignore unreachable food
            if not path and start != food:
                continue

            # Select shortest path
            if (
                shortest_path is None
                or len(path) < len(shortest_path)
            ):

                closest_food = food
                shortest_path = path

        return closest_food



    def create_plan(
            self,
            start,
            goal,
            walls,
            grid_size):

        if self.active_algo == 'BFS':

            return self.bfs_search(
                start,
                goal,
                walls,
                grid_size
            )

        elif self.active_algo == 'DFS':

            return self.dfs_search(
                start,
                goal,
                walls,
                grid_size
            )

        elif self.active_algo == 'UCS':

            return self.ucs_search(
                start,
                goal,
                walls,
                grid_size
            )

        elif self.active_algo == 'AStar':

            return self.astar_search(
                start,
                goal,
                walls,
                grid_size
            )

        else:

            print(
                "Invalid search algorithm:",
                self.active_algo
            )

            return []



    def sense_and_act(self, percept: dict):
        """
        Create a complete plan when no plan exists.

        Then execute one action from the plan.
        """



        if not self.plan:

            # Current agent position
            start = tuple(
                percept['agent_pos']
            )

            # Global environment information
            grid_size = percept['grid_size']

            walls = set(
                tuple(wall)
                for wall in percept['walls']
            )

            all_food = [
                tuple(food)
                for food in percept['all_food']
            ]

            # Find closest food
            goal = self.find_closest_food(
                start,
                all_food,
                walls,
                grid_size
            )

            # If no food is reachable
            if goal is None:
                return random.choice(
                    ['Up', 'Down', 'Left', 'Right']
                )

            # Create plan
            self.plan = self.create_plan(
                start,
                goal,
                walls,
                grid_size
            )


        if self.plan:

            return self.plan.pop(0)

        # No action available
        return random.choice(
            ['Up', 'Down', 'Left', 'Right']
        )


class GreedyGridAgent:
    """
    Original agent from the base project.

    Kept here so the previous practical code
    does not completely break.
    """

    def __init__(self):
        self.actions_pool = [
            'Up',
            'Down',
            'Left',
            'Right'
        ]

    def sense_and_act(self, percept: dict) -> str:

        pos = percept['agent_pos']

        return random.choice(
            self.actions_pool
        )