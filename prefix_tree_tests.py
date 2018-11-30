from prefix_tree import SimplePrefixTree, CompressedPrefixTree
from timeit import timeit
import pytest
import matplotlib.pyplot as plt
from hypothesis import given
from hypothesis.strategies import integers, characters, lists, tuples
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

def test_cpt_insert() -> None:
    cpt = CompressedPrefixTree('sum')
    cpt.insert('help', 12, ['h', 'e', 'l', 'p'])
    cpt.insert('hello', 2, ['h', 'e', 'l', 'l', 'o'])
    cpt.insert('he man', 23, ['h', 'e', ' ', 'm', 'a', 'n'])
    cpt.insert('hello', 12, ['h', 'e', 'l', 'l', 'o'])
    assert cpt.weight == 49
    assert cpt.subtrees[0].weight == 49
    assert cpt.subtrees[0].subtrees[0].weight == 26
    assert cpt.subtrees[0].subtrees[0].subtrees[0].weight == 14
    assert cpt.subtrees[0].subtrees[0].subtrees[0].subtrees[0].weight == 14
    assert cpt.subtrees[0].subtrees[0].subtrees[1].weight == 12
    assert cpt.subtrees[0].subtrees[0].subtrees[1].subtrees[0].weight == 12
    assert cpt.subtrees[0].subtrees[1].weight == 23
    assert cpt.subtrees[0].subtrees[1].subtrees[0].weight == 23
    assert cpt.__len__() == 3
    assert cpt.subtrees[0].__len__() == 3
    assert cpt.subtrees[0].subtrees[0].__len__() == 2
    assert cpt.subtrees[0].subtrees[0].subtrees[0].__len__() == 1
    assert cpt.subtrees[0].subtrees[0].subtrees[0].subtrees[0].__len__() == 1
    assert cpt.subtrees[0].subtrees[0].subtrees[1].__len__() == 1
    assert cpt.subtrees[0].subtrees[0].subtrees[1].subtrees[0].__len__() == 1
    assert cpt.subtrees[0].subtrees[1].__len__() == 1
    assert cpt.subtrees[0].subtrees[1].subtrees[0].__len__() == 1

def test_cpt_remove() -> None:
    cpt = CompressedPrefixTree("sum")
    cpt.insert("hello", 100, ['h', 'e', 'l', 'l', 'o'])
    cpt.remove(['h'])
    assert cpt.weight == 0
    assert cpt.__len__() == 0
    cpt.insert('help', 12, ['h', 'e', 'l', 'p'])
    cpt.insert('hello', 2, ['h', 'e', 'l', 'l', 'o'])
    cpt.insert('he man', 23, ['h', 'e', ' ', 'm', 'a', 'n'])
    cpt.insert('hello', 12, ['h', 'e', 'l', 'l', 'o'])
    cpt.remove(['h'])
    assert cpt.weight == 0
    assert cpt.__len__() == 0
    cpt.insert('help', 12, ['h', 'e', 'l', 'p'])
    cpt.insert('hello', 2, ['h', 'e', 'l', 'l', 'o'])
    cpt.insert('he man', 23, ['h', 'e', ' ', 'm', 'a', 'n'])
    cpt.insert('hello', 12, ['h', 'e', 'l', 'l', 'o'])
    cpt.remove(['h', 'e'])
    assert cpt.weight == 0
    assert cpt.__len__() == 0
    cpt.insert('help', 12, ['h', 'e', 'l', 'p'])
    cpt.insert('hello', 2, ['h', 'e', 'l', 'l', 'o'])
    cpt.insert('he man', 23, ['h', 'e', ' ', 'm', 'a', 'n'])
    cpt.insert('hello', 12, ['h', 'e', 'l', 'l', 'o'])
    cpt.remove(['h', 'e', 'l'])
    assert cpt.__len__() == 1
    assert cpt.subtrees[0].__len__() == 1
    assert cpt.subtrees[0].subtrees[0].__len__() == 1
    assert cpt.subtrees[0].subtrees[0].subtrees[0].__len__() == 1
    assert cpt.weight == 23
    assert cpt.subtrees[0].weight == 23
    assert cpt.subtrees[0].subtrees[0].weight == 23
    assert cpt.subtrees[0].subtrees[0].subtrees[0].weight == 23
    cpt.remove(['h'])
    assert cpt.__len__() == 0
    assert cpt.weight == 0
    cpt.insert('swell', 75, ['s', 'w', 'e', 'l', 'l'])
    cpt.insert('sweet', 50, ['s', 'w', 'e', 'e', 't'])
    cpt.insert('swat', 51, ['s', 'w', 'a', 't'])
    cpt.insert('swap', 76, ['s', 'w', 'a', 'p'])
    cpt.remove(['s', 'w'])


