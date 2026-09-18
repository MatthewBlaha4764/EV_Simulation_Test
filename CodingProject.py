mass = 2000 # mass in kilograms
rollingResistanceCoefficient = 0.01 # rolling resistance coefficient
dragCoefficient = 0.3 # drag coefficient
frontalArea = 2.5 # frontal area in square meters
airDensity = 1.2 # air density in kg/m^3
g = 10 # acceleration due to gravity in m/s^2
tireRadius = 0.4 # tire radius in meters
drivetrainEfficiency = 0.90 # drivetrain efficiency

gearRatio = 9.0 # gear ratio
timeStep = 0.01 # seconds
simulationTime = 120.0 # seconds


def motor_torque(motor_rpm):
	"""Return motor torque in N*m for the given motor speed in rpm."""
	if motor_rpm <= 4000:
		return 250.0
	if motor_rpm <= 10000:
		return 250.0 * 4000.0 / motor_rpm
	return 0.0


def simulate():
	times = []
	speeds = []
	speed = 0.0
	time = 0.0

	while time <= simulationTime:
		wheel_rpm = speed / (2.0 * 3.141592653589793 * tireRadius) * 60.0
		motor_rpm = wheel_rpm * gearRatio
		motor_torque_value = motor_torque(motor_rpm)

		tire_force = (
			motor_torque_value * gearRatio * drivetrainEfficiency / tireRadius
		)
		
		rolling_resistance = rollingResistanceCoefficient * mass * g
		
		aerodynamic_drag = 0.5 * airDensity * dragCoefficient * frontalArea * speed**2
		
		resistance_force = rolling_resistance + aerodynamic_drag
		
		acceleration = (tire_force - resistance_force) / mass

		times.append(time)
		speeds.append(speed)
		speed += acceleration * timeStep
		time += timeStep

	return times, speeds


times, speeds = simulate()

# Pair each recorded time with its speed, keep pairs where speed reaches 20 m/s,
# and return the first matching time. If no speed reaches 20 m/s, use None.
time_to_20 = next(
	(time for time, speed in zip(times, speeds) if speed >= 20.0), None
)
top_speed = max(speeds)

print(f"Gear ratio: {gearRatio}:1")
if time_to_20 is None:
	print("The vehicle does not reach 20 m/s during the simulation.")
else:
	print(f"Time to reach 20 m/s: {time_to_20:.2f} s")
print(f"Top speed reached: {top_speed:.2f} m/s")
print(f"Speed after 1 second: {speeds[100]:.2f} m/s")


# This is entirely done by ai here, I don't really understand how to plot this
# It gives me trouble when I try to run it but I can run it in PowerShell with AI help
import matplotlib.pyplot as plt

plt.plot(times, speeds)
plt.xlabel("Time (s)")
plt.ylabel("Vehicle speed (m/s)")
plt.title(f"Vehicle speed for a {gearRatio}:1 gear ratio")
plt.grid(True)
plt.tight_layout()
plt.show()
