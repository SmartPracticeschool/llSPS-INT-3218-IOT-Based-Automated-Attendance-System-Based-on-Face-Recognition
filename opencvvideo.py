import cv2

cap=cv2.VideoCapture(0)

print(cap.isOpened())
rec=cv2.VideoWriter_fourcc(*'XVID')

out=cv2.VideoWriter('output.avi',rec,20.0,(640,480))
while(cap.isOpened()):
    ret,frame=cap.read()

    out.write(frame)

    cv2.imshow("videocapture",frame)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
