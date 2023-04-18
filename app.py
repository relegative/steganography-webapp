import os
from flask import Flask, render_template, request, send_file, session, redirect, url_for
import stego

app = Flask(__name__, static_url_path='/static')

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
            return redirect(url_for('home'))
            
        img_file = request.files['image']
        msg = request.form['message']
        
        if img_file.filename.endswith('.jpg'):
            img_file.save('injected.jpg')
            stego.write_data('injected.jpg', msg)

            return send_file('injected.jpg', as_attachment=True)
        
        # elif img_file.filename.endswith('.png'):
        #     img_file.save('injected.png')
        #     stego.write_data('injected.png', msg)

        #     return send_file('injected.png', as_attachment=True)

        else:

            return redirect(url_for('index'))

@app.route('/message', methods=['POST'])
def message_decode():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(url_for('home'))
        
        img_file = request.files['image']

        if img_file.filename.endswith('.jpg'):
            img_file.save('temp.jpg')
            secret_message = stego.read_text('temp.jpg')
            os.remove('temp.jpg')

            if secret_message != '':
                with open('secret.txt','w') as f:
                    f.write(secret_message)

                return send_file('secret.txt', as_attachment=True)

            else:
                return redirect(url_for('index'))


    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)