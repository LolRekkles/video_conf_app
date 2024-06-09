import cv2

class VideoStream:
    def __init__(self):
        # Initialize the video capture with the default camera (usually the laptop camera)
        self.cap = cv2.VideoCapture(0)

    def __del__(self):
        # Release the video capture when the object is deleted
        self.cap.release()

    def generate_frames(self, deepfake_detector):
        while True:
            # Read a frame from the camera
            success, frame = self.cap.read()
            if not success:
                break
            else:
                # Here you can pass the frame to your deepfake detection model
                # For now, we are skipping this part and directly converting the frame
                # You can integrate your deepfake detection logic here

                # Encode the frame in JPEG format
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()

                # Yield the frame in multipart format for the streaming
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
