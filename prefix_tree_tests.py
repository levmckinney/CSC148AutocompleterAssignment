from prefix_tree import SimplePrefixTree, CompressedPrefixTree
from timeit import timeit
import pytest
import matplotlib.pyplot as plt
from hypothesis import given
from hypothesis.strategies import integers, characters, lists, tuples
import random as r
import string as s
from autocomplete_engines import LetterAutocompleteEngine, SentenceAutocompleteEngine, Melody, MelodyAutocompleteEngine

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

def test_value_as_list_then_string() -> None:
    """
    >>> spt = SimplePrefixTree('sum')
    >>> spt.insert('hello', 80, ['h', 'e', 'l', 'l', 'o'])
    >>> spt.insert('help', 10, ['h', 'e', 'l', 'p'])
    >>> spt.insert('hell', 20, ['h', 'e', 'l', 'l'])
    >>> spt.insert('he', 109, ['h', 'e'])
    >>> spt.insert('heart', 50, ['h', 'e', 'a', 'r', 't'])
    >>> spt.insert('heal', 45, ['h', 'e', 'a', 'l'])
    >>> spt.insert('heap', 46, ['h', 'e', 'a', 'p'])
    >>> spt.insert(['h', 'e', 'a', 't'], 47, ['h', 'e', 'a', 't'])
    >>> spt._print_wl()
    [] (407) (8)
      ['h'] (407) (8)
        ['h', 'e'] (407) (8)
          ['h', 'e', 'a'] (188) (4)
            ['h', 'e', 'a', 'r'] (50) (1)
              ['h', 'e', 'a', 'r', 't'] (50) (1)
                heart (50) (1)
            ['h', 'e', 'a', 't'] (47) (1)
              ['h', 'e', 'a', 't'] (47) (1)
            ['h', 'e', 'a', 'p'] (46) (1)
              heap (46) (1)
            ['h', 'e', 'a', 'l'] (45) (1)
              heal (45) (1)
          ['h', 'e', 'l'] (110) (3)
            ['h', 'e', 'l', 'l'] (100) (2)
              ['h', 'e', 'l', 'l', 'o'] (80) (1)
                hello (80) (1)
              hell (20) (1)
            ['h', 'e', 'l', 'p'] (10) (1)
              help (10) (1)
          he (109) (1)
    <BLANKLINE>
    >>> spt.insert('heat', 100, ['h', 'e', 'a', 't'])
    >>> spt._print_wl()
    [] (507) (9)
      ['h'] (507) (9)
        ['h', 'e'] (507) (9)
          ['h', 'e', 'a'] (288) (5)
            ['h', 'e', 'a', 't'] (147) (2)
              heat (100) (1)
              ['h', 'e', 'a', 't'] (47) (1)
            ['h', 'e', 'a', 'r'] (50) (1)
              ['h', 'e', 'a', 'r', 't'] (50) (1)
                heart (50) (1)
            ['h', 'e', 'a', 'p'] (46) (1)
              heap (46) (1)
            ['h', 'e', 'a', 'l'] (45) (1)
              heal (45) (1)
          ['h', 'e', 'l'] (110) (3)
            ['h', 'e', 'l', 'l'] (100) (2)
              ['h', 'e', 'l', 'l', 'o'] (80) (1)
                hello (80) (1)
              hell (20) (1)
            ['h', 'e', 'l', 'p'] (10) (1)
              help (10) (1)
          he (109) (1)
    <BLANKLINE>
    >>> cpt = CompressedPrefixTree('sum')
    >>> cpt.insert('hello', 80, ['h', 'e', 'l', 'l', 'o'])
    >>> cpt.insert('help', 10, ['h', 'e', 'l', 'p'])
    >>> cpt.insert('hell', 20, ['h', 'e', 'l', 'l'])
    >>> cpt.insert('he', 109, ['h', 'e'])
    >>> cpt.insert('heart', 50, ['h', 'e', 'a', 'r', 't'])
    >>> cpt.insert('heal', 45, ['h', 'e', 'a', 'l'])
    >>> cpt.insert('heap', 46, ['h', 'e', 'a', 'p'])
    >>> cpt.insert(['h', 'e', 'a', 't'], 47, ['h', 'e', 'a', 't'])
    >>> cpt._print_wl()
    ['h', 'e'] (407) (8)
      ['h', 'e', 'a'] (188) (4)
        ['h', 'e', 'a', 'r', 't'] (50) (1)
          heart (50) (1)
        ['h', 'e', 'a', 't'] (47) (1)
          ['h', 'e', 'a', 't'] (47) (1)
        ['h', 'e', 'a', 'p'] (46) (1)
          heap (46) (1)
        ['h', 'e', 'a', 'l'] (45) (1)
          heal (45) (1)
      ['h', 'e', 'l'] (110) (3)
        ['h', 'e', 'l', 'l'] (100) (2)
          ['h', 'e', 'l', 'l', 'o'] (80) (1)
            hello (80) (1)
          hell (20) (1)
        ['h', 'e', 'l', 'p'] (10) (1)
          help (10) (1)
      he (109) (1)
    <BLANKLINE>
    >>> cpt.insert('heat', 100, ['h', 'e', 'a', 't'])
    >>> cpt._print_wl()
    ['h', 'e'] (507) (9)
      ['h', 'e', 'a'] (288) (5)
        ['h', 'e', 'a', 't'] (147) (2)
          heat (100) (1)
          ['h', 'e', 'a', 't'] (47) (1)
        ['h', 'e', 'a', 'r', 't'] (50) (1)
          heart (50) (1)
        ['h', 'e', 'a', 'p'] (46) (1)
          heap (46) (1)
        ['h', 'e', 'a', 'l'] (45) (1)
          heal (45) (1)
      ['h', 'e', 'l'] (110) (3)
        ['h', 'e', 'l', 'l'] (100) (2)
          ['h', 'e', 'l', 'l', 'o'] (80) (1)
            hello (80) (1)
          hell (20) (1)
        ['h', 'e', 'l', 'p'] (10) (1)
          help (10) (1)
      he (109) (1)
    <BLANKLINE>
    >>> spt.autocomplete(['h', 'e', 'a'], 3)
    [('heat', 100), ('heart', 50), (['h', 'e', 'a', 't'], 47)]
    >>> cpt.autocomplete(['h', 'e', 'a'], 3)
    [('heat', 100), ('heart', 50), (['h', 'e', 'a', 't'], 47)]
    >>> spt.remove(['h', 'e', 'a', 't'])
    >>> spt._print_wl()
    [] (360.0) (7)
      ['h'] (360.0) (7)
        ['h', 'e'] (360.0) (7)
          ['h', 'e', 'a'] (141.0) (3)
            ['h', 'e', 'a', 'r'] (50) (1)
              ['h', 'e', 'a', 'r', 't'] (50) (1)
                heart (50) (1)
            ['h', 'e', 'a', 'p'] (46) (1)
              heap (46) (1)
            ['h', 'e', 'a', 'l'] (45) (1)
              heal (45) (1)
          ['h', 'e', 'l'] (110) (3)
            ['h', 'e', 'l', 'l'] (100) (2)
              ['h', 'e', 'l', 'l', 'o'] (80) (1)
                hello (80) (1)
              hell (20) (1)
            ['h', 'e', 'l', 'p'] (10) (1)
              help (10) (1)
          he (109) (1)
    <BLANKLINE>
    >>> cpt.remove(['h', 'e', 'a', 't'])
    >>> cpt._print_wl()
    ['h', 'e'] (360) (7)
      ['h', 'e', 'a'] (141) (3)
        ['h', 'e', 'a', 'r', 't'] (50) (1)
          heart (50) (1)
        ['h', 'e', 'a', 'p'] (46) (1)
          heap (46) (1)
        ['h', 'e', 'a', 'l'] (45) (1)
          heal (45) (1)
      ['h', 'e', 'l'] (110) (3)
        ['h', 'e', 'l', 'l'] (100) (2)
          ['h', 'e', 'l', 'l', 'o'] (80) (1)
            hello (80) (1)
          hell (20) (1)
        ['h', 'e', 'l', 'p'] (10) (1)
          help (10) (1)
      he (109) (1)
    <BLANKLINE>
    """
    pass


