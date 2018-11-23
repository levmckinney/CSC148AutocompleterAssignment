"""CSC148 Assignment 2: Autocompleter classes

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This file contains the design of a public interface (Autocompleter) and two
implementation of this interface, SimplePrefixTree and CompressedPrefixTree.
You'll complete both of these subclasses over the course of this assignment.

As usual, be sure not to change any parts of the given *public interface* in the
starter code---and this includes the instance attributes, which we will be
testing directly! You may, however, add new private attributes, methods, and
top-level functions to this file.
"""
from __future__ import annotations
from typing import Any, List, Optional, Tuple


################################################################################
# The Autocompleter ADT
################################################################################
class Autocompleter:
    """An abstract class representing the Autocompleter Abstract Data Type.
    """
    def __len__(self) -> int:
        """Return the number of values stored in this Autocompleter."""
        raise NotImplementedError

    def insert(self, value: Any, weight: float, prefix: List) -> None:
        """Insert the given value into this Autocompleter.

        The value is inserted with the given weight, and is associated with
        the prefix sequence <prefix>.

        If the value has already been inserted into this prefix tree
        (compare values using ==), then the given weight should be *added* to
        the existing weight of this value.

        Preconditions:
            weight > 0
            The given value is either:
                1) not in this Autocompleter
                2) was previously inserted with the SAME prefix sequence
        """
        raise NotImplementedError

    def autocomplete(self, prefix: List,
                     limit: Optional[int] = None) -> List[Tuple[Any, float]]:
        """Return up to <limit> matches for the given prefix.

        The return value is a list of tuples (value, weight), and must be
        ordered in non-increasing weight. (You can decide how to break ties.)

        If limit is None, return *every* match for the given prefix.

        Precondition: limit is None or limit > 0.
        """
        raise NotImplementedError

    def remove(self, prefix: List) -> None:
        """Remove all values that match the given prefix.
        """
        raise NotImplementedError


