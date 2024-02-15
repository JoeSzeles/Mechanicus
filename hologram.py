import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# Define line segment endpoints
start = np.array([0, 0, 0])
end = np.array([10, 10, 15])

# Define number of scratches
num_scratches = 10

# Calculate scratch positions
scratch_pos = np.linspace(start, end, num_scratches + 1)

# Calculate tangents
tangents = scratch_pos[1:] - scratch_pos[:-1]
tangents = tangents / np.linalg.norm(tangents, axis=1)[:, np.newaxis]
tangents = tangents.astype(np.int32) # explicitly cast to int32



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i in range(num_scratches):
    p1 = scratch_pos[i]
    p2 = scratch_pos[i+1]
    tangent = tangents[i]
    normal = np.array([-tangent[1], tangent[0], 0]) # rotate tangent by 90 degrees
    midpoint = (p1 + p2) / 2
    radius = np.linalg.norm(midpoint[:2])
    center = midpoint + radius * normal

    # Plot scratch as a circle
    theta = np.linspace(0, 2*np.pi, 100)
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    z = center[2] * np.ones_like(theta)
    ax.plot(x, y, z, 'b')

# Set plot limits and labels
ax.set_xlim(-5, 15)
ax.set_ylim(-5, 15)
ax.set_zlim(0, 15)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

# define line segment endpoints
p1 = np.array([0, 0, 0])
p2 = np.array([10, 10, 15])

# define number of scratches
N = 10

# calculate scratch midpoint positions
midpoints = np.linspace(p1, p2, N+1)[:-1] + (p2 - p1) / (2*N)
midpoints -= midpoints[0]

# calculate scratch tangent vectors
tangents = (p2 - p1).astype(float)
tangents /= np.linalg.norm(tangents)
tangents = tangents[np.newaxis, :]

# calculate scratch normal vectors
normals = np.empty((N, 3))
normals[:, 0] = -tangents[:, 1]
normals[:, 1] = tangents[:, 0]
normals[:, 2] = 0

# calculate scratch radii
radii = np.linalg.norm(midpoints, axis=1) / np.linalg.norm(normals, axis=1)

# calculate scratch angles
angles = np.zeros_like(radii)
for i in range(N-1):
    angle1 = np.arctan2(midpoints[i,1], midpoints[i,0])
    angle2 = np.arctan2(midpoints[i+1,1], midpoints[i+1,0])
    angles[i] = angle2 - angle1

# plot scratches
fig, ax = plt.subplots()
for i in range(N):
    arc = Arc(midpoints[i,:2], radii[i]*2, radii[i]*2, theta1=np.degrees(angles[i]), theta2=np.degrees(angles[i])+180, fill=False)
    ax.add_artist(arc)
    # plot line
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='black')
# set plot limits and labels
ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)
ax.set_aspect('equal')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Hologram Scratches')

# show plot
plt.show()


