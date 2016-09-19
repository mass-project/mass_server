from flask_wtf import Form
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea
from flask_modular_auth import current_authenticated_entity


class CommentForm(Form):
    comment = StringField('Your comment', widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField()

    def validate_comment(self, field):
        if not current_authenticated_entity.is_authenticated:
            raise ValidationError('You have to login before you can post a comment.')
