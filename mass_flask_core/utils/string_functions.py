class StringFunctions:
    @staticmethod
    def strip_zero_bytes_from_string(string):
        return string.decode('utf-8').replace('\u0000', '')