# Viam SLAM Setup

These scripts control the robot through [Viam](https://www.viam.com/) instead of ROS 2. Viam was the first approach we used for mapping and navigation, before moving to the ROS 2 Nav2 stack in `../ros2_ws`.

| Script | What it does |
|---|---|
| `get_resources.py` | Connects to the robot and lists every component/service it exposes. Run this first to check the connection and the resource names. |
| `base_square.py` | Spins the base 90° four times (a quick motor test). |
| `imu_tester.py` | Prints linear acceleration and angular velocity from the IMU. |
| `lidar_readings.py` | Grabs one frame from the RPLIDAR and saves it to `lidar_image.jpg`. |
| `localize_slam.py` | Reads the robot's pose from the SLAM map, then sends it to a target pose with the Motion service. |
| `slam-navigation.py` | Sends the robot to a fixed target pose on the SLAM map. |

## 1. Set up the robot (Raspberry Pi)

1. Create a free account at [app.viam.com](https://app.viam.com) and add a new machine.
2. Follow the setup steps shown for the machine to install `viam-server` on the Raspberry Pi. When it connects, the machine shows as **Live** in the app.
3. On the machine's **CONFIGURE** tab, add these components and services. **Use exactly these names**, because the scripts look them up by name:

   | Name | Type | Notes |
   |---|---|---|
   | `viam_base` | Base (`wheeled`) | Uses the left/right motors driven by the Arduino + motor driver |
   | `imu` | Movement sensor | The IMU on the robot |
   | `camera-1` | Camera | The RPLIDAR A1 (install the `rplidar` module from the Viam registry) |
   | `Cartographer` | SLAM service | Install the `cartographer` module from the Viam registry; set `camera-1` as its LiDAR |
   | `builtin` | Motion service | Present by default, so nothing to add |

4. Save the config, then use the **CONTROL** tab to check that the base moves and the LiDAR streams data.

## 2. Set up your computer

You need Python 3.8+ on the computer running the scripts (it can be the Pi itself or a laptop on any network).

```sh
pip install viam-sdk
```

## 3. Add your credentials

On the machine's page in the Viam app, open the **CONNECT** tab and select **API keys**. Copy:

- the **API key**
- the **API key ID**
- the **machine address** (looks like `my-robot-main.abc123.viam.cloud`)

Each script has a `connect()` function with `'x'` placeholders. Replace them with your values:

```python
opts = RobotClient.Options.with_api_key(
    api_key='<API key>',
    api_key_id='<API key ID>'
)
robot = await RobotClient.at_address('<machine address>', opts)
```

> ⚠️ **Do not commit real keys.** Put the `'x'` placeholders back before pushing. Anyone with these keys can drive the robot.

## 4. Run

Start with the connection check, then the sensor tests, then navigation:

```sh
cd "Software Stack/viam-slam"
python get_resources.py      # should list viam_base, imu, camera-1, Cartographer, builtin
python imu_tester.py
python lidar_readings.py
python base_square.py        # the robot will spin in place, so give it space
python localize_slam.py      # needs a map built by the Cartographer service
```

## Known issues

- **Units are millimetres.** Viam poses use mm, so the target in `slam-navigation.py` (`x=1.0, y=2.0`) is only 1–2 mm away and the robot will barely move. Use values like those in `localize_slam.py` (`x=3768.0, y=1694.0`).
- **`localize_slam.py` resource names:** `base.get_resource_name(base)` and `slam.get_resource_name(slam)` should be given the names as strings, i.e. `Base.get_resource_name("viam_base")` and `SLAMClient.get_resource_name("Cartographer")` (as done in `slam-navigation.py`). Otherwise the move request fails with an error.
- **`lidar_readings.py`:** newer versions of `viam-sdk` return a `ViamImage` from `get_image()`, so `len(image)` and `f.write(image)` fail. Use `image.data` instead. For raw LiDAR data, `get_point_cloud()` is usually more useful than an image.
- **`base_square.py`** only spins in place. To drive a real square, add `await base.move_straight(distance=500, velocity=500)` before each spin.
