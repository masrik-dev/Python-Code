import math

# Simple free-kick trajectory analyzer for a soccer ball.
# This computes the ball path, height, horizontal distance, total distance traveled,
# lateral curve, and whether the shot would enter a regulation goal.

BALL_MASS = 0.43  # kg
AIR_DENSITY = 1.2  # kg/m^3
BALL_DIAMETER = 0.22  # meters
BALL_AREA = math.pi * (BALL_DIAMETER / 2) ** 2
DRAG_COEFFICIENT = 0.25
MAGNUS_COEFFICIENT = 8.5e-5  # tune for a visible curve
GRAVITY = 9.81  # m/s^2


def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def cross(u, v):
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


def vector_length(v):
    return math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)


def add_vector(u, v):
    return (u[0] + v[0], u[1] + v[1], u[2] + v[2])


def scale_vector(v, scalar):
    return (v[0] * scalar, v[1] * scalar, v[2] * scalar)


def simulate_free_kick(
    initial_speed,
    elevation_deg,
    azimuth_deg=0.0,
    spin_rpm=2500,
    spin_axis=(0.0, -1.0, 0.0),
    time_step=0.01,
    max_time=5.0,
    goal_distance=11.0,
    goal_width=7.32,
    goal_height=2.44,
    start_height=0.20,
):
    """Simulate a free kick and return the flight data."""
    launch_angle = math.radians(elevation_deg)
    azimuth = math.radians(azimuth_deg)
    velocity = (
        initial_speed * math.cos(launch_angle) * math.cos(azimuth),
        initial_speed * math.sin(launch_angle),
        initial_speed * math.cos(launch_angle) * math.sin(azimuth),
    )

    omega = 2.0 * math.pi * (spin_rpm / 60.0)
    spin_vector = scale_vector(spin_axis, omega)

    position = (0.0, start_height, 0.0)
    max_height = position[1]
    total_distance = 0.0
    path = [position]
    crossed_goal_plane = False
    goal_info = None

    last_position = position
    last_velocity = velocity

    for _ in range(int(max_time / time_step)):
        speed = vector_length(velocity)
        if speed <= 0.001:
            break

        # Drag acceleration
        drag_force = 0.5 * AIR_DENSITY * DRAG_COEFFICIENT * BALL_AREA * speed * speed
        drag_acc = scale_vector(scale_vector(velocity, -1.0 / speed), drag_force / BALL_MASS)

        # Magnus effect: curve from spin
        magnus_acc = scale_vector(cross(spin_vector, velocity), MAGNUS_COEFFICIENT)

        # Gravity
        gravity_acc = (0.0, -GRAVITY, 0.0)

        # Total acceleration
        acceleration = add_vector(add_vector(drag_acc, magnus_acc), gravity_acc)

        # Euler integration for position and velocity
        new_velocity = add_vector(velocity, scale_vector(acceleration, time_step))
        displacement = scale_vector(add_vector(velocity, new_velocity), 0.5 * time_step)
        new_position = add_vector(position, displacement)

        segment_length = vector_length(displacement)
        total_distance += segment_length
        max_height = max(max_height, new_position[1])
        path.append(new_position)

        # Check goal plane crossing at x = goal_distance
        if not crossed_goal_plane and position[0] <= goal_distance <= new_position[0]:
            fraction = (goal_distance - position[0]) / (new_position[0] - position[0])
            cross_y = position[1] + (new_position[1] - position[1]) * fraction
            cross_z = position[2] + (new_position[2] - position[2]) * fraction
            if 0.0 <= cross_y <= goal_height and abs(cross_z) <= goal_width / 2.0:
                crossed_goal_plane = True
                goal_info = {
                    "cross_y": cross_y,
                    "cross_z": cross_z,
                    "goal_height": goal_height,
                    "goal_width": goal_width,
                    "distance_to_goal": total_distance,
                }

        if new_position[1] < 0.0:
            break

        position = new_position
        velocity = new_velocity
        last_position = position
        last_velocity = velocity

    horizontal_distance = position[0]
    lateral_curve = position[2]
    result = {
        "max_height": max_height,
        "horizontal_distance": horizontal_distance,
        "total_distance": total_distance,
        "lateral_curve": lateral_curve,
        "goal_scored": crossed_goal_plane,
        "goal_info": goal_info,
        "path": path,
    }
    return result


def format_meters(value):
    return f"{value:.2f} m"


def analyze_free_kick(
    initial_speed=28.0,
    elevation_deg=16.0,
    azimuth_deg=0.0,
    spin_rpm=2500,
    spin_axis=(0.0, -1.0, 0.0),
    goal_distance=11.0,
):
    """Analyze a free kick and print the shot summary."""
    info = simulate_free_kick(
        initial_speed=initial_speed,
        elevation_deg=elevation_deg,
        azimuth_deg=azimuth_deg,
        spin_rpm=spin_rpm,
        spin_axis=spin_axis,
        goal_distance=goal_distance,
    )

    print("Messi-style free-kick analysis")
    print("--------------------------------")
    print(f"Initial speed: {initial_speed:.1f} m/s")
    print(f"Elevation angle: {elevation_deg:.1f} degrees")
    print(f"Spin rate: {spin_rpm:.0f} rpm")
    print(f"Goal distance: {goal_distance:.1f} m")
    print()
    print(f"Max height reached: {format_meters(info['max_height'])}")
    print(f"Horizontal distance traveled: {format_meters(info['horizontal_distance'])}")
    print(f"Distance traveled along the path: {format_meters(info['total_distance'])}")
    print(f"Lateral curve at landing: {format_meters(info['lateral_curve'])}")
    print(f"Goal scored: {'Yes' if info['goal_scored'] else 'No'}")
    if info["goal_scored"]:
        cross_y = info["goal_info"]["cross_y"]
        cross_z = info["goal_info"]["cross_z"]
        print(f"Goal plane height at crossing: {format_meters(cross_y)}")
        print(f"Goal plane lateral offset at crossing: {format_meters(cross_z)}")
        print(f"Path length to goal: {format_meters(info['goal_info']['distance_to_goal'])}")

    return info


def plot_trajectory(path):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed, skipping plot.")
        return

    xs = [p[0] for p in path]
    ys = [p[1] for p in path]
    zs = [p[2] for p in path]

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 2, 1)
    ax.plot(xs, ys, label="vertical profile")
    ax.set_xlabel("Distance toward goal (m)")
    ax.set_ylabel("Height (m)")
    ax.set_title("Ball height vs. distance")
    ax.grid(True)

    ax2 = fig.add_subplot(1, 2, 2)
    ax2.plot(xs, zs, label="curve", color="orange")
    ax2.set_xlabel("Distance toward goal (m)")
    ax2.set_ylabel("Lateral curve (m)")
    ax2.set_title("Ball curve toward goal")
    ax2.grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    result = analyze_free_kick(
        initial_speed=30.0,
        elevation_deg=16.0,
        azimuth_deg=-1.5,
        spin_rpm=2800,
        spin_axis=(0.0, -1.0, 0.0),
        goal_distance=11.0,
    )
    plot_trajectory(result["path"])
