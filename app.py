from flask import Flask, request, render_template, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    quality = request.form['quality']
    file_id = str(uuid.uuid4())
    filename = f"{file_id}.mp4"

    ydl_opts = {
        'format': quality,
        'outtmpl': filename,
        'quiet': True,
        'merge_output_format': 'mp4',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"<h3>Error:</h3><p>{str(e)}</p>"
    finally:
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == '__main__':
    app.run(debug=True)