################################################################################
# SimplePrefixTree (Tasks 1-3)
################################################################################
class SimplePrefixTree(Autocompleter):
    """A simple prefix tree.

    This class follows the implementation described on the assignment handout.
    Note that we've made the attributes public because we will be accessing them
    directly for testing purposes.

    === Attributes ===
    value:
        The value stored at the root of this prefix tree, or [] if this
        prefix tree is empty.
    weight:
        The weight of this prefix tree. If this tree is a leaf, this attribute
        stores the weight of the value stored in the leaf. If this tree is
        not a leaf and non-empty, this attribute stores the *aggregate weight*
        of the leaf weights in this tree.
    subtrees:
        A list of subtrees of this prefix tree.

    === Representation invariants ===
    - self.weight >= 0

    - (EMPTY TREE):
        If self.weight == 0, then self.value == [] and self.subtrees == [].
        This represents an empty simple prefix tree.
    - (LEAF):
        If self.subtrees == [] and self.weight > 0, this tree is a leaf.
        (self.value is a value that was inserted into this tree.)
    - (NON-EMPTY, NON-LEAF):
        If len(self.subtrees) > 0, then self.value is a list (*common prefix*),
        and self.weight > 0 (*aggregate weight*).

    - ("prefixes grow by 1")
      If len(self.subtrees) > 0, and subtree in self.subtrees, and subtree
      is non-empty and not a leaf, then

          subtree.value == self.value + [x], for some element x

    - self.subtrees does not contain any empty prefix trees.
    - self.subtrees is *sorted* in non-increasing order of their weights.
      (You can break ties any way you like.)
      Note that this applies to both leaves and non-leaf subtrees:
      both can appear in the same self.subtrees list, and both have a `weight`
      attribute.
    """
    value: Any
    weight: float
    subtrees: List[SimplePrefixTree]

    # === Private Instance Attributes ===
    # _weight_type: A string that specifies whether the weight of the
    # tree will be calculated as the 'sum' or the 'average' of the weights of
    # each leaf value in the tree.
    _weight_type: bool
    # _len: is the number of values currently stored in the tree
    _len: int
    # _summed_weight: this is the sum of the weights inserted into self
    # regardless of the value of _weight_type.
    _summed_weight: int
    # === Private Representation invariants ===
    # All trees have the same _weight_type as their subtrees.
    # _len >= 0
    # _len is always the number of leaf nodes(i.e. values) in the tree.

    def __init__(self, weight_type: str) -> None:
        """Initialize an empty simple prefix tree.

        Precondition: weight_type == 'sum' or weight_type == 'average'.

        The given <weight_type> value specifies how the aggregate weight
        of non-leaf trees should be calculated (see the assignment handout
        for details).
        """
        self.value = []
        self.subtrees = []
        self.weight = 0.0
        self._summed_weight = 0.0
        self._weight_type = weight_type
        self._len = 0

    def is_empty(self) -> bool:
        """Return whether this simple prefix tree is empty."""
        return self.weight == 0.0

    def is_leaf(self) -> bool:
        """Return whether this simple prefix tree is a leaf."""
        return self.weight > 0 and self.subtrees == []

    def __str__(self) -> str:
        """Return a string representation of this tree.

        You may find this method helpful for debugging.
        """
        return self._str_indented()

    def _str_indented(self, depth: int = 0) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            s = '  ' * depth + f'{self.value} ({self.weight})\n'
            for subtree in self.subtrees:
                s += subtree._str_indented(depth + 1)
            return s

    def __len__(self) -> int:
        """Return the number of values stored in this Autocompleter.

        >>> spt = SimplePrefixTree('sum')
        >>> spt.insert('hello', 20, ['h','e','l','l','o'])
        >>> spt.insert('help', 10, ['h','e','l','p'])
        >>> len(spt)
        2
        """
        # This only counts leaf nodes
        return self._len

    def insert(self, value: Any, weight: float, prefix: List) -> None:
        """Insert the given value into this Autocompleter.

        The value is inserted with the given weight, and is associated with
        the prefix sequence <prefix>.

        If the value has already been inserted into this prefix tree
        (compare values using ==), then the given weight should be *added* to
        the existing weight of this value.

        Preconditions:
            weight > 0
            The given value is either:
                1) not in this Autocompleter
                2) was previously inserted with the SAME prefix sequence



        >>> spt = SimplePrefixTree('sum')
        >>> spt.insert('hello', 20, ['h','e','l','l','o'])
        >>> print(spt)
        [] (20)
          ['h'] (20)
            ['h', 'e'] (20)
              ['h', 'e', 'l'] (20)
                ['h', 'e', 'l', 'l'] (20)
                  ['h', 'e', 'l', 'l', 'o'] (20)
                    hello (20)
            <BLANKLINE>
        """
        depth = len(self.value)
        self._len += 1

        subtree_index = self._find_subtree_with_prefix(prefix[:(depth + 1)])

        if depth == len(prefix):
            # We have reached the end of the prefix and will add a leaf.
            subtree = SimplePrefixTree(self._weight_type)
            subtree.value = value  # TODO this is an alias may cause problems for mutble tpyes
            subtree.weight = weight
            subtree._summed_weight = weight
            subtree._len = 1
            self._add_subtree(subtree)

        elif subtree_index is None:  # depth < len(prefix)
            # No prefix exists in the subtree so we add a new subtree.
            subtree = SimplePrefixTree(self._weight_type)
            subtree.value = prefix[:(depth + 1)]
            subtree.insert(value, weight, prefix)
            self._add_subtree(subtree)

        else:
            # A branch already exists so we go down it.
            self.subtrees[subtree_index].insert(value, weight, prefix)
            self._fix_subtree_at_index(subtree_index)
        self._calculate_weight()

    def _add_subtree(self, subtree: SimplePrefixTree) -> None:
        """ Place a subtree into self.subtrees in the correct position base on
        weight.
        """
        if self.subtrees:
            # This should only run the first time we fail to find a subtree.
            i = 0
            while i in range(0, len(self.subtrees)):
                if subtree.weight >= self.subtrees[i].weight:
                    # We are mutating the list and then breaking the
                    # loop so this is okay.
                    break
                i += 1

            self.subtrees.insert(i, subtree)
        else:  # self.subtrees == []
            self.subtrees.append(subtree)

    def remove(self, prefix: List) -> None:
        """Remove all values that match the given prefix.
        """
        self._remove_helper(prefix)

    def _remove_helper(self, prefix: List) -> int:
        """Just like remove but returns number of leaves deleted.
        """
        depth = len(self.value)

        if prefix == self.value:
            # make self empty and return its length
            self.subtrees = []
            self.weight = 0.0
            self._summed_weight = 0.0
            length = len(self)
            self._len = 0
            return length
        else:
            subtree_index = self._find_subtree_with_prefix(prefix[:(depth + 1)])

            if subtree_index is not None:
                subtree = self.subtrees[subtree_index]
                num_removed = subtree._remove_helper(prefix)

                self._len -= num_removed

                assert self._len >= 0 # TODO for testing remove

                self._calculate_weight()

                if subtree.is_empty():
                    self.subtrees.remove(subtree)

                    if self.is_empty():
                        self.value = []

                    # Since removing a subtree will never make the list unsorted
                    return num_removed
                else:
                    if num_removed != 0:
                        # We found prefix but all subtrees still needed
                        self._fix_subtree_at_index(subtree_index)
                    else:
                        # Prefix was not found
                        pass

                    return num_removed

    def _calculate_weight(self) -> None:
        """This recalculates the weight for this tree based on the weight of its
        subtrees
        Note: This method is not recursive.
        >>> spt = SimplePrefixTree('average')
        >>> spt.insert('hell', 200, ['h','e','l','l'])
        >>> spt.insert('heap', 100, ['h','e', 'a', 'p'])
        >>> spt.insert('hello', 50, ['h','e','l','l','o'])
        >>> print(spt)
        """
        self._summed_weight = sum([subtree._summed_weight
                                   for subtree in self.subtrees])
        if self._weight_type == 'sum':
            self.weight = self._summed_weight

        else:  # self._weight_type == 'average'
            if len(self) == 0:
                self.weight = 0
                self._summed_weight = 0
                return

            self.weight = self._summed_weight / len(self)

    def _find_subtree_with_prefix(self, prefix: list) -> Optional[int]:
        """Finds a subtree that matches a given  prefix and returns its index
        or None is it cant find one.
        """
        # TODO This makes the assumption there are no non-empty non-leaf subtrees with the same value.
        for i in range(0, len(self.subtrees)):
            if self.subtrees[i].value == prefix:
                return i

    def _fix_subtree_at_index(self, index: int) -> None:
        """If subtree at index is out of order it fixes that by shifting it
        left or right

        Precondition:
        index in range(0, len(self.subtrees))
        self.subtrees is all sorted except for subtree at index
        """
        subtree = self.subtrees[index]

        while True:
            if index > 0 and subtree.weight > self.subtrees[index - 1].weight:
                # Switch with index to left
                self.subtrees[index - 1], self.subtrees[index] = \
                    subtree, self.subtrees[index - 1]
            elif (index < len(self.subtrees) - 1
                  and subtree.weight < self.subtrees[index + 1].weight):
                # Switch with index to right
                self.subtrees[index + 1], self.subtrees[index] = \
                    subtree, self.subtrees[index + 1]
            else:
                # Current position ok
                return

    def autocomplete(self, prefix: List,
                     limit: Optional[int] = None) -> List[Tuple[Any, float]]:
        """Return up to <limit> matches for the given prefix.

        The return value is a list of tuples (value, weight), and must be
        ordered in non-increasing weight. (You can decide how to break ties.)

        If limit is None, return *every* match for the given prefix.

        Precondition: limit is None or limit > 0.
        >>> spt = SimplePrefixTree("sum")
        >>> spt.insert('hello', 80, ['h', 'e', 'l', 'l', 'o'])
        >>> spt.insert('help', 10, ['h', 'e', 'l', 'p'])
        >>> spt.insert('hell', 20, ['h', 'e', 'l', 'l'])
        >>> spt.insert('he', 109, ['h', 'e'])
        >>> spt.insert('heart', 50, ['h', 'e', 'a', 'r', 't'])
        >>> spt.insert('heal', 45, ['h', 'e', 'a', 'l'])
        >>> spt.insert('heap', 46, ['h', 'e', 'a', 'p'])
        >>> spt.insert('heat', 47, ['h', 'e', 'a', 't'])
        >>> spt.insert('all', 100, ['a', 'l', 'l'])
        >>> print(spt)
        [] (507)
          ['h'] (407)
            ['h', 'e'] (407)
              ['h', 'e', 'a'] (188)
                ['h', 'e', 'a', 'r'] (50)
                  ['h', 'e', 'a', 'r', 't'] (50)
                    heart (50)
                ['h', 'e', 'a', 't'] (47)
                  heat (47)
                ['h', 'e', 'a', 'p'] (46)
                  heap (46)
                ['h', 'e', 'a', 'l'] (45)
                  heal (45)
              ['h', 'e', 'l'] (110)
                ['h', 'e', 'l', 'l'] (100)
                  ['h', 'e', 'l', 'l', 'o'] (80)
                    hello (80)
                  hell (20)
                ['h', 'e', 'l', 'p'] (10)
                  help (10)
              he (109)
          ['a'] (100)
            ['a', 'l'] (100)
              ['a', 'l', 'l'] (100)
                all (100)
        <BLANKLINE>
        >>> spt.autocomplete([])
        [('he', 109), ('all', 100), ('hello', 80), ('heart', 50), ('heat', 47), ('heap', 46), ('heal', 45), ('hell', 20), ('help', 10)]
        >>> spt.autocomplete(['h', 'e'])
        [('he', 109), ('hello', 80), ('heart', 50), ('heat', 47), ('heap', 46), ('heal', 45), ('hell', 20), ('help', 10)]
        >>> spt.autocomplete(['h', 'e', 'a'])
        [('heart', 50), ('heat', 47), ('heap', 46), ('heal', 45)]
        >>> spt.autocomplete(['n', 'o', 'n', 'e'])
        []
        """
        depth = len(self.value)

        if len(prefix) == depth:
            return self._get_leaves_greedy(limit)
        else:
            # If we find an existing subtree go done it else non exist
            # and we return an empty list.
            for subtree in self.subtrees:
                if prefix[:(depth + 1)] == subtree.value:
                    return subtree.autocomplete(prefix, limit)
            return []

    def _get_leaves_greedy(self, limit: Optional[int]) -> (List[Tuple[Any, float]]):
        # THIS VERSION IS GREEDY (MOST EFFICIENT)
        # IF YOU WANT ALL THE OBJECTS, SET THIS LIMIT TO LEN(SELF)
        """ The return value is a list with a tuple (value, weight) for each leaf.
        This is ordered in non-increasing weight.
        """

        if self.is_empty():
            return []
        elif self.subtrees == []:
            # Reached leaf node
            return [(self.value, self.weight)]
        else:
            if limit is None:
                limit = len(self)

            leaves = []

            # non empty non-leaf case
            # Here we want to collect up to limit number of leafs
            for subtree in self.subtrees:

                new_leaves = subtree._get_leaves_greedy(limit)
                leaves = self._merge_leafs(leaves, new_leaves)
                # Reduce limit by number of leaves collected
                limit -= len(new_leaves)

                if limit <= 0:
                    break

            return leaves

    def _merge_leafs(self, old_leaves, new_leaves):
        """ Merges two list of already sorted leaves together and returns a new
        sorted list of leafs contaning all of the
        elements of old and new_leafs
        """
        # Based of a portion of merge sort. Algorithm putting two sorted
        # list together.
        a = 0
        b = 0
        merged_leaves = []
        while a < len(old_leaves) and b < len(new_leaves):
            if old_leaves[a][1] >= new_leaves[b][1]:
                merged_leaves.append(old_leaves[a])
                a += 1
            else:
                merged_leaves.append(new_leaves[b])
                b += 1
        while a < len(old_leaves):
            merged_leaves.append(old_leaves[a])
            a += 1
        while b < len(new_leaves):
            merged_leaves.append(new_leaves[b])
            b += 1

        return merged_leaves


