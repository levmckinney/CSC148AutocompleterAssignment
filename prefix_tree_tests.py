from prefix_tree import SimplePrefixTree
from timeit import timeit
import pytest
import matplotlib.pyplot as plt
import random as r
import string as s

def test_get_leafs_greedy():
    spt = SimplePrefixTree("sum")
    spt.insert('hello', 80, ['h', 'e', 'l', 'l', 'o'])
    spt.insert('help', 10, ['h', 'e', 'l', 'p'])
    spt.insert('hell', 20, ['h', 'e', 'l', 'l'])
    spt.insert('he', 109, ['h', 'e'])
    spt.insert('heart', 50, ['h', 'e', 'a', 'r', 't'])
    spt.insert('heal', 45, ['h', 'e', 'a', 'l'])
    spt.insert('heap', 46, ['h', 'e', 'a', 'p'])
    spt.insert('heat', 47, ['h', 'e', 'a', 't'])
    assert spt._get_leaves_greedy(None) == [('he', 109), ('hello', 80),
                                            ('heart', 50), ('heat', 47),
                                            ('heap', 46), ('heal', 45),
                                            ('hell', 20), ('help', 10)]
    assert spt._get_leaves_greedy(8) == [('he', 109), ('hello', 80),
                                         ('heart', 50), ('heat', 47),
                                         ('heap', 46), ('heal', 45),
                                         ('hell', 20), ('help', 10)]
    assert spt._get_leaves_greedy(3) == [('heart', 50), ('heat', 47),
                                         ('heap', 46)]
    assert spt.subtrees[0].subtrees[0].subtrees[1]._get_leaves_greedy(None) == \
           [('hello', 80), ('hell', 20), ('help', 10)]

    print (random_string(123))


def test_autocomplete() -> None:
    spt = SimplePrefixTree("sum")
    spt.insert('hello', 80, ['h', 'e', 'l', 'l', 'o'])
    spt.insert('help', 10, ['h', 'e', 'l', 'p'])
    spt.insert('hell', 20, ['h', 'e', 'l', 'l'])
    spt.insert('he', 109, ['h', 'e'])
    spt.insert('heart', 50, ['h', 'e', 'a', 'r', 't'])
    spt.insert('heal', 45, ['h', 'e', 'a', 'l'])
    spt.insert('heap', 46, ['h', 'e', 'a', 'p'])
    spt.insert('heat', 47, ['h', 'e', 'a', 't'])
    spt.insert('all', 100, ['a', 'l', 'l'])
    assert spt.autocomplete([]) == [('he', 109), ('all', 100), ('hello', 80),
                                    ('heart', 50), ('heat', 47), ('heap', 46),
                                    ('heal', 45), ('hell', 20), ('help', 10)]
    assert spt.autocomplete(['h', 'e']) == [('he', 109), ('hello', 80),
                                            ('heart', 50), ('heat', 47),
                                            ('heap', 46), ('heal', 45),
                                            ('hell', 20), ('help', 10)]
    assert spt.autocomplete(['h', 'e', 'a']) == [('heart', 50), ('heat', 47),
                                                 ('heap', 46), ('heal', 45)]
    assert spt.autocomplete(['n', 'o', 'n', 'e']) == []

def random_string(N:int):
    ''.join(r.choices(s.ascii_uppercase + s.digits, k=N))


if __name__ == '__main__':
    print (random_string(123))
    pytest.main(['prefix_tree_tests.py', 'v'])

    test_autocomplete()

