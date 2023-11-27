from flask import Blueprint, redirect, render_template
import os
import psycopg2
from .forms import AppointmentForm

bp = Blueprint("main", __name__, url_prefix="/")

CONNECTION_PARAMETERS = {
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASS"),
    "dbname": os.environ.get("DB_NAME"),
    "host": os.environ.get("DB_HOST")
}

@bp.route("/", methods=["GET", "POST"])
def main():
    form = AppointmentForm()

    if form.validate_on_submit():
        data = form.get_form_data()
        with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
           with conn.cursor() as curs:
               query = """
                  INSERT INTO appointments (name, start_datetime,
                  end_datetime, description,private)
                  VALUES (%s, %s, %s, %s, %s)
               """
               curs.execute(query, data)
        return redirect("/")

    with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
        with conn.cursor() as curs:
            query = """
                SELECT id, name, start_datetime, end_datetime
                FROM appointments
                ORDER BY start_datetime;
            """
            curs.execute(query)
            rows = curs.fetchall()
    return render_template("main.html", rows=rows, form=form)
