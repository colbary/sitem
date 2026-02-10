from flask import Flask, request, send_from_directory, render_template_string
import os, uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Загрузка скриншотов</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial; max-width: 800px; margin: 40px auto; }
        input, textarea, button { width: 100%; margin: 10px 0; padding: 10px; }
        .link { background: #f0f0f0; padding: 10px; word-break: break-all; }
    </style>
</head>
<body>
    <h1>📱 Загрузи скриншот</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="image" accept="image/*" required>
        <textarea name="description" placeholder="Описание (необязательно)" rows="3"></textarea>
        <button type="submit">Загрузить</button>
    </form>
    <p>После загрузки получишь ссылку, которая откроется на телефоне.</p>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    description = request.form.get('description', '')
    
    if file:
        # Генерируем уникальное имя
        filename = f"{uuid.uuid4().hex[:8]}_{file.filename}"
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        
        # Ссылка для просмотра с телефона
        file_url = f"https://{request.host}/uploads/{filename}"
        
        return f'''
            <h2>✅ Загружено!</h2>
            <p><strong>Ссылка для телефона:</strong></p>
            <div class="link">{file_url}</div>
            <p>Отправь эту ссылку на телефон или открой её в браузере.</p>
            <p><strong>Превью:</strong></p>
            <img src="/uploads/{filename}" style="max-width: 300px;">
            <br><br>
            <a href="/">⬅️ Загрузить ещё</a>
        '''
    
    return "Ошибка загрузки"

@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
