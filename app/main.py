from flask import Flask, Response, render_template, request, send_from_directory, redirect, url_for
from video_stream import VideoStream
from chat import Chat
from deepfake_detection import DeepfakeDetector
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

video_stream = VideoStream()
chat = Chat()
deepfake_detector = DeepfakeDetector()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', chat_history=chat.get_history())

@app.route('/video_feed')
def video_feed():
    return Response(video_stream.generate_frames(deepfake_detector),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'file' not in request.files:
        message = request.form['message']
        if deepfake_detector.is_deepfake(message):
            return "Deepfake detected!"
        chat.broadcast_message(message, 'text')
    else:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            if deepfake_detector.is_deepfake(filepath):
                os.remove(filepath)
                return "Deepfake detected!"
            chat.broadcast_message(filename, 'file')
    return "Message sent!"

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
