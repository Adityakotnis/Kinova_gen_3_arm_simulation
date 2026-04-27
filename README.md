RSS Project - Sensor-Controlled Robotic Arm
A real-time system that uses physical sensors (ESP8266, MPU6050, IR sensor, rotary encoder) to control a simulated 6-DOF robotic arm via ROS 2.
Project Overview
This project creates an interactive robotic arm system where physical sensor inputs trigger emotional states (Happy, Scared, Bored) that control the arm's behavior:

Happy State: Triggered by IR sensor detection, makes the arm wave with adjustable speed based on encoder rotation
Scared State: Triggered by sudden movements (jolt detection), makes the arm recoil defensively
Bored State: Default resting position when no stimuli are detected for 10 sec

System Architecture
The system consists of 5 main components communicating via ROS 2 topics:
ESP8266 Hardware → UDP Bridge → Sensor Parser → State Estimator → Robot Controller → RViz2
Component Flow

ESP8266 (Arduino): Reads sensor data and broadcasts via UDP
UDP Bridge (udp_bridge.py): Receives UDP packets and publishes to /imu_raw
Sensor Parser (sensor_parser.py): Applies moving average filter, publishes to /imu_filtered
State Estimator (state_estimator.py): Determines robot state based on sensor inputs, publishes to /imu_control
Robot Controller (robot_controller.py): Controls joint positions based on state, publishes to joint trajectory controller

Hardware Components

ESP8266: WiFi microcontroller 
MPU6050: 6-axis gyroscope and accelerometer for motion detection
IR Sensor: Infrared proximity sensor (GPIO 16)
Rotary Encoder: Controls happy animation speed (GPIO 14, 12)
Breadboards and jumpers for connections

Software Requirements
On Ubuntu Linux
For more refer Docker file

On Development Machine

Arduino IDE
ESP8266 board support (via Board Manager)
Libraries:

Adafruit_MPU6050
ESP8266WiFi
WiFiUdp



Hardware Setup
Wiring Connections
MPU6050 to ESP8266:

SDA → GPIO 4 (D2)
SCL → GPIO 5 (D1)
VCC → 3.3V
GND → GND

IR Sensor:

OUT → GPIO 16 (D0)
VCC → 3.3V
GND → GND

Rotary Encoder:

CLK → GPIO 14 (D5)
DT → GPIO 12 (D6)
VCC → 3.3V
GND → GND

Software Installation
1. Arduino Setup
bash# Install Arduino IDE from arduino.cc

# Add ESP8266 board support:
# File → Preferences → Additional Board Manager URLs:
http://arduino.esp8266.com/stable/package_esp8266com_index.json

# Tools → Board Manager → Search "ESP8266" → Install

# Install libraries via Library Manager:
# - Adafruit MPU6050
# - Adafruit Unified Sensor (dependency)
2. ROS 2 Workspace Setup
bash# Create workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# Clone or copy the Python nodes
mkdir robot_control
cd robot_control
# Copy: udp_bridge.py, sensor_parser.py, state_estimator.py, robot_controller.py

# Make scripts executable
chmod +x *.py

# Build workspace
cd ~/ros2_ws
colcon build
source install/setup.bash
Configuration
Arduino Code
Edit WiFi credentials in the ESP8266 code:
cppconst char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
Adjustable Parameters
In ESP8266 code:

JOLT_G: Acceleration threshold for scared state (default: 1.1g)
port: UDP port (default: 4242)

In Python nodes:

State durations in state_estimator.py (default: 10 seconds)
Moving average window in sensor_parser.py (default: 5 samples)
Joint angles in robot_controller.py for each emotional pose

Running the Project
1. Upload Arduino Code

Connect ESP8266 via USB
Select board: "Generic ESP8266 Module" or "NodeMCU 1.0"
Upload the code
Open Serial Monitor to verify broadcast IP

### 2. Launch ROS 2 Nodes

**Option 1: Using Launch File (Recommended)**
```bash
# Launch all sensor processing nodes at once
ros2 launch sensor_pipeline pipeline.launch.py
```

**Option 2: Manual Launch (for debugging)**

Open 4 separate terminals and run:
```bash
# Terminal 1: UDP Bridge
ros2 run robot_control udp_bridge.py

# Terminal 2: Sensor Parser
ros2 run robot_control sensor_parser.py

# Terminal 3: State Estimator
ros2 run robot_control state_estimator.py

# Terminal 4: Robot Controller
ros2 run robot_control robot_controller.py
```

**Verify UDP reception (optional):**
```bash
# Test UDP packets are being received on port 4242
nc -ul 4242
```

### 3. Launch Robot Simulation with RViz2
```bash
ros2 launch gen3_bottle_description gen3_with_bottle.launch.py \
  robot_ip:=0.0.0.1 \
  use_fake_hardware:=true \
  launch_rviz:=true
```

This will:
- Load the Gen3 robot with bottle description
- Start fake hardware interface for simulation
- Automatically launch RViz2 for visualization

# Add RobotModel display
# Set Fixed Frame to appropriate link (generally world)
# Set joints topic

Testing & Interaction
Triggering States

Happy State: Wave hand in front of IR sensor

Arm waves back and forth
Rotate encoder clockwise for faster waving (2x speed)
Rotate encoder counter-clockwise for slower waving (0.5x speed)


Scared State: Shake or jolt the ESP8266

Arm recoils into defensive position
Lasts 10 seconds unless another state is triggered


Bored State: Leave sensors untouched

Arm returns to neutral resting position



Monitoring Topics
bash# View raw sensor data
ros2 topic echo /imu_raw

# View filtered sensor data
ros2 topic echo /imu_filtered

# View current state and gain
ros2 topic echo /imu_control

# View joint commands
ros2 topic echo /joint_trajectory_controller/joint_trajectory
What We Implemented
Core Features

Multi-sensor integration: Combined MPU6050, IR sensor, and rotary encoder into unified system
State machine: Three emotional states with smooth transitions
Real-time control: 50Hz sensor sampling with filtered data processing
UDP broadcast communication: Automatic network discovery for flexible deployment
Modular ROS 2 architecture: Separation of concerns across 4 specialized nodes

Technical Highlights

Moving average filter: Reduces sensor noise for stable state detection
Interrupt-driven encoder: Accurate tick counting without polling
Dynamic animation speed: User-adjustable waving speed via encoder
State persistence: 10-second state duration prevents rapid switching
Graceful transitions: Smooth joint movements between emotional poses

Robot Behaviors

Happy: Joint 1 oscillates ±90° at variable speed while joints 4 and 6 bend
Scared: Quick recoil to protective position with raised joints
Bored: Relaxed neutral pose with minimal joint angles

Troubleshooting
ESP8266 not connecting:

Verify WiFi credentials
Check that router allows broadcast packets
Ensure ESP8266 is on same subnet as Linux machine

No data in ROS 2:

Verify UDP port 4242 is not blocked by firewall
Check broadcast IP calculation in Serial Monitor
Confirm all nodes are running: ros2 node list

Arm not moving:

Ensure robot URDF and controller are properly configured
Check joint trajectory topic is being published: ros2 topic hz /joint_trajectory_controller/joint_trajectory
Verify joint names match your robot description


Future Enhancements

Add temperature-based behavior (using MPU6050 temp sensor)
Implement gesture recognition using gyroscope data
Add voice feedback or LED indicators
Create custom emotional poses
Multi-robot coordination

Team & Credits
RSS Project Team 14 - Winter Semester 2025/26
