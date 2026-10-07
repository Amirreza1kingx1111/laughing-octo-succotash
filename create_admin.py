from getpass import getpass

from werkzeug.security import generate_password_hash

from app import app
from database import db
from models import Admin


def main():
    with app.app_context():

        username = input("نام کاربری مدیر: ").strip()

        if not username:
            print("نام کاربری نمی‌تواند خالی باشد.")
            return

        existing = db.session.execute(
            db.select(Admin).where(Admin.username == username)
        ).scalar_one_or_none()

        if existing:
            print("این نام کاربری قبلاً وجود دارد.")
            return

        password = getpass("رمز عبور مدیر: ")
        confirm = getpass("تکرار رمز عبور: ")

        if not password:
            print("رمز عبور نمی‌تواند خالی باشد.")
            return

        if password != confirm:
            print("رمزهای عبور یکسان نیستند.")
            return

        admin = Admin(
            username=username,
            password_hash=generate_password_hash(password)
        )

        db.session.add(admin)
        db.session.commit()

        print()
        print("مدیر با موفقیت ساخته شد.")


if __name__ == "__main__":
    main()
