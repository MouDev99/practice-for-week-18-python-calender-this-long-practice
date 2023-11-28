from flask_wtf import FlaskForm
from wtforms.fields import (
    BooleanField, DateField, StringField, SubmitField, TextAreaField, TimeField
)
from wtforms.validators import DataRequired, ValidationError
from datetime import datetime


class AppointmentForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    start_date = DateField("Start date", validators=[DataRequired()])
    start_time = TimeField("Start time", validators=[DataRequired()])
    end_date = DateField("End date", validators=[DataRequired()])
    end_time = TimeField("End time", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    private = BooleanField("Private")
    submit = SubmitField("Create an appointment")


    def get_form_data(self):
        name = self.name.data
        start_datetime = datetime.combine(self.start_date.data, self.start_time.data)
        end_datetime = datetime.combine(self.end_date.data, self.end_time.data)
        description = self.description.data
        private = self.private.data
        return (name, start_datetime, end_datetime, description, private)

    def validate_end_date(form, field):
        start = datetime.combine(form.start_date.data, form.start_time.data)
        end = datetime.combine(form.end_date.data, form.end_time.data)
        if start >= end:
            msg = "End date/time must come after start date/time"
            raise ValidationError(msg)
        if start.date() != end.date():
            msg = "Appointments must be on the same day"
            raise ValidationError(msg)
