import numpy as np
import matplotlib.pyplot as plt

# Grid definition
x = np.linspace(0, 10, 20)
y = np.linspace(0, 10, 20)
X, Y = np.meshgrid(x, y)

# Robot 1 moves towards (8, 8)
goal1 = np.array([8, 8])
U1 = goal1[0] - X
V1 = goal1[1] - Y
mag1 = np.sqrt(U1**2 + V1**2)
U1 /= mag1
V1 /= mag1

# Robot 2 moves towards (2, 2)
goal2 = np.array([2, 2])
U2 = goal2[0] - X
V2 = goal2[1] - Y
mag2 = np.sqrt(U2**2 + V2**2)
U2 /= mag2
V2 /= mag2

# Combine vector fields (e.g., overlay)
plt.figure(figsize=(8, 8))
plt.quiver(X, Y, U1, V1, color='r', label='Robot 1 direction')
plt.quiver(X, Y, U2, V2, color='b', alpha=0.5, label='Robot 2 direction')

# Mark goals
plt.plot(goal1[0], goal1[1], 'ro', label='Goal 1')
plt.plot(goal2[0], goal2[1], 'bo', label='Goal 2')

plt.title("Vector Field of Two Robots Moving to Different Goals")
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.axis('equal')
plt.grid(True)
plt.show()
