import os
import time, random, string
import stego
from werkzeug.exceptions import HTTPException
from flask import Flask, render_template, request, send_file, session, redirect, url_for


def generate_unique_filename(extension):
    timestamp = int(time.time())
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    return f"{timestamp}_{random_string}.{extension}"


app = Flask(__name__, static_url_path='/static')
app.secret_key = 'MY_SECRET_KEY'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt')
def encrypt():
    return render_template('encrypt.html')

@app.route('/decrypt')
def decrypt():
    return render_template('decrypt.html')

@app.route('/injected', methods=['POST'])
def encode():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(url_for('index'))
            
        img_file = request.files['image']
        msg = request.form['message']
        
        if img_file.filename.endswith('.jpg') or img_file.filename.endswith('.jpeg'):
            fname = generate_unique_filename('.jpg')
            img_file.save(fname)
            stego.write_data(fname, msg)

            return send_file(fname, as_attachment=True)
            
           
        else:
            return redirect(url_for('index'))


@app.route('/message', methods=['POST'])
def message_decode():
    if request.method == 'POST':
        try:
            if 'image' not in request.files:
                return redirect(url_for('index'))
            
            img_file = request.files['image']

            if img_file.filename.endswith('.jpg') or img_file.filename.endswith('.jpeg'):
                img_fname = generate_unique_filename('jpg')
                img_file.save(img_fname)
                
                secret_message = stego.read_text(img_fname)
                os.remove(img_fname)

                print(secret_message)
                if secret_message != '':
                    session['secret_message'] = secret_message
                    return redirect(url_for('display_secret'))
                
                else:
                    return redirect(url_for('index'))
        except Exception as e:
            print(f'Exception: {e}')
            return redirect(url_for('index'))
          
@app.route('/display_secret')
def display_secret():
    secret_message = session.get('secret_message')
    if secret_message:
        print(secret_message)
        return f"Hidden Data: {secret_message}"
    else:
        return redirect(url_for('index'))                


@app.errorhandler(Exception)
def handle_error(error):
    code = 500
    if isinstance(error, HTTPException):
        code = error.code
    return f"{code} Error"
    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

