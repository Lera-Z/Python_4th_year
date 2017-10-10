from unittest import *


class MyExceptionEmpty(Exception):
    def __init__(self, message):
        self.message = message


class MyExceptionInvalidInput(Exception):
    def __init__(self, message):
        self.message = message


def poly_hash(s, x=31, p=997):
    h = 0
    for j in range(len(s)-1, -1, -1):
        h = (h * x + ord(s[j]) + p) % p
    return h


def search_rabin2(text, *args, x=31, p=997):
    indices = []

    if args == ():
        raise MyExceptionEmpty('An empty substring to search')

    for pat in args:
        if not isinstance(pat, str):
            raise MyExceptionInvalidInput('A non-string object was given')

        ind_for_pattern = []

        if len(text) < len(pat):
            indices.append('-')

    # precompute hashes
        precomputed = [0] * (len(text) - len(pat) + 1)
        precomputed[-1] = poly_hash(text[-len(pat):], x, p)

        factor = 1
        for i in range(len(pat)):
            factor = (factor * x + p) % p

        for i in range(len(text) - len(pat) - 1, -1, -1):
            precomputed[i] = (precomputed[i + 1] * x + ord(text[i]) - factor * ord(text[i + len(pat)]) + p) % p

        pattern_hash = poly_hash(pat, x, p)
        for i in range(len(precomputed)):
            if precomputed[i] == pattern_hash:
                if text[i: i + len(pat)] == pat:
                    ind_for_pattern.append(i)

        indices.append(ind_for_pattern)

    return indices


class TestCase(TestCase):
    def setUp(self):
        pass

    def test_for_valid_input(self):
        try:
            f = search_rabin2('text', 'e', 't', 42)

        except MyExceptionInvalidInput:
            print('Arguments contain instance(s) of non-string object(s)')

    def test_for_empty_input(self):
        try:
            f = search_rabin2('text')
        except MyExceptionEmpty:
            print('No substring provided')

    def test_check_for_correct_output(self):
        self.assertEqual(search_rabin2('This is a text.', 'text', 'lalala', 'is'), [[10],[],[2, 5]])


# case = TestCase()
# suite = TestLoader().loadTestsFromModule(case)
# TextTestRunner().run(suite)

# print(search_rabin2('sometext','text'))

# Оценка сложности: O(|T|+ n1|P1| + n2|P2| ... +ni|Pi|), где 1, 2 ... i - индексы, |T| длина текста, |Pi| - длина паттерна,
# ni - кол-во вхождений паттерна Pi