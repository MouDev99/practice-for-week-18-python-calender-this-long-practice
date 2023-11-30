from flask import Blueprint, redirect, render_template, url_for
import os
import psycopg2
from datetime import datetime, timedelta
from .forms import AppointmentForm

bp = Blueprint("main", __name__, url_prefix="/")

CONNECTION_PARAMETERS = {
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASS"),
    "dbname": os.environ.get("DB_NAME"),
    "host": os.environ.get("DB_HOST")
}

@bp.route("/")
def main():
    d = datetime.now()
    return redirect(url_for(".daily", year=d.year, month=d.month, day=d.day))


@bp.route("/<int:year>/<int:month>/<int:day>", methods=["GET","POST"])
def daily(year, month, day):
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
            d = datetime(year, month, day)
            next_day = d + timedelta(days=1)
            query = """
                SELECT id, name, start_datetime, end_datetime
                FROM appointments
                WHERE start_datetime BETWEEN (%s) AND (%s)
                ORDER BY start_datetime;
            """
            curs.execute(query, (d, next_day))
            rows = curs.fetchall()
    return render_template("main.html", rows=rows, form=form)
