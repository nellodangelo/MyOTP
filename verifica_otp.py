from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
import random
import string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'dangelonello@libero.it' and password == '1234':
            # Genera casualmente la OTP
            otp = generate_otp()

            # Invia la OTP all'indirizzo email specificato
            send_otp_email(username, otp)

            # Memorizza la OTP per la verifica successiva
            store_otp(username, otp)

            # Reindirizza l'utente alla pagina di verifica dell'OTP
            return render_template('verify_otp.html')

    return render_template('login2.html')

@app.route('/verify', methods=['POST'])
def verify():
    otp = request.form['otp']
    username = request.form['username']

    # Recupera la OTP memorizzata per l'utente
    stored_otp = get_stored_otp(username)

    # Verifica che la OTP inserita sia uguale a quella memorizzata
    if otp == stored_otp:
        return render_template('access_granted.html')

    error_message = 'Codice OTP non valido. Riprova.'
    return render_template('verify_otp.html', error_message=error_message)

def generate_otp():
    # Genera una OTP casuale di 6 caratteri
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(6))
    return otp

def send_otp_email(email, otp):
    # Implementa qui il codice per inviare l'OTP all'indirizzo email specificato
    # Esempio: utilizzo di una stampa di log per simulare l'invio dell'email
    # Configurazione delle informazioni del server SMTP
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'brighetto93@gmail.com'
    smtp_password = 'bpjstbvadmntbcne'

    # Creazione del messaggio email
    message = MIMEText(f"La tua One Time Password (OTP) è: {otp}")
    message['Subject'] = 'OTP Verification'
    message['From'] = smtp_username
    message['To'] = email

    try:
        # Connessione al server SMTP
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)

            # Invio dell'email
            server.sendmail(smtp_username, email, message.as_string())

        print("Email inviata correttamente.")
        print(f"Email inviata a {email} con codice OTP: {otp}")
    except Exception as e:
        print("Si è verificato un errore durante l'invio dell'email:", str(e))

def store_otp(username, otp):
    # Implementa qui il codice per memorizzare la OTP per l'utente specificato
    # Esempio: memorizzazione nella memoria del server utilizzando un dizionario
    otp_storage[username] = otp

def get_stored_otp(username):
    # Implementa qui il codice per recuperare la OTP memorizzata per l'utente specificato
    # Esempio: recupero dalla memoria del server utilizzando un dizionario
    return otp_storage.get(username)

if __name__ == '__main__':
    # Dizionario per la memorizzazione delle OTP degli utenti
    otp_storage = {}

    app.run(debug=True)