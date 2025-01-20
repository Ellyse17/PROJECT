import cv2
import numpy as np

# Open the default camera (usually the first camera, index 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open the video stream!")
    exit()

# Initialize the previous frame variable
prev_gray = None

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Blank frame grabbed!")
        break

    # Flip the frame horizontally (left-right)
    frame = cv2.flip(frame, 1)  # 1 indicates horizontal flip

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Blur the image to reduce noise
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if prev_gray is None:
        prev_gray = gray
        continue

    # Compute the absolute difference between the current and previous frame
    diff = cv2.absdiff(prev_gray, gray)
    # Threshold the difference to get a binary image
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through the contours and draw bounding boxes around detected motion
    for contour in contours:
        if cv2.contourArea(contour) < 500:  # Filter out small contours (noise)
            continue
        
        # Get the bounding rectangle for each contour
        (x, y, w, h) = cv2.boundingRect(contour)
        # Draw a rectangle around the detected motion
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Show the resulting frame
    cv2.imshow("Motion Detection", frame)

    # Update the previous frame for the next iteration
    prev_gray = gray

    # Exit the loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()