################################################################################
# CompressedPrefixTree (Task 6)
################################################################################
class CompressedPrefixTree(Autocompleter):
    """A compressed prefix tree implementation.

    While this class has the same public interface as SimplePrefixTree,
    (including the initializer!) this version follows the implementation
    described on Task 6 of the assignment handout, which reduces the number of
    tree objects used to store values in the tree.

    === Attributes ===
    value:
        The value stored at the root of this prefix tree, or [] if this
        prefix tree is empty.
    weight:
        The weight of this prefix tree. If this tree is a leaf, this attribute
        stores the weight of the value stored in the leaf. If this tree is
        not a leaf and non-empty, this attribute stores the *aggregate weight*
        of the leaf weights in this tree.
    subtrees:
        A list of subtrees of this prefix tree.

    === Representation invariants ===
    - self.weight >= 0

    - (EMPTY TREE):
        If self.weight == 0, then self.value == [] and self.subtrees == [].
        This represents an empty simple prefix tree.
    - (LEAF):
        If self.subtrees == [] and self.weight > 0, this tree is a leaf.
        (self.value is a value that was inserted into this tree.)
    - (NON-EMPTY, NON-LEAF):
        If len(self.subtrees) > 0, then self.value is a list (*common prefix*),
        and self.weight > 0 (*aggregate weight*).

    - **NEW**
      This tree does not contain any compressible internal values.
      (See the assignment handout for a definition of "compressible".)

    - self.subtrees does not contain any empty prefix trees.
    - self.subtrees is *sorted* in non-increasing order of their weights.
      (You can break ties any way you like.)
      Note that this applies to both leaves and non-leaf subtrees:
      both can appear in the same self.subtrees list, and both have a `weight`
      attribute.
    """
    value: Optional[Any]
    weight: float
    subtrees: List[CompressedPrefixTree]


if __name__ == '__main__':
    # TODO REMOVE DOCTEST import
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config={
        'max-nested-blocks': 4
    })
