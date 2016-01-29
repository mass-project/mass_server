import hashlib
import ssdeep
from math import log
from collections import Counter
import sys
import logging

logger = logging.getLogger('mass_core')


class HashFunctions:
    @staticmethod
    def _calculate_hash_value(hash_fn, file):
        hash_fn.update(file.read())
        file.stream.seek(0)
        return hash_fn.hexdigest().lower()

    @staticmethod
    def md5_hash(file):
        hash_fn = hashlib.md5()
        return HashFunctions._calculate_hash_value(hash_fn, file)

    @staticmethod
    def sha1_hash(file):
        hash_fn = hashlib.sha1()
        return HashFunctions._calculate_hash_value(hash_fn, file)

    @staticmethod
    def sha256_hash(file):
        hash_fn = hashlib.sha256()
        return HashFunctions._calculate_hash_value(hash_fn, file)

    @staticmethod
    def sha512_hash(file):
        hash_fn = hashlib.sha512()
        return HashFunctions._calculate_hash_value(hash_fn, file)

    @staticmethod
    def ssdeep_hash(file):
        hash_fn = ssdeep.Hash()
        hash_fn.update(file.read())
        file.stream.seek(0)
        ret_val = hash_fn.digest()
        return ret_val

    @staticmethod
    def shannon_entropy(file):
        data = file.read()
        file.stream.seek(0)
        byte_count = len(data)
        if HashFunctions._is_python3_or_greater():
            probabilities = (count / byte_count for count in Counter(data).values())
        else:
            probabilities = (float(count) / float(byte_count) for count in Counter(data).values())

        entropy = 0
        for prob in probabilities:
            entropy += prob * log(prob, 2)

        return -entropy
        # return -sum(p * log(p, 2) for p in probabilities)

    @staticmethod
    def get_hash_values_dictionary(file):
        return {
            'md5sum': HashFunctions.md5_hash(file),
            'sha1sum': HashFunctions.sha1_hash(file),
            'sha256sum': HashFunctions.sha256_hash(file),
            'sha512sum': HashFunctions.sha512_hash(file),
            'ssdeep_hash': HashFunctions.ssdeep_hash(file),
            'shannon_entropy': HashFunctions.shannon_entropy(file)
        }

    @staticmethod
    def _is_python3_or_greater():
        if sys.version_info[0] < 3:
            return False
        return True
