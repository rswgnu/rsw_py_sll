# rsw_py_sll
A Python3 MutableSequence, polymorphic singly linked list (for educational purposes) offering:

* creation with any number of items: `s1 = Sll(0, 1, 2), s2 = Sll()`

* numeric indexing of list items (0 or greater): `s[0]`

* iteration: `for item in s1`

* containment for finding if an item is in the list: `if 2 in s1: print("found it")`

* concatenation with '+': `s1 + s2`

* duplication and extending with '*': `s1 * 2` returns `Sll[0, 1, 2, 0, 1, 2]`

* prepending and extending by any number of items:<br>
    `s1.prepend(3, 4)` returns `Sll[3, 4, 0, 1, 2]`<br>
    `s1.extend(5, 6)` returns `Sll[3, 4, 0, 1, 2, 5, 6]`<br>
    `s2.extend(3, 4)` returns `Sll[3, 4]`

* appending single items: `s2.append(5)` returns `Sll[3, 4, 5]`

* finding an item and returning its sublist: `s2.find(4)` returns `Sll[4, 5]`

* counting item occurrences: `s2.count(3)` returns `1`

* list or item deletion via 'del': `del s1[2]` or `del s1`

* access to last item or sublist:<br>
    `s2.last()` returns `5`<br>
    `s2.last_sublist()` returns `Sll[5]`

* conversion to a standard Python list of items: `s2.items()` returns `[3, 4, 5]`

* a full set of self-tests: `Sll.test()`.
