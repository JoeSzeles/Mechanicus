import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from sklearn.cluster import KMeans
from typing import Tuple

def create_plot(dimensions: Tuple[int, int]):

    # Extract width and height from dimensions
    width, height = dimensions

    # A large point count will produce more defined results
    point_count = 150

    # Generate random points
    points = np.random.rand(point_count, 2) * np.array([width, height])
    
    # The N value for k-means clustering
    # Lower values will produce bigger chunks
    cluster_count = 3

    # The list of lines to draw
    lines = []

    # Run our generative algorithm at 30 FPS
    while True:

        # Not enough points in our data set
        if len(points) <= cluster_count:
            break

        # k-means cluster our data
        kmeans = KMeans(n_clusters=cluster_count)
        kmeans.fit(points)
        clusters = [points[kmeans.labels_ == i] for i in range(cluster_count)]
        clusters = list(filter(lambda c: len(c) >= 3, clusters))

        # Ensure we resulted in some clusters
        if len(clusters) == 0:
            break

        # Sort clusters by density
        clusters.sort(key=lambda c: len(c))

        # Select the least dense cluster
        cluster = clusters[0]
        positions = cluster.tolist()
        # Find the hull of the cluster
        hull = ConvexHull(positions)

        # Ensure the hull is large enough
        if len(hull.vertices) <= 2:
            break

        # Create a closed polyline from the hull
        path = [positions[i] for i in hull.vertices]
        path.append(path[0])

        # Add to total list of polylines
        lines.append(path)

        # Remove those points from our data set
        points = np.array([p for p in points.tolist() if p not in positions])

    # Plot the lines
    for line in lines:
        plt.plot([p[0] for p in line], [p[1] for p in line], color='black')

    # Set the axis limits
    plt.xlim(0, width)
    plt.ylim(0, height)

    # Set the background color
    plt.gca().set_facecolor('white')

    # Return the plot
    return plt.gcf()
plot = create_plot((800, 800))
plt.savefig('plot.png')
plot.show()