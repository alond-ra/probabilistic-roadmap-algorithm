import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import LineString, Polygon, Point
from scipy.spatial import Voronoi, voronoi_plot_2d

def line_intersects(p1, p2, x, y):
    linea = LineString([p1, p2])
    obstaculo = Polygon([(x[0], y[0]), (x[1], y[1]), (x[2], y[2])])
    return linea.intersects(obstaculo)

def collision_free(p1, p2, obstacles):
    for obstacle in obstacles:
        x, y = obstacle
        if line_intersects(p1, p2, x,y):
            return False
    return True

def sample_in_obstacle(px, py, obstacles):
    punto = Point(px, py)
    for obstacle in obstacles:
        x, y = obstacle
        triangulo = Polygon([(x[0], y[0]), (x[1], y[1]), (x[2], y[2])])
        if triangulo.contains(punto) or triangulo.touches(punto):
            return True
    return False

def initialize_samples(samples,full_samples,x_lim, y_lim, obstacles, initial_size=5000):
    while len(samples) < initial_size:
        px, py = np.random.uniform(low=[x_lim[0], y_lim[0]], high=[x_lim[1], y_lim[1]])
        if not sample_in_obstacle(px, py, obstacles):
            samples.append([px, py])
        
        full_samples.append([px, py])
    samples = np.array(samples)



def calculate_triangle_area(vertices):
    x1, y1 = vertices[0]
    x2, y2 = vertices[1]
    x3, y3 = vertices[2]

    area = 0.5 * abs(x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2))
    # print(area)
    return area


def plot_PRM(V, E, radio, obstacles, x_lim, y_lim,start=None, goal=None, path=None):
    plt.figure(figsize=(10, 10))
    
    V_array = np.array(V)
    num_muestras = len(V)
    if(V):
        plt.scatter(V_array[:, 0], V_array[:, 1], c='b', s=10)

    for edge in E:
        plt.plot([V[edge[0]][0], V[edge[1]][0]], [V[edge[0]][1], V[edge[1]][1]], 'k-', lw=0.3)

    for obstacle in obstacles:
        obstacle_polygon = plt.Polygon(
                [(obstacle[0][0], obstacle[1][0]),
                (obstacle[0][1], obstacle[1][1]),
                (obstacle[0][2], obstacle[1][2])],
                color='black',  alpha=0.6)
        plt.gca().add_patch(obstacle_polygon)

    if path is not None:
        for i in range(len(path)-1):
            plt.plot([path[i][0], path[i+1][0]], [path[i][1], path[i+1][1]], 'r-', lw=2)
        num_muestras = len(V) - 2

    if start is not None:
        plt.plot(start[0], start[1], 'go', markersize=10, label='start')
        plt.plot(goal[0], goal[1], 'ro', markersize=10, label='goal')

    plt.xlim(x_lim)
    plt.ylim(y_lim)
    plt.title(f"PRM - Muestras: {num_muestras}, radio: {radio}")
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

def radical_inverse(n, b):
    # Van der Corput
    result = 0.0
    f = 1.0 / b
    i = n
    while i > 0:
        result += f * (i % b)
        i = i // b
        f = f / b
    return result

def plot_halton_voronoi(N, b1=2, b2=3):
    def halton_sequence(N, b1=2, b2=3):
        points = np.zeros((N, 2))
        for n in range(N):
            points[n, 0] = radical_inverse(n, b1)
            points[n, 1] = radical_inverse(n, b2)
        return points

    points = halton_sequence(N, b1, b2)

    plt.figure(figsize=(10, 10))
    plt.scatter(points[:, 0], points[:, 1], color='blue', s=10)
    plt.title(f'Halton (N={N} puntos, b=({b1},{b2}))')
    plt.xlabel(r'$\frac{i}{N}$', fontsize=14)
    plt.ylabel(r'$\phi_b(i)$', fontsize=14)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

    vor = Voronoi(points)
    fig, ax = plt.subplots(figsize=(10, 10))
    voronoi_plot_2d(vor, ax=ax, show_points=False, show_vertices=False,
                   line_colors='black', line_width=1, line_alpha=0.5)
    ax.scatter(points[:, 0], points[:, 1], color='blue', s=30, zorder=10)
    ax.set_title(f'Halton Voronoi - N={N} puntos, base b=({b1},{b2}))')
    ax.set_xlabel(r'$\phi_{'+str(b1)+'}(i)$', fontsize=14)
    ax.set_ylabel(r'$\phi_{'+str(b2)+'}(i)$', fontsize=14)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    plt.show()


def plot_hammersley_voronoi(N, b=2):
    def hammersley_sequence(N, b=2):
        points = np.zeros((N, 2))
        for n in range(N):
            points[n, 0] = n / N
            points[n, 1] = radical_inverse(n, b)  # Van der Corput 2D
        return points

    points = hammersley_sequence(N, b)

    plt.figure(figsize=(10, 10))
    plt.scatter(points[:, 0], points[:, 1], color='blue', s=10)
    plt.title(f'Hammersley (N={N} puntos, base b={b})')
    plt.xlabel(r'$\frac{i}{N}$', fontsize=14)
    plt.ylabel(r'$\phi_b(i)$', fontsize=14)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

    vor = Voronoi(points)
    fig, ax = plt.subplots(figsize=(10, 10))
    voronoi_plot_2d(vor, ax=ax, show_points=False, show_vertices=False, line_colors='black', line_width=1, line_alpha=0.5)
    ax.scatter(points[:, 0], points[:, 1], color='blue', s=30, zorder=10)

    ax.set_title(f'Voronoi - N={N} puntos, base b={b}')
    ax.set_xlabel(r'$\frac{i}{N}$', fontsize=14)
    ax.set_ylabel(r'$\phi_b(i)$', fontsize=14)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    plt.show()


def filter_samples(seq_points, obstacles):
    filtered_points = []
    for point in seq_points:
        if not sample_in_obstacle(point[0], point[1], obstacles):
            filtered_points.append(point)
    return np.array(filtered_points)
