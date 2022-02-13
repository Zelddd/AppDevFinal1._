from wtforms import Form, StringField, PasswordField, HiddenField, SubmitField, validators

class SignUpForm(Form):
  username  = StringField('Username', [validators.Length(min=4, max=25), validators.InputRequired()])
  password  = PasswordField('Password', [validators.Length(min=4, max=25), validators.InputRequired()])
  Cpassword = PasswordField('Confirm Password', [validators.Length(min=4, max=25), validators.InputRequired(), validators.EqualTo('password', message='Passwords must match')])
  email     = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email(), validators.InputRequired()])
  location  = StringField('Shipping Address', [validators.Length(min=6, max=60), validators.InputRequired()])
  submit    = SubmitField('Sign Up', [validators.InputRequired()])

class LoginForm(Form):
  login_name = StringField('Username', [validators.Length(min=4, max=25), validators.InputRequired()])
  login_pass = PasswordField('Password', [validators.Length(min=6, max=20), validators.InputRequired()])
  login_submit = SubmitField('Login', [validators.InputRequired()])

class ProfileForm(Form):
  profile_name      = StringField('Username', [validators.Length(min=4, max=25), validators.Optional()])
  profile_pass      = PasswordField('New Password', [validators.Length(min=4, max=25), validators.Optional()])
  profile_Cpass     = PasswordField('Confirm Password', [validators.Length(min=4, max=25), validators.Optional(), validators.EqualTo('profile_pass', message='Passwords must match')])
  profile_email     = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email(), validators.Optional()])
  profile_location  = StringField('Shipping Address', [validators.Length(min=6, max=60), validators.Optional()])
  profile_submit    = SubmitField('Update Profile', [validators.InputRequired()])

class LogoutForm(Form):
  logout_hidden     = HiddenField('')
  logout_submit     = SubmitField('Logout', [validators.InputRequired()])