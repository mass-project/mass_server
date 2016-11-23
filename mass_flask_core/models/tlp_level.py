from mongoengine import IntField


class TLPLevelField(IntField):
    TLP_LEVEL_WHITE = 0  # Access without login
    TLP_LEVEL_GREEN = 1  # Access with login
    TLP_LEVEL_AMBER = 2  # Access only for especially authorized users of same group
    TLP_LEVEL_RED = 3    # Access only for explicitly mentioned users/groups

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = [
            TLPLevelField.TLP_LEVEL_WHITE,
            TLPLevelField.TLP_LEVEL_GREEN,
            TLPLevelField.TLP_LEVEL_AMBER,
            TLPLevelField.TLP_LEVEL_RED
        ]
        super(TLPLevelField, self).__init__(*args, **kwargs)
