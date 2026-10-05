import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QPushButton, QLabel
from rclpy.qos import QoSProfile

class DeliveryRobotGUI(Node):

    def __init__(self):
        super().__init__('delivery_robot_gui')

        # Create a publisher for the goal pose
        self.publisher_ = self.create_publisher(PoseStamped, 'move_base_simple/goal', QoSProfile(depth=10))

        # Set up the GUI components
        self.app = QApplication([])
        self.window = QWidget()
        self.layout = QVBoxLayout()
        
        # Label to display current action
        self.label = QLabel("Select a location for the robot to navigate to:")
        self.layout.addWidget(self.label)

        # Dropdown menu with locations
        self.dropdown = QComboBox()
        self.dropdown.addItem("Kitchen")
        self.dropdown.addItem("Drawing Room")
        self.dropdown.addItem("Bedroom")
        self.dropdown.addItem("Office")
        self.layout.addWidget(self.dropdown)

        # Button to trigger navigation
        self.navigate_button = QPushButton("Navigate")
        self.navigate_button.clicked.connect(self.navigate)
        self.layout.addWidget(self.navigate_button)

        # Set the layout and show the window
        self.window.setLayout(self.layout)
        self.window.setWindowTitle("Autonomous Delivery Robot")
        self.window.show()

    def get_goal_coordinates(self, location):
        """
        This method returns the coordinates for the given location based on the SLAM map.
        Replace these coordinates with the actual ones from your SLAM-generated map.
        """
        coordinates = {
            'Kitchen': (1.0, 2.0),  # Replace with actual SLAM map coordinates for Kitchen
            'Drawing Room': (3.0, -1.0),  # Replace with actual SLAM map coordinates for Drawing Room
            'Bedroom': (-2.0, 4.0),  # Replace with actual SLAM map coordinates for Bedroom
            'Office': (0.0, 0.0)  # Replace with actual SLAM map coordinates for Office
        }
        return coordinates.get(location, (0.0, 0.0))

    def navigate(self):
        location = self.dropdown.currentText()
        goal = PoseStamped()

        # Set the frame_id to 'map' (SLAM map frame)
        goal.header.frame_id = 'map'

        # Get the coordinates for the selected location
        goal.pose.position.x, goal.pose.position.y = self.get_goal_coordinates(location)

        # Set the orientation (assuming the robot faces the positive x-axis)
        goal.pose.orientation.w = 1.0

        # Publish the goal pose to the navigation stack (move_base)
        self.publisher_.publish(goal)

        self.get_logger().info(f'Navigating to {location} at coordinates: ({goal.pose.position.x}, {goal.pose.position.y})')

    def run(self):
        """
        Start the PyQt5 application.
        """
        self.app.exec_()


def main(args=None):
    rclpy.init(args=args)

    # Create the DeliveryRobotGUI object
    gui = DeliveryRobotGUI()

    # Start the GUI application
    gui.run()

    # Clean up and shutdown when the application is closed
    rclpy.shutdown()


if __name__ == '__main__':
    main()

