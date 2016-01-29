from mongoengine import signals
from .dispatch_request import update_dispatch_request_for_new_sample


def connect_signals():
    signals.post_save.connect(update_dispatch_request_for_new_sample)
