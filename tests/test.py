import json
from app.main import max_possible_suffix_of_expr


def test_general():
    for id_ in range(1, 21):
        with open(f'tests/test{id_}.json') as input_file:
            dictionary = json.load(input_file)
            expr = dictionary['expr']
            word = dictionary['word']
            result = dictionary['result']
            assert (result == max_possible_suffix_of_expr(expr, word))
