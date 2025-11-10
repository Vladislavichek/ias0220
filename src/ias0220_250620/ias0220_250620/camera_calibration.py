import rclpy
import numpy as np
import cv2
from rclpy.node import Node
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
from cv_bridge import CvBridge, CvBridgeError


class Publish_Images(Node):
    def __init__(self):
        super().__init__('camera_calibration')

        self.sub_img = self.create_subscription(
            Image, "/image_raw", self.img_callback, 10)

        self.pub_proc_img = self.create_publisher(
            Image, "/image_processed", 10)

        self.pub_cam_info = self.create_publisher(
            CameraInfo, "/camera_info", 10)

        # A variable to show whether the robot is allowed to move or not
        self.img_cnt = 0
        self.state = "collection"

        self.cv_img_arr = []
        self.bridge = CvBridge()
        self.cam_info = CameraInfo()

        self.objpoints = []
        self.imgpoints = []

        self.rvecs = []
        self.tvecs = []

        squareSize = 0.108  # size in meters
        self.objp = np.zeros((6*7, 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2) * squareSize

    def img_callback(self, data):
        if (self.state == "collection"):
            try:
                cv_img = self.bridge.imgmsg_to_cv2(data, "bgr8")
            except CvBridgeError as e:
                print(e)
                return
                # Maybe it would be better to save the position of the failed
                # picture to later try to load this picture again, but doing
                # this just to avoid any errors, not fix them

            # print(f'The image: {self.cv_img_arr[self.img_cnt]}')

            # termination criteria (same as in calibration)
            criteria = (
                cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

            gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

            # Try to find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (7, 6), None)

            if ret is True:
                # Refine corners
                corners2 = cv2.cornerSubPix(
                    gray, corners, (11, 11), (-1, -1), criteria)

                # Save object points and image points
                self.objpoints.append(self.objp)
                self.imgpoints.append(corners2)
                self.cv_img_arr.append(cv_img)
                self.img_cnt += 1

                # Draw and visualize
                vis_img = cv2.drawChessboardCorners(
                    cv_img.copy(), (7, 6), corners2, ret)
                img_msg = self.bridge.cv2_to_imgmsg(vis_img, encoding="bgr8")
                self.pub_proc_img.publish(img_msg)

                self.get_logger().info(
                    f"Collected {self.img_cnt}/37 valid chessboard images")

            if self.img_cnt >= 37:
                self.state = "calibration"

        elif self.state == "calibration":
            # Use the last image to get image size
            gray = cv2.cvtColor(self.cv_img_arr[-1], cv2.COLOR_BGR2GRAY)

            # Calibrate camera
            ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(
                self.objpoints, self.imgpoints, gray.shape[::-1], None, None)

            # Compute reprojection error
            total_error = 0
            for i in range(len(self.objpoints)):
                imgpointsKnown, _ = cv2.projectPoints(
                    self.objpoints[i], self.rvecs[i], self.tvecs[i],
                    self.mtx, self.dist)
                error = cv2.norm(self.imgpoints[i], imgpointsKnown,
                                 cv2.NORM_L2) / len(imgpointsKnown)
                total_error += error

            mean_error = total_error / len(self.objpoints)
            self.get_logger().info(
                f"Calibration done. RMS error (OpenCV): {ret:.6f}")
            self.get_logger().info(
                f"Mean reprojection error (manual): {mean_error:.6f}")

            # Switch to publishing CameraInfo
            self.state = "publishing"

        elif (self.state == "publishing"):
            CI = self.cam_info
            CI.header = data.header
            CI.height = data.height
            CI.width = data.width
            CI.distortion_model = "plumb_bob"
            CI.d = self.dist.flatten().tolist()

            CI.k = self.mtx.flatten().tolist()

            CI.r = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]

            P = np.hstack((self.mtx, np.zeros((3, 1))))
            CI.p = P.flatten().astype(float).tolist()

            self.pub_cam_info.publish(CI)


def main(args=None):
    rclpy.init(args=args)
    sub_node = Publish_Images()
    rclpy.spin(sub_node)

    sub_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
