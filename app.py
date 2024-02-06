from flask import Flask, request, render_template, redirect, url_for, flash
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

if __name__ == '__main__':
    app.run(debug=True)
