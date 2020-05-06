import cv2
import numpy as np

def segment_characters(path):
    # Preprocess cropped license plate image
    image=cv2.imread(path)
    img_lp=cv2.resize(image, (150, 75))
    img_gray_lp=cv2.cvtColor(img_lp, cv2.COLOR_BGR2GRAY)
    _, img_binary_lp = cv2.threshold(img_gray_lp, 100, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    img_binary_lp = cv2.erode(img_binary_lp, (3, 3))
    img_binary_lp = cv2.dilate(img_binary_lp, (3,3))

    LP_WIDTH = img_binary_lp.shape[0]
    LP_HEIGHT = img_binary_lp.shape[1]

    # Make borders white
    img_binary_lp[0:3,:] = 255
    img_binary_lp[:,0:3] = 255
    img_binary_lp[72:75,:] = 255
    img_binary_lp[:,147:150] = 255

    # Estimations of character contours sizes of cropped license plates
    boundaries_crop = [LP_WIDTH/6,
                       LP_WIDTH/3,
                       LP_HEIGHT/6,
                       2*LP_HEIGHT/3]

    # Estimations of character contour sizes of non-cropped license plates
    boundaries_no_crop = [LP_WIDTH/12,
                          LP_WIDTH/6,
                          LP_HEIGHT/8,
                          LP_HEIGHT/3]

    # Get contours within cropped license plate
    char_contours, char_list = _check_contours(boundaries_crop, img_binary_lp, img_binary_lp, False)

    if len(char_contours) != 7:

        # Check the smaller contours; possibly no plate was detected at all
        char_contours, char_list = _check_contours(boundaries_no_crop, img_binary_lp, img_binary_lp, False)


    if len(char_contours) == 0 :

            # If nothing was found, try inverting the image in case the background is darker than the foreground
            invert_img_lp = np.invert(img_binary_lp)
            char_contours, char_list = _check_contours(boundaries_crop, img_binary_lp, invert_img_lp, False)

    # If we found 7 chars, it is likely to form a license plate
    full_license_plate = []
    if len(char_contours) == 7 :

        full_license_plate = char_list

    return full_license_plate
