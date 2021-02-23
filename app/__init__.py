from flask import Flask


app = Flask(__name__)

app.config["SECRET_KEY"] = "nicetofamia"
app.config["ENCRYPT_KEY"] = b'jmsP7JHUzKV6sOYK0jW7hFpGMp-CR3OpZa0mnSygeqY='


from app import routes