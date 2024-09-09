import networkx as nx
import matplotlib.pyplot as plt
import random

maze = nx.grid_2d_graph(8, 8)

def generate_random_obstacles(grid_size, obstacles_number, start_node, target_node):
    all_nodes = list(maze.nodes())
    all_nodes.remove(start_node)
    all_nodes.remove(target_node)
    obstacles = random.sample(all_nodes, obstacles_number)
    return obstacles

def generate_random_start_and_target(grid_size):
    all_nodes = list(maze.nodes())
    start_node = random.choice(all_nodes)
    all_nodes.remove(start_node)  # Ensure start and target are different
    target_node = random.choice(all_nodes)
    return start_node, target_node

# Generate random start and target nodes
start_node, target_node = generate_random_start_and_target(8)

# Generate random obstacles
obstacles_number = random.randrange(12, 20)
obstacles = generate_random_obstacles(8, obstacles_number, start_node, target_node)
maze.remove_nodes_from(obstacles)

# Heuristic function for A* algorithm
def manhattan_heuristic(u, v):
    ux, uy = u
    vx, vy = v
    return abs(ux - vx) + abs(uy - vy)

# Find the shortest path
try:
    path = nx.astar_path(maze, start_node, target_node, heuristic=manhattan_heuristic)
    print(f"The shortest path from {start_node} to {target_node} is: {path}")
except nx.NetworkXNoPath:
    print(f"No path found from {start_node} to {target_node}.")

# Draw the grid graph
pos = {(x, y): (y, -x) for x, y in maze.nodes()}  # Positions for all nodes

# Draw nodes
nx.draw(maze, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')

# Draw obstacles
for obs in obstacles:
    plt.plot(obs[1], -obs[0], 'rs', markersize=20)  

# Highlight the path from start to goal in green
if 'path' in locals():  
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(maze, pos, edgelist=path_edges, edge_color='yellow', width=5)

# Highlight the start and goal nodes
nx.draw_networkx_nodes(maze, pos, nodelist=[start_node], node_color='green', node_size=700, label='Start')
nx.draw_networkx_nodes(maze, pos, nodelist=[target_node], node_color='blue', node_size=700, label='Goal')

plt.title("Path from Start to Goal with Random Obstacles")
plt.show()
