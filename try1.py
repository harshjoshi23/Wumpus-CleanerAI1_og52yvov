import os
from collections import deque

def load_problem_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    task_type = lines[0].strip()
    plan = ""
    map_start_idx = 1

    if task_type == "CHECK PLAN":
        plan = lines[1].strip()
        map_start_idx = 2
    
    map_representation = [line.strip() for line in lines[map_start_idx:]]
    return task_type, plan, map_representation

def move(position, direction, map_representation, portals):
    x, y = position
    moves = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}
    new_position = (x + moves[direction][0], y + moves[direction][1])

    if 0 <= new_position[0] < len(map_representation[0]) and 0 <= new_position[1] < len(map_representation):
        if map_representation[new_position[1]][new_position[0]] == 'P':
            new_position = portals.get(new_position, new_position)
        if map_representation[new_position[1]][new_position[0]] != 'X':
            return new_position
    return position

def find_portals(map_representation):
    portals = {}
    for y, row in enumerate(map_representation):
        for x, cell in enumerate(row):
            if cell == 'P':
                portals[(x, y)] = None
    portal_pairs = list(portals.keys())
    if portal_pairs:
        for i in range(0, len(portal_pairs), 2):
            portals[portal_pairs[i]] = portal_pairs[i + 1]
            portals[portal_pairs[i + 1]] = portal_pairs[i]
    return portals

def check_plan(plan, initial_position, map_representation):
    cleaned_squares = set()
    current_position = initial_position
    portals = find_portals(map_representation)

    for direction in plan:
        current_position = move(current_position, direction, map_representation, portals)
        cleaned_squares.add(current_position)
    
    all_cleaned = True
    missed_squares = []
    for y, row in enumerate(map_representation):
        for x, cell in enumerate(row):
            if cell == ' ' and (x, y) not in cleaned_squares:
                all_cleaned = False
                missed_squares.append((x, y))

    return all_cleaned, missed_squares

def find_start_position(map_representation):
    for y, row in enumerate(map_representation):
        for x, cell in enumerate(row):
            if cell == 'S':
                return (x, y)
    return None

def bfs_cleaning_plan(start_position, map_representation):
    directions = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}
    queue = deque([start_position])
    visited = set([start_position])
    plan = []

    while queue:
        current = queue.popleft()
        for d_key, (dx, dy) in directions.items():
            next_pos = (current[0] + dx, current[1] + dy)
            if 0 <= next_pos[0] < len(map_representation[0]) and 0 <= next_pos[1] < len(map_representation):
                if map_representation[next_pos[1]][next_pos[0]] != 'X' and next_pos not in visited:
                    visited.add(next_pos)
                    queue.append(next_pos)
                    plan.append(d_key)

    return ''.join(plan)

def generate_solution_file(task_type, plan, map_representation, solution_file_path):
    if task_type == "CHECK PLAN":
        initial_position = find_start_position(map_representation)
        if initial_position is None:
            print(f"No starting position found in the map for {solution_file_path}")
            return

        is_cleaned, missed_squares = check_plan(plan, initial_position, map_representation)
        result = "GOOD PLAN" if is_cleaned else "BAD PLAN\n" + "\n".join(f"{x}, {y}" for x, y in missed_squares)
        
        with open(solution_file_path, 'w') as file:
            file.write(result)
    elif task_type == "FIND PLAN":
        start_position = find_start_position(map_representation)
        if start_position is None:
            print(f"No starting position found in the map for {solution_file_path}")
            return
        
        cleaning_plan = bfs_cleaning_plan(start_position, map_representation)
        with open(solution_file_path, 'w') as file:
            file.write(cleaning_plan)
        print(f"Solution for FIND PLAN written to {solution_file_path}")

def automate_solutions(problem_directory, solution_directory):
    for file_name in os.listdir(problem_directory):
        if file_name.startswith('problem_') and file_name.endswith('.txt'):
            problem_path = os.path.join(problem_directory, file_name)
            task_type, plan, map_representation = load_problem_file(problem_path)
            solution_file_name = file_name.replace('problem_', 'solution_')
            solution_file_path = os.path.join(solution_directory, solution_file_name)
            generate_solution_file(task_type, plan, map_representation, solution_file_path)

if __name__ == "__main__":
    problem_directory = 'problems'
    solution_directory = 'example-solutions'
    automate_solutions(problem_directory, solution_directory)

