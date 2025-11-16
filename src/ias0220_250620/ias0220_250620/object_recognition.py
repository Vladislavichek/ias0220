import rclpy
import numpy as np
import cv2
from rclpy.node import Node
from sensor_msgs.msg import Image
# from sensor_msgs.msg import CameraInfo
from cv_bridge import CvBridge


class Object_recognition(Node):
    def __init__(self):
        super().__init__('object_recognition')

        self.sub_img = self.create_subscription(
            Image, "/camera1/image_raw", self.img_callback, 10)

        self.pub_proc_img = self.create_publisher(
            Image, "/image_detected", 10)

        # self.pub_cam_info = self.create_publisher(
        #     CameraInfo, "/camera_info", 10)

        # # A variable to show whether the robot is allowed to move or not
        # self.img_cnt = 0
        # self.state = "collection"

        # self.cv_img_arr = []
        self.bridge = CvBridge()
        self.pathOverlay = 0
        self.pathOverlayIsSet = 0
        # self.cam_info = CameraInfo()

        # self.objpoints = []
        # self.imgpoints = []

        # self.rvecs = []
        # self.tvecs = []

        # squareSize = 0.108  # size in meters
        # self.objp = np.zeros((6*7, 3), np.float32)
        # self.objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2) * squareSize

    def img_callback(self, data):
        cvImage = self.bridge.imgmsg_to_cv2(data, "bgr8")

        hsv = cv2.cvtColor(cvImage, cv2.COLOR_BGR2HSV)

        # define range of red color in HSV
        lower_red = np.array([0, 50, 50])
        upper_red = np.array([5, 255, 255])

        # Threshold the HSV image to get only red colors
        self.mask = cv2.inRange(hsv, lower_red, upper_red)

        ret, thresh = cv2.threshold(self.mask, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)

        # cv2.drawContours(mask, contours, -1, (0, 255, 0), 3)

        # Detect edges using Canny
        self.canny_output = cv2.Canny(self.mask, 10, 10 * 2)

        # Approximate contours to polygons + get bounding rects and circles
        contours_poly = [None]*len(contours)
        boundRect = [None]*len(contours)
        centers = [None]*len(contours)
        radius = [None]*len(contours)
        for i, c in enumerate(contours):
            contours_poly[i] = cv2.approxPolyDP(c, 3, True)
            boundRect[i] = cv2.boundingRect(contours_poly[i])
            centers[i], radius[i] = cv2.minEnclosingCircle(contours_poly[i])

        # Assign the first value to the drawing of the detection path
        if (self.pathOverlayIsSet == 0):
            self.pathOverlay = np.zeros((self.canny_output.shape[0],
                                        self.canny_output.shape[1], 3),
                                        dtype=np.uint8)
            self.pathOverlayIsSet = 1

        if len(contours) > 0:

            red = (0, 255, 0)  # Red for drawing
            blue = (255, 0, 0)

            largest_contour_idx = np.argmax([
                cv2.contourArea(c) for c in contours])
            x, y, w, h = boundRect[largest_contour_idx]
            cx, cy = centers[largest_contour_idx]

            # Draw bounding box for the largest contour
            cv2.rectangle(cvImage, (x, y), (x + w, y + h), red, 2)

            cv2.circle(self.pathOverlay, (int(cx), int(cy)), 2, blue, 2)

        px_mask = np.any(self.pathOverlay != 0, axis=2)
        cvImage[px_mask] = self.pathOverlay[px_mask]
        # overlayed = cv2.addWeighted(self.pathOverlay, 1.0, drawing, 1.0, 0)
        # overlayed = cv2.addWeighted(cvImage, 1.0, drawing, 1.0, 0)

        img_msg = self.bridge.cv2_to_imgmsg(cvImage, encoding="bgr8")

        self.pub_proc_img.publish(img_msg)


def main(args=None):
    rclpy.init(args=args)
    sub_node = Object_recognition()
    rclpy.spin(sub_node)

    sub_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