def test_melody() -> None:
    e1 = MelodyAutocompleteEngine({'file': 'data/songbook.csv', 'autocompleter': 'simple', 'weight_type': 'sum'})
    e2 = MelodyAutocompleteEngine({'file': 'data/songbook.csv', 'autocompleter': 'compressed', 'weight_type': 'sum'})
    for a in range(-6, 6, 1):
        for b in range(-10, 10, 1):
            for c in range(-3, 3, 1):
                intervals = [a, b, c]
                m1 = e1.autocomplete(intervals, 20)
                m2 = e2.autocomplete(intervals, 20)
                assert len(m1) == len(m2)
                for i in range(len(m1)):
                    assert len(m1[i]) == len(m2[i])
                    assert m1[i][0].name == m2[i][0].name
                    assert m1[i][0].notes == m2[i][0].notes
                    assert m1[i][1] == m2[i][1]
    e1 = MelodyAutocompleteEngine({'file': 'data/songbook.csv', 'autocompleter': 'simple', 'weight_type': 'average'})
    e2 = MelodyAutocompleteEngine({'file': 'data/songbook.csv', 'autocompleter': 'compressed', 'weight_type': 'average'})
    for a in range(-6, 6, 1):
        for b in range(-10, 10, 1):
            for c in range(-3, 3, 1):
                intervals = [a, b, c]
                m1 = e1.autocomplete(intervals, 20)
                m2 = e2.autocomplete(intervals, 20)
                assert len(m1) == len(m2)
                for i in range(len(m1)):
                    assert len(m1[i]) == len(m2[i])
                    assert m1[i][0].name == m2[i][0].name
                    assert m1[i][0].notes == m2[i][0].notes
                    assert m1[i][1] == m2[i][1]

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
    >>> cpt.remove([])
    >>> cpt._len == 0 and cpt.weight == 0.0
    True
    """
    pass


def test_sentence_autocomplete() -> None:
    """A sample run of the sentence autocomplete engine."""
    e1 = LetterAutocompleteEngine({
        # NOTE: you should also try 'data/google_no_swears.txt' for the file.
        'file': 'data/lotr.txt',
        'autocompleter': 'simple',
        'weight_type': 'sum'
    })
    e2 = LetterAutocompleteEngine({
        # NOTE: you should also try 'data/google_no_swears.txt' for the file.
        'file': 'data/lotr.txt',
        'autocompleter': 'compressed',
        'weight_type': 'sum'
    })
    f1 = LetterAutocompleteEngine({
        # NOTE: you should also try 'data/google_no_swears.txt' for the file.
        'file': 'data/lotr.txt',
        'autocompleter': 'simple',
        'weight_type': 'average'
    })
    f2 = LetterAutocompleteEngine({
        # NOTE: you should also try 'data/google_no_swears.txt' for the file.
        'file': 'data/lotr.txt',
        'autocompleter': 'compressed',
        'weight_type': 'average'
    })
    phrase = ['why do', 'how could', 'we do', 'hockey game', 'wild', 'yeet']
    for a in range(0, len(phrase), 1):
        m1 = e1.autocomplete(phrase, 22)
        m2 = e2.autocomplete(phrase, 20)
        assert len(m1) == len(m2)
        for i in range(len(m1)):
            assert len(m1[i]) == len(m2[i])
            assert m1[i][0] == m2[i][0]
            assert m1[i][1] == m2[i][1]
            n1 = f1.autocomplete(phrase, 20)
            n2 = f2.autocomplete(phrase, 20)
            assert len(n1) == len(n2)
            for i in range(len(n1)):
                assert len(n1[i]) == len(n2[i])
                assert n1[i][0] == n2[i][0]
                assert n1[i][1] == n2[i][1]

    """
