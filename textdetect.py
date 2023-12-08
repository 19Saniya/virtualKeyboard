import cv2
import pytesseract

# Initialize the webcam
cap = cv2.VideoCapture(0)  # 0 represents the default camera, you can change it to another camera if needed

# Initialize Tesseract OCR (make sure you have Tesseract installed)
pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'  # Replace with your Tesseract path

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to grayscale for better text recognition
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply some preprocessing (you can adjust the parameters as needed)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Perform text detection using Tesseract
    text = pytesseract.image_to_string(gray)

    # Draw the detected text on the frame
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame
    cv2.imshow('Text Detection', frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit the loop
        break

cap.release()
cv2.destroyAllWindows()
