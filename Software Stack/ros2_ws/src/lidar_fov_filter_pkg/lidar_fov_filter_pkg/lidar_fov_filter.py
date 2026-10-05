import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math

class LidarFOVFilter(Node):
    def __init__(self):
        super().__init__('lidar_fov_filter')

        # Parameters: adjust as needed
        self.declare_parameter('input_topic', '/scan')
        self.declare_parameter('output_topic', '/filtered_scan')
        self.declare_parameter('min_angle_deg', -90.0)
        self.declare_parameter('max_angle_deg', 90.0)

        self.input_topic = self.get_parameter('input_topic').get_parameter_value().string_value
        self.output_topic = self.get_parameter('output_topic').get_parameter_value().string_value
        self.min_angle = math.radians(self.get_parameter('min_angle_deg').get_parameter_value().double_value)
        self.max_angle = math.radians(self.get_parameter('max_angle_deg').get_parameter_value().double_value)

        self.publisher_ = self.create_publisher(LaserScan, self.output_topic, 10)
        self.subscription = self.create_subscription(
            LaserScan,
            self.input_topic,
            self.listener_callback,
            10
        )
        self.get_logger().info(f'Lidar FOV Filter running. Subscribed to {self.input_topic}, publishing to {self.output_topic}')
        self.get_logger().info(f'Filtering scan between {math.degrees(self.min_angle)}° and {math.degrees(self.max_angle)}°')

    def listener_callback(self, msg: LaserScan):
        angle_min = msg.angle_min
        angle_increment = msg.angle_increment

        # Indices for the range limits
        start_idx = int((self.min_angle - angle_min) / angle_increment)
        end_idx = int((self.max_angle - angle_min) / angle_increment)

        # Clamp to valid range
        start_idx = max(start_idx, 0)
        end_idx = min(end_idx, len(msg.ranges) - 1)

        # Create filtered LaserScan message
        filtered_msg = LaserScan()
        filtered_msg.header = msg.header
        filtered_msg.angle_min = angle_min + start_idx * angle_increment
        filtered_msg.angle_max = angle_min + end_idx * angle_increment
        filtered_msg.angle_increment = angle_increment
        filtered_msg.time_increment = msg.time_increment
        filtered_msg.scan_time = msg.scan_time
        filtered_msg.range_min = msg.range_min
        filtered_msg.range_max = msg.range_max
        filtered_msg.ranges = msg.ranges[start_idx:end_idx]
        filtered_msg.intensities = msg.intensities[start_idx:end_idx]

        self.publisher_.publish(filtered_msg)

def main(args=None):
    rclpy.init(args=args)
    node = LidarFOVFilter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