@given(inserts=lists(
                    tuples(
                           lists(characters(whitelist_categories=('L', 'Nd'))),
                           integers(min_value=1))),
       removes=lists(
                     lists(characters(whitelist_categories=('L', 'Nd'))),
                     max_size=4))
def test_propertys_cpt(inserts, removes):
    cpt = CompressedPrefixTree('average')
    for insert in inserts:
        cpt.insert(str(insert[0]), insert[1], insert[0])

    check_rep_vars_cpt(cpt)

    for remove in removes:
        cpt.remove(remove)

    check_rep_vars_cpt(cpt)


def check_rep_vars_cpt(cpt: CompressedPrefixTree) -> None:

    if cpt.is_empty():
        assert cpt.subtrees == []
    else:
        if cpt.subtrees != []:
            assert isinstance(cpt.value, list)

        # check for redundent trees
        if len(cpt.subtrees) == 1:
            assert cpt.subtrees[0].is_leaf() or cpt.subtrees[0].subtrees[0]\
                 .is_leaf() # TODO NEED TO CHECK this assumtion

        # check subtrees are sorted
        assert cpt.subtrees == sorted(cpt.subtrees, key=lambda spt: spt.weight,
                                      reverse=True)

        sumed_weight_len = calc_sumed_weight_len_spt(cpt)

        # check weight is good
        assert sumed_weight_len[0] / sumed_weight_len[1] == cpt.weight

        # check len is good
        assert sumed_weight_len[1] == len(cpt)

        # check still subtrees are good
        for subtree in cpt.subtrees:
            check_rep_vars_cpt(subtree)


@given(inserts=lists(
                    tuples(
                           lists(characters(whitelist_categories=('L', 'Nd'))),
                           integers(min_value=1))),
       removes=lists(
                     lists(characters(whitelist_categories=('L', 'Nd'))),
                     max_size=4))
def test_propertys_spt(inserts, removes):
    """Test that after insertion and deletion the representaion invariants of
    the tree are maintained."""

    spt = SimplePrefixTree('average')
    for insert in inserts:
        spt.insert(str(insert[0]), insert[1], insert[0])

    check_rep_vars_spt(spt)

    for remove in removes:
        spt.remove(remove)

    check_rep_vars_spt(spt)


def check_rep_vars_spt(spt: SimplePrefixTree) -> None:
    """Test that after insertion and deletion the representaion invariants of
    the tree are maintained."""
    if spt.is_empty():
        assert spt.subtrees == []
    else:
        if spt.subtrees != []:
            assert isinstance(spt.value, list)

        assert spt.subtrees == sorted(spt.subtrees, key=lambda spt: spt.weight,
                                      reverse=True)

        sumed_weight_len = calc_sumed_weight_len_spt(spt)

        assert sumed_weight_len[0] / sumed_weight_len[1] == spt.weight

        assert sumed_weight_len[1] == len(spt)

        for subtree in spt.subtrees:
            check_rep_vars_spt(subtree)


def calc_sumed_weight_len_spt(spt: SimplePrefixTree):
    if spt.is_empty():
        return 0, 0
    elif spt.subtrees == []:
        return spt.weight, 1
    else:
        weight = 0
        leangth = 0
        for subtree in spt.subtrees:
           w_l = calc_sumed_weight_len_spt(subtree)
           weight += w_l[0]
           leangth += w_l[1]
        return weight, leangth


if __name__ == '__main__':
    pytest.main(['prefix_tree_tests.py', 'v'])
