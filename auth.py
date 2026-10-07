from functools import wraps

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    flash
)
from werkzeug.security import check_password_hash

from database import db
from models import Admin
from forms import LoginForm

from extensions import limiter


auth = Blueprint("auth", __name__, url_prefix="/auth")


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):

        if "admin_id" not in session:
            return redirect(url_for("auth.login"))

        return view(*args, **kwargs)

    return wrapped


@auth.route("/login", methods=["GET", "POST"])
@limiter.limit(
    "5 per minute",
    methods=["POST"]
)
def login():

    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data.strip()
        password = form.password.data

        admin = db.session.execute(
            db.select(Admin).where(
                Admin.username == username
            )
        ).scalar_one_or_none()

        if admin and check_password_hash(
            admin.password_hash,
            password
        ):
            session.clear()

            session["admin_id"] = admin.id
            session["admin_username"] = admin.username

            return redirect(
                url_for("admin.dashboard")
            )

        flash(
            "نام کاربری یا رمز عبور اشتباه است.",
            "error"
        )

    return render_template(
        "login.html",
        form=form
    )


@auth.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("auth.login")
    )
