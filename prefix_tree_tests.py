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
    """
    >>> cpt = CompressedPrefixTree('sum')
    >>> cpt.insert('help', 10.0, ['h', 'e', 'l', 'p'])
    >>> cpt._print_wl()
    ['h', 'e', 'l', 'p'] (10.0) (1)
      help (10.0) (1)
    <BLANKLINE>
    >>> cpt.insert('help', 2.0, ['h', 'e', 'l', 'p'])
    >>> cpt._print_wl()
    ['h', 'e', 'l', 'p'] (12.0) (1)
      help (12.0) (1)
    <BLANKLINE>
    >>> cpt.insert('hello', 2.0, ['h', 'e', 'l', 'l', 'o'])
    >>> cpt._print_wl()
    ['h', 'e', 'l'] (14.0) (2)
      ['h', 'e', 'l', 'p'] (12.0) (1)
        help (12.0) (1)
      ['h', 'e', 'l', 'l', 'o'] (2.0) (1)
        hello (2.0) (1)
    <BLANKLINE>
    >>> cpt.insert('he man', 23.0, ['h', 'e', ' ', 'm', 'a', 'n'])
    >>> cpt._print_wl()
    ['h', 'e'] (37.0) (3)
      ['h', 'e', ' ', 'm', 'a', 'n'] (23.0) (1)
        he man (23.0) (1)
      ['h', 'e', 'l'] (14.0) (2)
        ['h', 'e', 'l', 'p'] (12.0) (1)
          help (12.0) (1)
        ['h', 'e', 'l', 'l', 'o'] (2.0) (1)
          hello (2.0) (1)
    <BLANKLINE>
    >>> cpt.insert('hello', 12.0, ['h', 'e', 'l', 'l', 'o'])
    >>> cpt._print_wl()
    ['h', 'e'] (49.0) (3)
      ['h', 'e', 'l'] (26.0) (2)
        ['h', 'e', 'l', 'l', 'o'] (14.0) (1)
          hello (14.0) (1)
        ['h', 'e', 'l', 'p'] (12.0) (1)
          help (12.0) (1)
      ['h', 'e', ' ', 'm', 'a', 'n'] (23.0) (1)
        he man (23.0) (1)
    <BLANKLINE>
    >>> cpt.insert('bet', 14.0, ['b', 'e', 't'])
    >>> cpt._print_wl()
    [] (63.0) (4)
      ['h', 'e'] (49.0) (3)
        ['h', 'e', 'l'] (26.0) (2)
          ['h', 'e', 'l', 'l', 'o'] (14.0) (1)
            hello (14.0) (1)
          ['h', 'e', 'l', 'p'] (12.0) (1)
            help (12.0) (1)
        ['h', 'e', ' ', 'm', 'a', 'n'] (23.0) (1)
          he man (23.0) (1)
      ['b', 'e', 't'] (14.0) (1)
        bet (14.0) (1)
    <BLANKLINE>
    >>> cpt.insert('bet', 200.0, ['b', 'e', 't'])
    >>> cpt._print_wl()
    [] (263.0) (4)
      ['b', 'e', 't'] (214.0) (1)
        bet (214.0) (1)
      ['h', 'e'] (49.0) (3)
        ['h', 'e', 'l'] (26.0) (2)
          ['h', 'e', 'l', 'l', 'o'] (14.0) (1)
            hello (14.0) (1)
          ['h', 'e', 'l', 'p'] (12.0) (1)
            help (12.0) (1)
        ['h', 'e', ' ', 'm', 'a', 'n'] (23.0) (1)
          he man (23.0) (1)
    <BLANKLINE>
    >>> cpt.insert('', 50.0, [])
    >>> cpt._print_wl()
    [] (313.0) (5)
      ['b', 'e', 't'] (214.0) (1)
        bet (214.0) (1)
       (50.0) (1)
      ['h', 'e'] (49.0) (3)
        ['h', 'e', 'l'] (26.0) (2)
          ['h', 'e', 'l', 'l', 'o'] (14.0) (1)
            hello (14.0) (1)
          ['h', 'e', 'l', 'p'] (12.0) (1)
            help (12.0) (1)
        ['h', 'e', ' ', 'm', 'a', 'n'] (23.0) (1)
          he man (23.0) (1)
    <BLANKLINE>
    >>> cpt.insert('co', 130.0, ['c', 'o'])
    >>> cpt._print_wl()
    [] (443.0) (6)
      ['b', 'e', 't'] (214.0) (1)
        bet (214.0) (1)
      ['c', 'o'] (130.0) (1)
        co (130.0) (1)
       (50.0) (1)
      ['h', 'e'] (49.0) (3)
        ['h', 'e', 'l'] (26.0) (2)
          ['h', 'e', 'l', 'l', 'o'] (14.0) (1)
            hello (14.0) (1)
          ['h', 'e', 'l', 'p'] (12.0) (1)
            help (12.0) (1)
        ['h', 'e', ' ', 'm', 'a', 'n'] (23.0) (1)
          he man (23.0) (1)
    <BLANKLINE>
    >>> cpt = CompressedPrefixTree('average')
    >>> cpt.insert('abc', 10.0, ['a', 'b', 'c'])
    >>> cpt._print_wl()
    ['a', 'b', 'c'] (10.0) (1)
      abc (10.0) (1)
    <BLANKLINE>
    >>> cpt.insert('apples', 60.0, ['a', 'p', 'p', 'l', 'e', 's'])
    >>> cpt._print_wl()
    ['a'] (35.0) (2)
      ['a', 'p', 'p', 'l', 'e', 's'] (60.0) (1)
        apples (60.0) (1)
      ['a', 'b', 'c'] (10.0) (1)
        abc (10.0) (1)
    <BLANKLINE>
    >>> cpt.insert('abc', 10.0, ['a', 'b', 'c'])
    >>> cpt._print_wl()
    ['a'] (40.0) (2)
      ['a', 'p', 'p', 'l', 'e', 's'] (60.0) (1)
        apples (60.0) (1)
      ['a', 'b', 'c'] (20.0) (1)
        abc (20.0) (1)
    <BLANKLINE>
    >>> cpt.insert('abop', 40.0, ['a', 'b', 'o', 'p'])
    >>> cpt.insert('abort', 510.0, ['a', 'b', 'o', 'r', 't'])
    >>> cpt._print_wl()
    ['a'] (157.5) (4)
      ['a', 'b'] (190.0) (3)
        ['a', 'b', 'o'] (275.0) (2)
          ['a', 'b', 'o', 'r', 't'] (510.0) (1)
            abort (510.0) (1)
          ['a', 'b', 'o', 'p'] (40.0) (1)
            abop (40.0) (1)
        ['a', 'b', 'c'] (20.0) (1)
          abc (20.0) (1)
      ['a', 'p', 'p', 'l', 'e', 's'] (60.0) (1)
        apples (60.0) (1)
    <BLANKLINE>
    """
    pass

