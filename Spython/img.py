import cv2
camera = cv2.VideoCapture(0)
while True:
    return_value,image = camera.read()
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    cv2.imwrite('img.jpg',image)
    break
camera.release()
cv2.destroyAllWindows()