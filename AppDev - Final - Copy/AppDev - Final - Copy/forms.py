from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, TextAreaField, SubmitField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import InputRequired

class ProductForm(FlaskForm):
    product_name = StringField("Product Name", validators=[InputRequired()])
    product_price = DecimalField("Product Price", validators=[InputRequired()])
    product_weight = StringField("Product Weight/Volume", validators=[InputRequired()])
    product_image = FileField("Product Image", validators=[FileRequired()])
    product_details = TextAreaField("Product Details", validators=[InputRequired()])
    product_category = SelectField("Product Category", validators=[InputRequired()], choices=[("Dry Goods", "Dry Goods"), ("Sauces", "Sauces"), ("Seasoning", "Seasoning")])
    submit = SubmitField("Submit")
