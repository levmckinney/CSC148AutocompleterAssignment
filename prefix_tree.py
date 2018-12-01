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
    _weight_type: str
    # _len: is the number of values currently stored in the tree
    _len: int
    # _summed_weight: this is the sum of the weights inserted into self
    # regardless of the value of _weight_type.
    _summed_weight: float
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
        >>> spt.insert('hello', 7, ['h','e','l','l','o'])
        >>> print(spt)
        [] (27)
          ['h'] (27)
            ['h', 'e'] (27)
              ['h', 'e', 'l'] (27)
                ['h', 'e', 'l', 'l'] (27)
                  ['h', 'e', 'l', 'l', 'o'] (27)
                    hello (27)
        <BLANKLINE>
        """
        self._insert_helper(value, weight, prefix)

    def _insert_helper(self, value: Any, weight: float, prefix: List) -> bool:
        """This helps to insert the given value into this Autocompleter.

        A helper was necessary since we needed to recursively edit the length
        attributes of each tree, but needed to return a boolean that determines
        whether we are adding a new_leaf. If True, this means the length
        of each tree it falls under must be increased. If False, we know an
        attempt was made to insert a previously added value. Consequently, only
        weights are increased.
        """

        depth = len(self.value)

        new_leaf = False

        if depth == len(prefix):
            # We have reached the end of the prefix and will add a leaf or
            # add our weight to an existing one.
            leaf_index = self._find_leaf_with_value(value)
            if leaf_index is not None:
                self.subtrees[leaf_index].weight += weight
                self.subtrees[leaf_index]._summed_weight += weight
                self._fix_subtree_at_index(leaf_index)
                new_leaf = False
            else:
                subtree = SimplePrefixTree(self._weight_type)
                subtree.value = value
                subtree.weight = weight
                subtree._summed_weight = weight
                subtree._len = 1
                self._add_subtree(subtree)
                new_leaf = True

        else:
            path_index = self._find_non_leaf_with_value(prefix[:(depth + 1)])

            if path_index is None:  # depth < len(prefix)
                # No prefix exists in the subtree so we add a new subtree.
                subtree = SimplePrefixTree(self._weight_type)
                subtree.value = prefix[:(depth + 1)]
                new_leaf = subtree._insert_helper(value, weight, prefix)
                self._add_subtree(subtree)

            else:
                # A subtree already exists so we go down it.
                new_leaf = self.subtrees[path_index]._insert_helper(value,
                                                                    weight,
                                                                    prefix)
                self._fix_subtree_at_index(path_index)

        if new_leaf:
            self._len += 1

        self._calculate_weight()

        return new_leaf

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
            subtree_index = self._find_non_leaf_with_value(prefix[:(depth + 1)])

            if subtree_index is not None:
                subtree = self.subtrees[subtree_index]
                num_removed = subtree._remove_helper(prefix)

                self._len -= num_removed

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
            else:
                return 0

    def _calculate_weight(self) -> None:
        """This recalculates the weight for this tree based on the weight of its
        subtrees
        Note: This method is not recursive.
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

    def _find_non_leaf_with_value(self, value: Any) -> Optional[int]:
        """ Finds a none leaf subtree with <value> and returns its index.
        If no subtree can be found it returns None"""
        for i in range(0, len(self.subtrees)):
            subtree = self.subtrees[i]
            if subtree.value == value and not subtree.is_leaf():
                return i
        return None

    def _find_leaf_with_value(self, value: Any) -> Optional[int]:
        """ Finds a leaf subtree with <value> and returns its index.
        If no subtree can be found it returns None"""
        for i in range(0, len(self.subtrees)):
            subtree = self.subtrees[i]
            if subtree.value == value and subtree.is_leaf():
                return i
        return None

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
                index -= 1
            elif (index < len(self.subtrees) - 1
                  and subtree.weight < self.subtrees[index + 1].weight):
                # Switch with index to right
                self.subtrees[index + 1], self.subtrees[index] = \
                    subtree, self.subtrees[index + 1]
                index += 1
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
        >>> spt.insert('he', 109, ['h', 'e'])
        >>> spt.autocomplete(['h', 'e', 'l'])
        [('hello', 80), ('help', 10)]
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

    def _get_leaves_greedy(self, limit: Optional[int]) -> \
            (List[Tuple[Any, float]]):
        """ The return value is a list with a tuple (value, weight)
         for each leaf. This is ordered by non-increasing weight.
         The list will contain all the leafs found in a greedy search up to
         limit or all the leafs if limit is None.
        """

        if self.is_empty():
            return []
        elif self.is_leaf():
            # Reached leaf node
            return [(self.value, self.weight)]
        else:
            if limit is None:
                limit = len(self)

            leaves = []

            # non empty non-leaf case
            # Here we want to collect up to limit number of leafs
            for subtree in self.subtrees:

                if limit <= 0:
                    break

                new_leaves = subtree._get_leaves_greedy(limit)
                leaves = _merge_leafs(leaves, new_leaves)
                # Reduce limit by number of leaves collected
                limit -= len(new_leaves)

            return leaves


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

    # === Private Instance Attributes ===
    # _weight_type: A string that specifies whether the weight of the
    # tree will be calculated as the 'sum' or the 'average' of the weights of
    # each leaf value in the tree.
    _weight_type: bool
    # _len: is the number of values currently stored in the tree
    _len: int
    # _summed_weight: this is the sum of the weights inserted into self
    # regardless of the value of _weight_type.
    _summed_weight: float
    # === Private Representation invariants ===
    # All trees have the same _weight_type as their subtrees.
    # _len >= 0
    # _len is always the number of leaf nodes(i.e. values) in the tree.

    def __init__(self, weight_type: str) -> None:
        """Initialize an empty compressed prefix tree.

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
        """Return whether this compressed prefix tree is empty."""
        return self.weight == 0.0

    def is_leaf(self) -> bool:
        """Return whether this compressed prefix tree is a leaf."""
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

        >>> spt = CompressedPrefixTree('sum')
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
        """
        # The empty prefix case
        self._insert_helper(value, weight, prefix, -1)

    def _insert_helper(self, value: Any, weight: float, prefix: List,
                       len_parent: int) -> bool:
        """This helps to insert the given value into this Autocompleter.

        Same as insert but len parent is the leangth of the parent of this
        subtree.

        Return true if value and prefix can be inserted with len_parent.
        """

        if self.value == prefix:  # Same prefix cases
            # We know that a leaf already exists or a leaf should exist here
            # with value <value>.

            for i in range(len(self.subtrees)):
                subtree = self.subtrees[i]
                if subtree.is_leaf() and subtree.value == value:

                    subtree.weight += weight
                    subtree._summed_weight += weight
                    self._calculate_len_weight()
                    # do not need to increase len since nothing was added
                    self._fix_subtree_at_index(i)
                    return True

            # We did not find a subtree to add weight to so we can add a leaf

            self._add_leaf(value, weight)
            self._calculate_len_weight()
            return True

        elif self.is_empty():  # Empty Tree case
            self.value = prefix
            # Goes to same prefix case
            return self._insert_helper(value, weight, prefix, len(self.value))

        elif _is_prefix(self.value, prefix):  # value is prefix case
            # This is the ['a', 'b'] in the tree is prefix of
            # ['a', 'b', 'c'] prefix.
            for i in range(len(self.subtrees)):
                subtree = self.subtrees[i]
                # We call insert helper on non-leaf subtrees and clean up if
                # we find one
                if (not subtree.is_leaf() and
                        subtree._insert_helper(value, weight, prefix,
                                               len(self.value))):

                    self._fix_subtree_at_index(i)
                    self._calculate_len_weight()
                    return True

            # We have failed to find a subtree to go down so we dump the leaf
            # here
            self._add_depth_2_subtree(value, prefix,
                                      weight)
            self._calculate_len_weight()
            return True
        else:
            shared_prefix = _share_prefix(prefix, self.value)

            if len(shared_prefix) > len_parent: # novel prefix case:
                # create a copy of self.
                copy_self = self._copy()

                # Give self correct value
                self.subtrees = []
                self.value = shared_prefix

                self.subtrees.append(copy_self)

                self._insert_helper(value, weight, prefix, len(self.value))

                return True
            else:  # We can't insert here
                return False

    def _copy(self) -> CompressedPrefixTree:
        """Make a copy of self"""

        copy_self = CompressedPrefixTree(self._weight_type)
        copy_self.value = self.value
        copy_self.weight = self.weight
        copy_self._len = self._len
        copy_self._summed_weight = self._summed_weight
        copy_self.subtrees = self.subtrees
        return copy_self

    def _add_leaf(self, value: any, weight: float) -> None:
        """Creates a leaf and inserts it in the correct position in subtrees
        By weight

        DOSE NOT RECOMPUTE self._len, self.weight, and self._sumed_weight
        """
        leaf = CompressedPrefixTree(self._weight_type)
        leaf.value = value
        leaf._len = 1
        leaf.weight = weight
        leaf._summed_weight = weight
        self._add_subtree(leaf)

    def _add_depth_2_subtree(self, value: Any, prefix: list, weight: float)\
            -> None:
        """Adds a subtree with only the prefix and the leaf in correct position
        by weight.

        DOSE NOT RECOMPUTE self._len, self.weight, and self._sumed_weight
        """
        leaf = CompressedPrefixTree(self)
        leaf._len = 1
        leaf.value = value
        leaf._summed_weight = weight
        # no need to use _calculate_weight() if len == 1
        leaf.weight = weight
        prefix_tree = CompressedPrefixTree(self._weight_type)
        prefix_tree.value = prefix
        prefix_tree.subtrees.append(leaf)
        prefix_tree._len = 1
        prefix_tree._summed_weight += weight
        prefix_tree._calculate_len_weight()
        self._add_subtree(prefix_tree)

    def _add_subtree(self, subtree: CompressedPrefixTree) -> None:
        """ Place a subtree into self.subtrees in the correct position base on
        weight.

        DOSE NOT RECOMPUTE self._len, self.weight, and self._sumed_weight
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

    def _calculate_len_weight(self) -> None:
        """This recalculates the weight and len for this tree based on the
        weight of its and lens of its subtrees.
        Note: This method is not recursive.
        """
        self._len = sum([len(subtree) for subtree in self.subtrees])
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
                index -= 1
            elif (index < len(self.subtrees) - 1
                  and subtree.weight < self.subtrees[index + 1].weight):
                # Switch with index to right
                self.subtrees[index + 1], self.subtrees[index] = \
                    subtree, self.subtrees[index + 1]
                index += 1
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

        >>> cpt = CompressedPrefixTree('sum')
        >>> cpt.insert('swell', 75, ['s', 'w', 'e', 'l', 'l'])
        >>> cpt.insert('sweet', 50, ['s', 'w', 'e', 'e', 't'])
        >>> cpt.insert('swat', 51, ['s', 'w', 'a', 't'])
        >>> cpt.insert('swap', 76, ['s', 'w', 'a', 'p'])
        >>> print(cpt)
        ['s', 'w'] (252)
          ['s', 'w', 'a'] (127)
            ['s', 'w', 'a', 'p'] (76)
              swap (76)
            ['s', 'w', 'a', 't'] (51)
              swat (51)
          ['s', 'w', 'e'] (125)
            ['s', 'w', 'e', 'l', 'l'] (75)
              swell (75)
            ['s', 'w', 'e', 'e', 't'] (50)
              sweet (50)
        <BLANKLINE>
        >>> cpt.autocomplete(['s', 'w', 'a'])
        [('swap', 76), ('swat', 51)]
        """

        if self.is_leaf():
            return []
        elif _is_prefix(prefix, self.value):

            return self._get_leaves_greedy(limit)

        elif _is_prefix(self.value, prefix):
            for subtree in self.subtrees:
                if not subtree.is_leaf():
                    auto = subtree.autocomplete(prefix, limit)
                    if auto != []:
                        return auto
            return []
        else:
            return []

    def _get_leaves_greedy(self, limit: Optional[int]) -> \
            (List[Tuple[Any, float]]):
        """ The return value is a list with a tuple (value, weight)
         for each leaf. This is ordered by non-increasing weight.
         The list will contain all the leafs found in a greedy search up to
         limit or all the leafs if limit is None.
        """

        if self.is_empty():
            return []
        elif self.is_leaf():
            # Reached leaf node
            return [(self.value, self.weight)]
        else:
            if limit is None:
                limit = len(self)

            leaves = []

            # non empty non-leaf case
            # Here we want to collect up to limit number of leafs
            for subtree in self.subtrees:

                if limit <= 0:
                    break

                new_leaves = subtree._get_leaves_greedy(limit)
                leaves = _merge_leafs(leaves, new_leaves)
                # Reduce limit by number of leaves collected
                limit -= len(new_leaves)

            return leaves

    def remove(self, prefix: List) -> None:
        """Remove all values that match the given prefix."""
        self._remove_helper(prefix)

    def _remove_helper(self, prefix: List) -> bool:
        """Remove all values that match the given prefix. Returns true if
        successfully removed prefix.
        """
        if prefix == []:
            self._make_empty()
            return True
        elif self.is_leaf():
            return False
        elif _is_prefix(prefix, self.value):
            self._make_empty()
            return True
        elif _is_prefix(self.value, prefix):
            for i in range(len(self.subtrees)):
                subtree = self.subtrees[i]
                if subtree._remove_helper(prefix):
                    if subtree.is_empty():
                        self.subtrees.remove(subtree)
                        break

            self._calculate_len_weight()
            if self.is_empty():
                self._make_empty()
                return True

            elif len(self.subtrees) == 1 \
                and not self.subtrees[0].is_leaf():
                # Promote good z_subtree to replace subtree
                z_subtree = self.subtrees[0]
                self.value = z_subtree.value
                self._len = z_subtree._len
                self.weight = z_subtree.weight
                self._summed_weight = z_subtree._summed_weight
                self.subtrees = z_subtree.subtrees
                return True

            # self is an incompressible subtree
            return True
        return False

    def _make_empty(self) -> None:
        """Make the self an empty subtree"""
        self.weight = 0
        self._summed_weight = 0
        self._len = 0
        self.subtrees = []
        self.value = []


