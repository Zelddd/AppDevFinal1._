from wtforms import StringField, SelectField, IntegerField, validators, SubmitField, DateField
from flask_wtf import FlaskForm

class CreateUserForm(FlaskForm):
    email = StringField("Email", [validators.length(min=6, max=35), validators.Email(), validators.DataRequired()])
    state = SelectField("State", [validators.DataRequired()], choices=[('West', 'West'), ('East', 'East'), ('North', 'North'), ('South', 'South'), ('Central', 'Central')])
    postalcode = IntegerField("PostalCode", [validators.DataRequired()])
    contact = IntegerField("Contact", [validators.DataRequired()])
    paymentmethod = SelectField('Choose Payment', choices=[('Visa', 'Visa'), ('PayPal', 'PayPal'), ('Other', 'Other')])
    cardholder = StringField("Cardholder",[validators.length(min=2), validators.DataRequired()])
    cardnumber = IntegerField("Cardnumber", [validators.DataRequired()])
    expiry = DateField('Expiry Date', [validators.DataRequired()])
    cvc = IntegerField("CVC", [validators.DataRequired()])
    submit = SubmitField('Submit')
