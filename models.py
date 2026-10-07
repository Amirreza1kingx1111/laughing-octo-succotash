from database import db


class School(db.Model):
    __tablename__ = "schools"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)

    students = db.relationship(
        "Student",
        backref="school",
        lazy=True
    )


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    student_code = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )
    grade = db.Column(db.String(50), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)

    school_id = db.Column(
        db.Integer,
        db.ForeignKey("schools.id"),
        nullable=False
    )


class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )
    password_hash = db.Column(
        db.String(255),
        nullable=False
    )


class Loan(db.Model):
    __tablename__ = "loans"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=True
    )

    book_id = db.Column(
        db.Integer,
        nullable=True
    )

    borrowed_at = db.Column(
        db.DateTime,
        nullable=False
    )

    due_at = db.Column(
        db.DateTime,
        nullable=False
    )

    returned_at = db.Column(
        db.DateTime,
        nullable=True
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="active"
    )

    notes = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False
    )

    student = db.relationship(
        "Student",
        backref=db.backref(
            "loans",
            lazy=True
        )
    )