def _merge_leafs(old_leaves: List, new_leaves: List) -> List:
    """ Merges two list of already sorted leaves together and returns a new
    sorted list of leafs contaning all of the
    elements of old and new_leaves.
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

def _share_prefix(a: list, b: list) -> List:
    """ If there is a common prefix amongst <a> and <b>,.

    >>> _share_prefix([0, 1, 2, 3], [0, 1, 2, 5, 7, 9])
    [0, 1, 2]
    >>> _share_prefix([0, 1, 2, 5, 7, 9], [0, 1, 2, 3])
    [0, 1, 2]
    """
    if len(a) >= len(b):
        long = a
        short = b
    else:
        long = b
        short = a

    for i in range(len(short)):
        if short[i] != long[i]:
            return short[:i]

    return short[:]


def _is_prefix(prefix: Any, items: Any) -> bool:
    """ If <prefix> is a prefix of <items>, return True.
    Otherwise, return False.
    Pre-condition: <prefix> and <items> are iterable
    >>> _is_prefix(['b', 'l', 'a'], ['b', 'l', 'a'])
    True
    >>> _is_prefix(['b', 'l', 'a'], ['b', 'l', 'a', 'c', 'k'])
    True
    >>> _is_prefix(['b', 'l', 'a'], ['b', 'l', 'd'])
    False
    """
    if len(prefix) > len(items):
        return False

    for p, i in zip(prefix, items):
        if p != i:
            return False
    return True

if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    import python_ta
    python_ta.check_all(config={
        'max-nested-blocks': 4
    })