# THESE HIT RECURSION LIMIT

def test_letter_autocomplete() -> None:
    #A sample run of the letter autocomplete engine.
    e1 = LetterAutocompleteEngine({
        # NOTE: you should also try 'data/google_no_swears.txt' for the file.
        'file': 'data/lotr.txt',
        'autocompleter': 'simple',
        'weight_type': 'sum'
    })
    e2 = LetterAutocompleteEngine({
        # NOTE: you should also try 'data/google_no_swears.txt' for the file.
        'file': 'data/lotr.txt',
        'autocompleter': 'compressed',
        'weight_type': 'sum'
    })
    f1 = LetterAutocompleteEngine({
        # NOTE: you should also try 'data/google_no_swears.txt' for the file.
        'file': 'data/google_no_swears.txt',
        'autocompleter': 'simple',
        'weight_type': 'average'
    })
    f2 = LetterAutocompleteEngine({
        # NOTE: you should also try 'data/google_no_swears.txt' for the file.
        'file': 'data/google_no_swears.txt',
        'autocompleter': 'compressed',
        'weight_type': 'average'
    })
    alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i','j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    a = math.randint(0, 5)
    b = math.randint(5, 18)
    string = alpha[a] + alpha[b]
    m1 = e1.autocomplete(string, 20)
    m2 = e2.autocomplete(string, 20)
    assert len(m1) == len(m2)
    for i in range(len(m1)):
       assert len(m1[i]) == len(m2[i])
       assert m1[i][0] == m2[i][0]
       assert m1[i][1] == m2[i][1]
    n1 = f1.autocomplete(string, 20)
    n2 = f2.autocomplete(string, 20)
    assert len(n1) == len(n2)
    for i in range(len(n1)):
        assert len(n1[i]) == len(n2[i])
        assert n1[i][0] == n2[i][0]
        assert n1[i][1] == n2[i][1]


