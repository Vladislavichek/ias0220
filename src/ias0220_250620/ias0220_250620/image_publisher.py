import rclpy
import cv2
from ament_index_python.packages import get_package_share_directory
import os
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


class Publish_Images(Node):
    def __init__(self):
        super().__init__('image_publisher')

        self.pub_img = self.create_publisher(
            Image, "/image_raw", 10)

        # A variable to show whether the robot is allowed to move or not
        self.img_cnt = 0

        self.bridge = CvBridge()
        self.image = Image()

        self.imgs_path = os.path.join(get_package_share_directory(
            'ias0220_250620'), "data/images")

        if not os.path.exists(self.imgs_path):
            self.get_logger().error(f"Image path {self.imgs_path} not found!")
            return
        self.imgs_list = os.listdir(self.imgs_path)

        self.move_timer = self.create_timer(0.5, self.img_callback)

    def img_callback(self):
        # self.get_logger().info(f'Published an image nr {self.img_cnt}')

        if (self.img_cnt >= len(self.imgs_list)):
            self.img_cnt = 0
        else:
            img_path = os.path.join(self.imgs_path, self.imgs_list[self.img_cnt])
            cv_img = cv2.imread(img_path)
            self.image = self.bridge.cv2_to_imgmsg(cv_img, encoding='bgr8')

            self.image.header.frame_id = "camera"

            self.pub_img.publish(self.image)
            self.img_cnt += 1


def main(args=None):
    rclpy.init(args=args)
    pub_node = Publish_Images()
    rclpy.spin(pub_node)

    pub_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
