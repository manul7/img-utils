import os
import cv2
import numpy as np


def shrink_image(image_path, output_path, scale_factor):
    """Shrink an image on both sides by a given percentage.
    :param image_path: the path to the image to shrink
    :param output_path: the path to save the shrunk image
    :param scale_factor: the percentage to shrink the image by
    """
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    # Calculate new width for the left and right sides
    new_width = int(width * (1 - scale_factor))
    # Calculate the starting and ending points for the cropping
    left_start = int(width * scale_factor / 2)
    right_end = left_start + new_width
    
    cropped_image = image[:, left_start:right_end]
    cv2.imwrite(output_path, cropped_image)


def rotate_image(image_path, output_path, angle):
    """Rotate an image by a given angle.
    :param image_path: the path to the image to rotate
    :param output_path: the path to save the rotated image
    :param angle: the angle to rotate the image by
    """
    image = cv2.imread(image_path)
    height, width = image.shape[:2]

    # Compute the rotation center and output size
    center = (width / 2, height / 2)
    output_size = (int(height * np.abs(np.sin(np.radians(angle))) + width * np.abs(np.cos(np.radians(angle)))),
                   int(height * np.abs(np.cos(np.radians(angle))) + width * np.abs(np.sin(np.radians(angle)))))

    # Compute the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)

    # Adjust the translation part of the rotation matrix
    rotation_matrix[0, 2] += output_size[0] / 2 - center[0]
    rotation_matrix[1, 2] += output_size[1] / 2 - center[1]

    # Rotate the image
    rotated_image = cv2.warpAffine(image, rotation_matrix, output_size)

    # Save the rotated image to the output path
    cv2.imwrite(output_path, rotated_image)


def list_dir(path):
    """List all files in a directory tree
    :param path: the root path to list
    :return: a list of paths
    """
    list_dir = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".png"):
                 list_dir.append(os.path.join(root, file))
    return list_dir

if __name__ == '__main__':
    ls = list_dir("dataset")
    
    for image in ls:
        new_filename = image.split("/")[-1].replace(".png", "-r.png")
        rotate_image(image, new_filename, 90)