def test_sentence_autocomplete() -> None:
    #A sample run of the sentence autocomplete engine.
    engine = SentenceAutocompleteEngine({
        'file': 'data/google_searches.csv',
        'autocompleter': 'simple',
        'weight_type': 'sum'
    })
    e1 = LetterAutocompleteEngine({
        # NOTE: you should also try 'data/google_no_swears.txt' for the file.
        'file': 'data/lotr.txt',
        'autocompleter': 'simple',
        'weight_type': 'sum'
    })
    e2 = LetterAutocompleteEngine({
        # NOTE: you should also try 'data/google_no_swears.txt' for the file.
        'file': 'data/lotr.txt',
        'autocompleter': 'compressed',
        'weight_type': 'sum'
    })
    f1 = LetterAutocompleteEngine({
        # NOTE: you should also try 'data/google_no_swears.txt' for the file.
        'file': 'data/lotr.txt',
        'autocompleter': 'simple',
        'weight_type': 'average'
    })
    f2 = LetterAutocompleteEngine({
        # NOTE: you should also try 'data/google_no_swears.txt' for the file.
        'file': 'data/lotr.txt',
        'autocompleter': 'compressed',
        'weight_type': 'average'
    })
    phrase = ['why do', 'how could', 'we do', 'hockey game', 'wild', 'yeet']
    for a in range(0, len(phrase), 1):
        m1 = e1.autocomplete(phrase, 22)
        m2 = e2.autocomplete(phrase, 20)
        assert len(m1) == len(m2)
        for i in range(len(m1)):
          assert len(m1[i]) == len(m2[i])
          assert m1[i][0] == m2[i][0]
          assert m1[i][1] == m2[i][1]
          n1 = f1.autocomplete(phrase, 20)
          n2 = f2.autocomplete(phrase, 20)
          assert len(n1) == len(n2)
          for i in range(len(n1)):
            assert len(n1[i]) == len(n2[i])
            assert n1[i][0] == n2[i][0]
            assert n1[i][1] == n2[i][1]
