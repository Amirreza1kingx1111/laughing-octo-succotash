from flask import Flask, render_template

from config import Config
from database import db
from extensions import limiter
from logging_config import setup_logging

from auth import auth
from routes import admin


app = Flask(__name__)
app.jinja_env.globals["now"] = __import__("datetime").datetime.utcnow
app.config.from_object(Config)

setup_logging(app)

# CSRF
app.config["WTF_CSRF_ENABLED"] = True
app.config["WTF_CSRF_TIME_LIMIT"] = 3600

# Rate limiting
limiter.init_app(app)

db.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(admin)

from models import School, Student, Admin, Loan


@app.errorhandler(404)
def page_not_found(error):
    app.logger.warning(
        "404 Not Found: %s",
        getattr(error, "description", "unknown")
    )
    return render_template("errors/404.html"), 404


@app.errorhandler(403)
def forbidden(error):
    app.logger.warning(
        "403 Forbidden: %s",
        getattr(error, "description", "unknown")
    )
    return render_template("errors/404.html"), 403


@app.errorhandler(429)
def rate_limit_exceeded(error):
    app.logger.warning(
        "429 Rate Limit: %s",
        getattr(error, "description", "unknown")
    )
    return "تعداد درخواست‌ها بیش از حد مجاز است. لطفاً کمی بعد دوباره تلاش کنید.", 429


@app.errorhandler(500)
def internal_server_error(error):
    app.logger.exception("500 Internal Server Error")
    return render_template("errors/500.html"), 500


@app.route("/")
def home():
    return render_template("home.html")


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True
    )
