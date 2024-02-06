from flask import Flask, request, render_template, redirect, url_for, flash, send_file
from qr_genw import genereer_qr_en_afbeelding

app = Flask(__name__)
app.secret_key = 'jouw_geheime_sleutel'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form['action'] == 'Ok':
            password = request.form.get('password')
            if password == "GbW2023":
                print("Wachtwoord correct, omleiden naar menu")
                flash("Geslaagd!", "success")
                return redirect(url_for('menu'))
            else:
                print("Verkeerd wachtwoord")
                flash("Verkeerd wachtwoord.", "error")
                return redirect(url_for('home'))

    return render_template('home.html')

@app.route('/geslaagd')
def geslaagd():
    # Logica na succesvolle wachtwoordcontrole
    return "Geslaagd!"

@app.route('/fout_wachtwoord')
def fout_wachtwoord():
    # Logica na foutieve wachtwoordcontrole
    return "Fout Wachtwoord."

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/qr_genw', methods=['GET', 'POST'])
def qr_genw():
    if request.method == 'POST':
        url = request.form['URL']
        subtekst = request.form['Subtekst']
        afdeling = 'Wijchmaal'  # Voorbeeld, aanpassen naar behoefte
        qr_img_io = genereer_qr_en_afbeelding(url, subtekst, afdeling)
        return send_file(qr_img_io, mimetype='image/png', attachment_filename='qr_code.png')

    return render_template('qr_genw.html')

if __name__ == '__main__':
    app.run(debug=True)
