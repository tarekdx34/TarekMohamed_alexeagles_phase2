from flask import Flask, request, jsonify
import networkx as nx
import random
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/api/generate-maze', methods=['POST'])
def generate_maze():
    data = request.json
    difficulty = data.get('difficulty', 'medium')

    grid_size = 8
    maze = nx.grid_2d_graph(grid_size, grid_size)
    start_node, target_node = generate_random_start_and_target(grid_size)

    obstacles_number = {'easy': 10, 'medium': 15, 'hard': 20}[difficulty]
    obstacles = generate_random_obstacles(grid_size, obstacles_number, start_node, target_node)
    maze.remove_nodes_from(obstacles)

    maze_data = [['O' if (i, j) in obstacles else '' for j in range(grid_size)] for i in range(grid_size)]

    return jsonify({'maze': maze_data, 'start': start_node, 'target': target_node})

@app.route('/api/solve-maze', methods=['POST'])
def solve_maze():
    data = request.json
    maze_data = data.get('maze')
    start_node = tuple(data.get('start'))
    target_node = tuple(data.get('target'))

    grid_size = len(maze_data)
    maze = nx.grid_2d_graph(grid_size, grid_size)
    for i, row in enumerate(maze_data):
        for j, cell in enumerate(row):
            if cell == 'O':
                maze.remove_node((i, j))

    try:
        path = nx.astar_path(maze, start_node, target_node, heuristic=manhattan_heuristic)
        return jsonify({'path': path})
    except nx.NetworkXNoPath:
        return jsonify({'error': 'No path found'}, 404)

def generate_random_obstacles(grid_size, obstacles_number, start_node, target_node):
    all_nodes = list(nx.grid_2d_graph(grid_size, grid_size).nodes())
    all_nodes.remove(start_node)
    all_nodes.remove(target_node)
    obstacles = random.sample(all_nodes, obstacles_number)
    return obstacles

def generate_random_start_and_target(grid_size):
    all_nodes = list(nx.grid_2d_graph(grid_size, grid_size).nodes())
    start_node = random.choice(all_nodes)
    all_nodes.remove(start_node)
    target_node = random.choice(all_nodes)
    return start_node, target_node

def manhattan_heuristic(u, v):
    ux, uy = u
    vx, vy = v
    return abs(ux - vx) + abs(uy - vy)

if __name__ == '__main__':
    app.run(debug=True)
