from flask import Flask

app = Flask(__name__)

UPLOAD_FOLDER = "/home/jerbeson/Documentos/Desenvolvimento/Python/Flask/BuyBazar/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config["SECRET_KEY"] = "nicetofamia"
app.config["ENCRYPT_KEY"] = b'jmsP7JHUzKV6sOYK0jW7hFpGMp-CR3OpZa0mnSygeqY='
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import routes