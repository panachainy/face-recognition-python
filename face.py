import cv2
import sqlite3

# Load the cascade classifier
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Connect to the database
conn = sqlite3.connect('faces.db')
cursor = conn.cursor()

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    _, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Extract the face region
        face_region = frame[y:y+h, x:x+w]

        # Check if the face is already in the database
        cursor.execute("SELECT * FROM faces WHERE face=?", (sqlite3.Binary(face_region),))
        result = cursor.fetchone()
        if result:
            # If the face is in the database, display the name
            name = result[1]
            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        else:
            # If the face is not in the database, ask the user to enter a name
            name = input("Enter name: ")

            # Insert the face and name into the database
            cursor.execute("INSERT INTO faces(face, name) VALUES (?, ?)", (sqlite3.Binary(face_region), name))
            conn.commit()

    # Display the output
    cv2.imshow('frame', frame)

    # Break the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the database connection
conn.close()

# Release the webcam
cap.release()
cv2.destroyAllWindows()