def test_cpt_remove() -> None:
    """
    >>> cpt = CompressedPrefixTree('sum')
    >>> cpt.insert('help', 10.0, ['h', 'e', 'l', 'p'])
    >>> cpt.insert('help', 2.0, ['h', 'e', 'l', 'p'])
    >>> cpt.insert('hello', 2.0, ['h', 'e', 'l', 'l', 'o'])
    >>> cpt.insert('he man', 23.0, ['h', 'e', ' ', 'm', 'a', 'n'])
    >>> cpt.insert('hello', 12.0, ['h', 'e', 'l', 'l', 'o'])
    >>> cpt.insert('bet', 14.0, ['b', 'e', 't'])
    >>> cpt.insert('bet', 200.0, ['b', 'e', 't'])
    >>> cpt.insert('', 50.0, [])
    >>> cpt.insert('co', 130.0, ['c', 'o'])
    >>> cpt._print_wl()
    [] (443.0) (6)
      ['b', 'e', 't'] (214.0) (1)
        bet (214.0) (1)
      ['c', 'o'] (130.0) (1)
        co (130.0) (1)
       (50.0) (1)
      ['h', 'e'] (49.0) (3)
        ['h', 'e', 'l'] (26.0) (2)
          ['h', 'e', 'l', 'l', 'o'] (14.0) (1)
            hello (14.0) (1)
          ['h', 'e', 'l', 'p'] (12.0) (1)
            help (12.0) (1)
        ['h', 'e', ' ', 'm', 'a', 'n'] (23.0) (1)
          he man (23.0) (1)
    <BLANKLINE>
    >>> cpt.remove(['h', 'e', 'l'])
    >>> cpt._print_wl()
    [] (417.0) (4)
      ['b', 'e', 't'] (214.0) (1)
        bet (214.0) (1)
      ['c', 'o'] (130.0) (1)
        co (130.0) (1)
       (50.0) (1)
      ['h', 'e', ' ', 'm', 'a', 'n'] (23.0) (1)
        he man (23.0) (1)
    <BLANKLINE>
    """
    pass
    # cpt = CompressedPrefixTree("sum")
    # cpt.insert("hello", 100, ['h', 'e', 'l', 'l', 'o'])
    # cpt.remove(['h'])
    # assert cpt.weight == 0
    # assert cpt.__len__() == 0
    # cpt.insert('help', 12, ['h', 'e', 'l', 'p'])
    # cpt.insert('hello', 2, ['h', 'e', 'l', 'l', 'o'])
    # cpt.insert('he man', 23, ['h', 'e', ' ', 'm', 'a', 'n'])
    # cpt.insert('hello', 12, ['h', 'e', 'l', 'l', 'o'])
    # cpt.remove(['h'])
    # assert cpt.weight == 0
    # assert cpt.__len__() == 0
    # cpt.insert('help', 12, ['h', 'e', 'l', 'p'])
    # cpt.insert('hello', 2, ['h', 'e', 'l', 'l', 'o'])
    # cpt.insert('he man', 23, ['h', 'e', ' ', 'm', 'a', 'n'])
    # cpt.insert('hello', 12, ['h', 'e', 'l', 'l', 'o'])
    # cpt.remove(['h', 'e'])
    # assert cpt.weight == 0
    # assert cpt.__len__() == 0
    # cpt.insert('help', 12, ['h', 'e', 'l', 'p'])
    # cpt.insert('hello', 2, ['h', 'e', 'l', 'l', 'o'])
    # cpt.insert('he man', 23, ['h', 'e', ' ', 'm', 'a', 'n'])
    # cpt.insert('hello', 12, ['h', 'e', 'l', 'l', 'o'])
    # cpt.remove(['h', 'e', 'l'])
    # assert cpt.__len__() == 1
    # assert cpt.subtrees[0].__len__() == 1
    # assert cpt.subtrees[0].subtrees[0].__len__() == 1
    # assert cpt.subtrees[0].subtrees[0].subtrees[0].__len__() == 1
    # assert cpt.weight == 23
    # assert cpt.subtrees[0].weight == 23
    # assert cpt.subtrees[0].subtrees[0].weight == 23
    # assert cpt.subtrees[0].subtrees[0].subtrees[0].weight == 23
    # cpt.remove(['h'])
    # assert cpt.__len__() == 0
    # assert cpt.weight == 0
    # cpt.insert('swell', 75, ['s', 'w', 'e', 'l', 'l'])
    # cpt.insert('sweet', 50, ['s', 'w', 'e', 'e', 't'])
    # cpt.insert('swat', 51, ['s', 'w', 'a', 't'])
    # cpt.insert('swap', 76, ['s', 'w', 'a', 'p'])
    # cpt.remove(['s', 'w'])


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
            assert cpt.subtrees[0].is_leaf()

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
            # Subtree value should be prefix of tree value
            if not subtree.is_leaf():
                assert _is_prefix(cpt.value, subtree.value)

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

        # check still subtrees are good
        for subtree in spt.subtrees:
            # Subtree value should be prefix of tree value
            if not subtree.is_leaf():
                assert _is_prefix(spt.value, subtree.value)
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


def _is_prefix(prefix, items) -> bool:
    if len(prefix) > len(items):
        return False

    for p, i in zip(prefix, items):
        if p != i:
            return False
    return True




if __name__ == '__main__':
    pytest.main(['prefix_tree_tests.py', 'v'])