"""
"""
def test_large_cpt_insert() -> None:
    >>> cpt = CompressedPrefixTree('sum')
    >>> prefix = ['a', 'l', 'l', ' ', 'i', ' ', 'w', 'a', 'n', 't', ' ', \
        'i', 's', ' ', 'n', 'o', 't', 'h', 'i', 'n', 'g', ' ',\
        'm', 'o', 'r', 'e']
    >>> string = 'all i want is nothing more'
    >>> for i in range(len(prefix), 0, -1): \
        cpt.insert(string[:i], i+1, prefix[:i])
    >>> cpt.insert('', 1, [])
    >>> cpt._print_wl()
    []
    ['a']
    ['a', 'l']
    ['a', 'l', 'l']
    ['a', 'l', 'l', ' ']
    ['a', 'l', 'l', ' ', 'i']
    ['a', 'l', 'l', ' ', 'i', ' ']
    ['a', 'l', 'l', ' ', 'i', ' ', 'w']
    ['a', 'l', 'l', ' ', 'i', ' ', 'w', 'a']
    ['a', 'l', 'l', ' ', 'i', ' ', 'w', 'a', 'n']
    ['a', 'l', 'l', ' ', 'i', ' ', 'w', 'a', 'n', 't']
    ['a', 'l', 'l', ' ', 'i', ' ', 'w', 'a', 'n', 't', ' ']
    ['a', 'l', 'l', ' ', 'i', ' ', 'w', 'a', 'n', 't', ' ', 'i']
    ['a', 'l', 'l', ' ', 'i', ' ', 'w', 'a', 'n', 't', ' ', 'i', 's']
    ['a', 'l', 'l', ' ', 'i', ' ', 'w', 'a', 'n', 't', ' ', 'i', 's', ' ']
    ['a', 'l', 'l', ' ', 'i', ' ', 'w', 'a', 'n', 't', ' ', 'i', 's', ' ', 'n']
    ['a', 'l', 'l', ' ', 'i', ' ', 'w', 'a', 'n', 't', ' ', 'i', 's', ' ', 'n', 'o']
    ['a', 'l', 'l', ' ', 'i', ' ', 'w', 'a', 'n', 't', ' ', 'i', 's', ' ', 'n', 'o', 't']
    ['a', 'l', 'l', ' ', 'i', ' ', 'w', 'a', 'n', 't', ' ', 'i', 's', ' ', 'n', 'o', 't', 'h']
    ['a', 'l', 'l', ' ', 'i', ' ', 'w', 'a', 'n', 't', ' ', 'i', 's', ' ', 'n', 'o', 't', 'h', 'i']
    ['a', 'l', 'l', ' ', 'i', ' ', 'w', 'a', 'n', 't', ' ', 'i', 's', ' ', 'n', 'o', 't', 'h', 'i', 'n']
    ['a', 'l', 'l', ' ', 'i', ' ', 'w', 'a', 'n', 't', ' ', 'i', 's', ' ', 'n', 'o', 't', 'h', 'i', 'n', 'g']
    ['a', 'l', 'l', ' ', 'i', ' ', 'w', 'a', 'n', 't', ' ', 'i', 's', ' ', 'n', 'o', 't', 'h', 'i', 'n', 'g', ' ']
    ['a', 'l', 'l', ' ', 'i', ' ', 'w', 'a', 'n', 't', ' ', 'i', 's', ' ', 'n', 'o', 't', 'h', 'i', 'n', 'g', ' ', 'm', 'o']
    ['a', 'l', 'l', ' ', 'i', ' ', 'w', 'a', 'n', 't', ' ', 'i', 's', ' ', 'n', 'o', 't', 'h', 'i', 'n', 'g', ' ', 'm', 'o', 'r'] (2.0) (2)
    ['a', 'l', 'l', ' ', 'i', ' ', 'w', 'a', 'n', 't', ' ', 'i', 's', ' ', 'n', 'o', 't', 'h', 'i', 'n', 'g', ' ', 'm', 'o', 'r', 'e'] (1.0) (1)
    """
    pass

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

"""
SIMPLE AND COMPRESSED PREFIX TREE BOTH NEED THESE METHODS FOR TESTING

def _print_wl(self) -> str:
#Return a string representation of this tree.
#This now includes length in edition to weight.
print(self._all_indented())

def _all_indented(self, depth: int = 0) -> str:
#Return an indented string representation of this tree.
#The indentation level is specified by the <depth> parameter.
if self.is_empty():
    return ''
else:
    s = '  ' * depth + f'{self.value} ({self.weight}) ({self._len})\n'
    for subtree in self.subtrees:
        s += subtree._all_indented(depth + 1)
    return s
"""


if __name__ == '__main__':
    pytest.main(['prefix_tree_tests.py', 'v'])
    test_letter_autocomplete()
