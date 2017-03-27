from pyparsing import infixNotation, opAssoc, Keyword, Regex, ParseException


class TagParser:

    MAX_TAG_LENGTH = 160

    def __init__(self, tag_list):
        self.tag_list = tag_list
        self._init_parser()

    def _bool_op(self, t):
        tag = t[0]
        if tag in self.tag_list:
            return True
        else:
            return False

    def _bool_and(self, t):
        arg1 = t[0][0]
        arg2 = t[0][2]
        return arg1 & arg2

    def _bool_or(self, t):
        arg1 = t[0][0]
        arg2 = t[0][2]
        return arg1 | arg2

    def _bool_not(self, t):
        arg = t[0][1]
        return not arg

    def _init_parser(self):
        TRUE = Keyword('True')
        FALSE = Keyword('False')
        boolOperand = TRUE | FALSE | Regex(r'[a-zA-Z0-9:\-\/]+')
        boolOperand.setParseAction(self._bool_op)

        self._parse_expr = infixNotation(
            boolOperand,
            [
                ('not', 1, opAssoc.RIGHT, self._bool_not),
                ('and', 2, opAssoc.LEFT,  self._bool_and),
                ('or',  2, opAssoc.LEFT,  self._bool_or),
            ])

    def parse_string(self, string):
        if string == '':
            return True
        try:
            return self._parse_expr.parseString(string)[0]
        except ParseException:
            return False
