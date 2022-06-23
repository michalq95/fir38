from flask import Flask
from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, StringField, PasswordField, BooleanField, SubmitField, DecimalField
from wtforms.validators import Length, ValidationError, DataRequired, Email, EqualTo
from app.models import User, Client, StatusesEnum#,coerce_for_enum
import email_validator
from markupsafe import escape


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class CreateClientForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    firstName = StringField("FirstName")
    lastName = StringField("LastName")
    nip = StringField("NIP", validators=[Length(max=10)])
    phoneNumber = StringField("PhoneNumber", validators=[DataRequired(),Length(max=12)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField('CreateClient')

    def validate_username(self, name):
        client = Client.query.filter_by(name=name.data).first()
        if client is not None:
            raise ValidationError('Please use a different name.')

    def validate_email(self, email):
        client = Client.query.filter_by(email=email.data).first()
        if client is not None:
            raise ValidationError('Please use a different email address.')



class CreateOrderForm(FlaskForm):
    subject = StringField("subject", validators=[DataRequired()])
    price = DecimalField("price", validators=[DataRequired()])
    description = StringField("Description")
    comment = TextAreaField("Comment", validators=[Length(max=256)])
    status = SelectField("Status", choices= [(e.name, e.value) for e in StatusesEnum]
        #,coerce=[e.name for e in StatusesEnum]
        )
    client = SelectField("Client", choices = Client.query.all())
    submit = SubmitField('CreateClient')


