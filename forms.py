from flask_wtf import FlaskForm
from wtforms import (
    PasswordField,
    StringField,
    SubmitField,
    SelectField
)
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField(
        "نام کاربری",
        validators=[
            DataRequired(message="نام کاربری را وارد کنید."),
            Length(max=100, message="نام کاربری بیش از حد طولانی است.")
        ]
    )

    password = PasswordField(
        "رمز عبور",
        validators=[
            DataRequired(message="رمز عبور را وارد کنید."),
            Length(max=256, message="رمز عبور بیش از حد طولانی است.")
        ]
    )

    submit = SubmitField("ورود به سامانه")


class ExcelImportForm(FlaskForm):
    submit = SubmitField("بررسی و نمایش پیش‌نمایش")


class LoanForm(FlaskForm):
    student_id = StringField(
        "شناسه عضو",
        validators=[
            DataRequired(message="شناسه عضو را وارد کنید."),
            Length(max=50, message="شناسه عضو بیش از حد طولانی است.")
        ]
    )

    book_id = StringField(
        "شناسه کتاب",
        validators=[
            DataRequired(message="شناسه کتاب را وارد کنید."),
            Length(max=100, message="شناسه کتاب بیش از حد طولانی است.")
        ]
    )

    due_date = StringField(
        "تاریخ بازگشت",
        validators=[
            DataRequired(message="تاریخ بازگشت را وارد کنید."),
            Length(max=30, message="تاریخ بازگشت معتبر نیست.")
        ]
    )

    notes = StringField(
        "توضیحات",
        validators=[
            Length(max=500, message="توضیحات بیش از حد طولانی است.")
        ]
    )

    submit = SubmitField("ثبت امانت")


class StudentForm(FlaskForm):
    first_name = StringField(
        "نام",
        validators=[
            DataRequired(message="نام را وارد کنید."),
            Length(max=100, message="نام بیش از حد طولانی است.")
        ]
    )

    last_name = StringField(
        "نام خانوادگی",
        validators=[
            DataRequired(message="نام خانوادگی را وارد کنید."),
            Length(max=100, message="نام خانوادگی بیش از حد طولانی است.")
        ]
    )

    student_code = StringField(
        "کد دانش‌آموزی",
        validators=[
            DataRequired(message="کد دانش‌آموزی را وارد کنید."),
            Length(max=50, message="کد دانش‌آموزی بیش از حد طولانی است.")
        ]
    )

    grade = StringField(
        "پایه",
        validators=[
            DataRequired(message="پایه را وارد کنید."),
            Length(max=50, message="پایه بیش از حد طولانی است.")
        ]
    )

    class_name = StringField(
        "کلاس",
        validators=[
            DataRequired(message="کلاس را وارد کنید."),
            Length(max=50, message="نام کلاس بیش از حد طولانی است.")
        ]
    )

    school_id = SelectField(
        "مدرسه",
        coerce=int,
        validators=[
            DataRequired(message="مدرسه را انتخاب کنید.")
        ]
    )

    submit = SubmitField("ثبت عضو")


class SchoolForm(FlaskForm):
    name = StringField(
        "نام مدرسه",
        validators=[
            DataRequired(message="نام مدرسه را وارد کنید."),
            Length(max=200, message="نام مدرسه بیش از حد طولانی است.")
        ]
    )

    code = StringField(
        "کد مدرسه",
        validators=[
            DataRequired(message="کد مدرسه را وارد کنید."),
            Length(max=50, message="کد مدرسه بیش از حد طولانی است.")
        ]
    )

    submit = SubmitField("ثبت مدرسه")
