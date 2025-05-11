import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation

# Pendulum rod lengths (m), bob masses (kg).
L1, L2 = 1, 1
m1, m2 = 1, 1
# The gravitational acceleration (m.s-2).
g = 9.81

def deriv(y, t, L1, L2, m1, m2):
    """Return the first derivatives of y = theta1, z1, theta2, z2."""
    theta1, z1, theta2, z2 = y

    c, s = np.cos(theta1-theta2), np.sin(theta1-theta2)

    theta1dot = z1
    z1dot = (m2*g*np.sin(theta2)*c - m2*s*(L1*z1**2*c + L2*z2**2) -
             (m1+m2)*g*np.sin(theta1)) / L1 / (m1 + m2*s**2)
    theta2dot = z2
    z2dot = ((m1+m2)*(L1*z1**2*s - g*np.sin(theta2) + g*np.sin(theta1)*c) + 
             m2*L2*z2**2*s*c) / L2 / (m1 + m2*s**2)
    return theta1dot, z1dot, theta2dot, z2dot

def calc_E(y):
    """Return the total energy of the system."""
    th1, th1d, th2, th2d = y.T
    V = -(m1+m2)*L1*g*np.cos(th1) - m2*L2*g*np.cos(th2)
    T = 0.5*m1*(L1*th1d)**2 + 0.5*m2*((L1*th1d)**2 + (L2*th2d)**2 +
            2*L1*L2*th1d*th2d*np.cos(th1-th2))
    return T + V

# Maximum time, time point spacings and the time grid (all in s).
tmax, dt = 30, 0.01
t = np.arange(0, tmax+dt, dt)
# Initial conditions: theta1, dtheta1/dt, theta2, dtheta2/dt.
y0 = np.array([3*np.pi/7, 0, 3*np.pi/4, 0])

# Do the numerical integration of the equations of motion
y = odeint(deriv, y0, t, args=(L1, L2, m1, m2))

# Check that the calculation conserves total energy to within some tolerance.
EDRIFT = 0.05
# energy from the initial conditions
E = calc_E(y0)
if np.max(np.sum(np.abs(calc_E(y) - E))) > EDRIFT:
    print('Maximum energy drift exceeded!')

# Unpack z and theta as a function of time
theta1, theta2 = y[:,0], y[:,2]

# Convert to Cartesian coordinates of the two bob positions.
x1 = L1 * np.sin(theta1)
y1 = -L1 * np.cos(theta1)
x2 = x1 + L2 * np.sin(theta2)
y2 = y1 - L2 * np.cos(theta2)

r = 0.05
trail_secs = 1
max_trail = int(trail_secs / dt)

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-L1-L2-r, L1+L2+r)
ax.set_ylim(-L1-L2-r, L1+L2+r)
ax.set_aspect('equal', adjustable='box')
plt.axis('off')

# Objects that will be updated in the animation
line, = ax.plot([], [], 'k-', lw=2)  # the pendulum rods
trail, = ax.plot([], [], 'r-', alpha=0.5, lw=2)  # trail of bob 2
circle0 = Circle((0, 0), r/2, fc='k', zorder=10)  # anchor point
circle1 = Circle((0, 0), r, fc='b', ec='b', zorder=10)  # bob 1
circle2 = Circle((0, 0), r, fc='r', ec='r', zorder=10)  # bob 2

ax.add_patch(circle0)
ax.add_patch(circle1)
ax.add_patch(circle2)
time_text = ax.text(0.05, 0.95, '', transform=ax.transAxes)

def init():
    """Initialize the animation"""
    line.set_data([], [])
    trail.set_data([], [])
    time_text.set_text('')
    circle1.center = (0, 0)
    circle2.center = (0, 0)
    return line, trail, time_text, circle1, circle2

def animate(i):
    """Update the animation for frame i"""
    frame_idx = i * int(1/(fps*dt))
    if frame_idx >= len(t):
        frame_idx = len(t) - 1
    
    # Update pendulum position
    line.set_data([0, x1[frame_idx], x2[frame_idx]], [0, y1[frame_idx], y2[frame_idx]])
    
    # Update bob positions
    circle1.center = (x1[frame_idx], y1[frame_idx])
    circle2.center = (x2[frame_idx], y2[frame_idx])
    
    # Update the trail of bob 2
    trail_start = max(0, frame_idx - max_trail)
    trail.set_data(x2[trail_start:frame_idx], y2[trail_start:frame_idx])
    
    # Update time text
    time_text.set_text(f'Time: {t[frame_idx]:.1f} s')
    
    return line, trail, time_text, circle1, circle2

fps = 30
frames = int(tmax * fps)
ani = FuncAnimation(fig, animate, frames=frames, init_func=init, 
                    interval=1000/fps, blit=True)


plt.tight_layout()
plt.show()