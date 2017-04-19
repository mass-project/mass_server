from mongoengine import StringField, DateTimeField, ReferenceField, EmbeddedDocumentField, ListField

from mass_server.core.utils import TimeFunctions
from mass_server import db
from .user import User


class Comment(db.EmbeddedDocument):
    comment = StringField(max_length=1000, verbose_name='Comment', help_text='Leave a comment', required=True)
    post_date = DateTimeField(default=TimeFunctions.get_timestamp, required=True)
    user = ReferenceField(User, required=True)


class CommentsMixin:
    comments = ListField(EmbeddedDocumentField(Comment))

    def add_comment(self, comment, post_date, user):
        self.comments.append(Comment(comment=comment, post_date=post_date, user=user))
