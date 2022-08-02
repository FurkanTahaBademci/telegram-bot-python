import cv2

def camera_shot():
    
    camera = cv2.VideoCapture(0)
    return_value,image = camera.read()
    image = cv2.flip(image,1)
    cv2.imwrite('output/camera.jpg',image)
    camera.release()
    cv2.destroyAllWindows()
