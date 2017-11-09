#!/usr/bin/python3
#
# SUMMARY:      A Python3 MutableSequence, polymorphic singly linked list (for educational purposes) 
# USAGE:        'sll.py' to run self-tests; 'import sll; lst = Sll(*items)' to create an Sll
#
# AUTHOR:       Bob Weiner
#
# LICENSE:      MIT License
# COPYRIGHT:    Copyright (C) 2017  Bob Weiner
#
# LAST-MOD:      9-Nov-17 at 08:40:55 by Bob Weiner
#
# DESCRIPTION:  
"""
There are many existing examples of implementing singly-linked lists
in Python but none of the others demonstrate standard Pythonic datatype
capabilities as described below.

Sll: A Python3 MutableSequence, polymorphic singly linked list
     (for educational purposes) offering:

        creation with any number of items: s1 = Sll(0, 1, 2); s2 = Sll()

        numeric indexing of list items (0 or greater): s[0]

        iteration: for item in s1

        containment for finding if an item is in the list: if 2 in s1: print("found it")

        concatenation with '+': s1 + s2

        duplication and extending with '*': s1 * 2 returns Sll[0, 1, 2, 0, 1, 2]

        prepending and extending by any number of items:
          s1.prepend(3, 4) returns Sll[3, 4, 0, 1, 2]
          s1.extend(5, 6)  returns Sll[3, 4, 0, 1, 2, 5, 6]
          s2.extend(3, 4)  returns Sll[3, 4]

        appending single items: s2.append(5) returns Sll[3, 4, 5]

        finding an item and returning its sublist: s2.find(4) returns Sll[4, 5]

        counting item occurrences: s2.count(3) returns 1

        list or item deletion via 'del': del s1[2] or del s1

        access to last item or sublist:
          s2.last() returns 5
          s2.last_sublist() returns Sll[5]

        conversion to a standard Python list of items: s2.items() returns [3, 4, 5]

        a full set of self-tests: Sll.test().
"""
# DESCRIP-END.

# Consider using __slots__ to reduce memory usage.
# Consider adding attr to store last sublist for quick appending performance.

from collections import MutableSequence
from numbers import Integral
class Sll(MutableSequence):
    "An Iterable, Singly Linked List"

    def __init__(self, *items):
        "Create a new singly-linked list (Sll) containing 'items'."
        self.index = 0
        if items: self = self.extend(*items)

    def __add__(self, sll):
        "Append 'sll' to self."
        n = self.last_sublist()
        if not n.is_empty():
            n.rest = sll
        return self

    def __mul__(self, num):
        """
        Prepend list items to itself 'num' - 1 times.  Return empty list if 'num' is 0.
        Raise TypeError if 'num' is non-integral or less than 0.
        """
        if isinstance(num, Integral) and num >= 0:
            if num == 0:
                return Sll()
            else:
                n = self; items = self.items()
                for i in range(num - 1):
                    n = n.prepend(*items)
                return n
        else:
            raise TypeError("Multiplier must be a non-negative integer but is: %s" % num)

    def __contains__(self, item):
        return item in self.items()

    def __delitem__(self, i):
        try:
            n = self; l = len(self)
            while i > 1:
                n = n.rest; i -= 1
            if i == 0:
                if l == 0:
                    pass
                elif l == 1:
                    del self.item
                    del self.rest
                else:
                    self.item = self.rest.item
                    self.rest = self.rest.rest
                    n = self
            elif i == 1:
                n.rest = n.rest.rest if n.rest != None else None
            else:
                raise IndexError
            return n
        except:
            raise  IndexError

    def __eq__(self, sll):
        return type(self) is type(sll) and self.items() == sll.items()

    def find(self, item):
        "If 'item' is in the list, return its sublist, else return None."
        n = self
        while n and not n.is_empty():
            if n.item == item:
                return n
            else:
                n = n.rest

    def __getitem__(self, i):
        n = self
        while i > 0:
            n = n.rest; i -= 1
        if i == 0:
            return n.item 
        else:
            raise IndexError

    def sublist(self, i):
        "Return the sublist of this list starting at index 'i' (starts at 0 for whole list)."
        n = self
        while i > 0:
            n = n.rest; i -= 1
        if i == 0:
            return n
        else:
            raise IndexError

    def __setitem__(self, i, item):
        n = self
        while i > 0:
            n = n.rest; i -= 1
        if i == 0:
            n.item = item
        else:
            raise IndexError
    insert = __setitem__

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index > len(self) - 1 or self.is_empty() or self.sublist(self.index) == None:
            self.index = 0
            raise StopIteration
        else:
            self.index += 1 
            return self[self.index - 1]

    def items(self):
        "Return a Python list of the items in this singly linked list."
        n = list()
        while self and self.item != None:
            n.append(self.item); self = self.rest
        return n

    def __len__(self):
        l = 0; n = self
        while hasattr(n, 'item') and n.item != None:
            l += 1; n = n.rest
        return l

    def append(self, item):
        "Append a single item at list end."
        return self.extend(item)

    def extend(self, *items):
        "Append all items at list end."
        if items:
            n = self
            if n.is_empty():
                n.item = items[0]; n.rest = None; items = items[1:]
            while n.rest != None:
                n = n.rest
            for item in items:
                n.rest = Sll(); n = n.rest; n.item = item; n.rest = None
        return self

    def prepend(self, *items):
        "Add all items at the start of list."
        h = n = self
        for item in reversed(items):
            h = Sll(); h.item = item; h.rest = n; n = h
        return h

    def reverse(self):
        """
        In-place, mutating reversal of a list.
        Use reversed(<Sll>) to generate a list of reversed items without mutation.
        """
        n = r = self
        if r and not r.is_empty():
           r = r.rest
           n.rest = None
           while r and not r.is_empty():
               t = r.rest; r.rest = n; n = r; r = t
        return n

    def is_empty(self):
        return not hasattr(self, 'item')

    def last(self):
        "Return last item in the list or None."
        n = self
        while n and not n.is_empty() and n.item != None and n.rest != None:
            n = n.rest
        return n.item if n and n.item != None else None

    def last_sublist(self):
        "Return last sublist in the list or None."
        n = self
        while n and not n.is_empty() and n.rest != None:
            n = n.rest
        return n if not n.is_empty() else None

    def __repr__(self):
        return 'Sll[' + ', '.join(map(repr, self.items())) + ']'
    __str__ = __repr__

    def test():
        # Make these Slls global so can be used after test() runs.
        global a, b
        a = Sll(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        b = Sll()
        assert not a.is_empty()
        assert b.is_empty()

        assert 7 in a
        assert 12 not in a
        assert 7 not in b

        assert len(a)==10, "len(a) = %d; a = %s" % (len(a), a)
        assert len(b)==0, "len(b) = %d; b = %s" % (len(b), b)

        assert a[0]==0 
        assert a[3]==3
        assert a[9]==9

        b.extend(10, 11, 12)
        assert b.items() == [10, 11, 12]
        assert 12 in b
        assert b.last() == 12

        assert [x for x in b] == [10, 11, 12]

        del b[1]; assert len(b)==2
        assert b.items() == [10, 12], "b.items() = %s" % b.items()

        b[1]=13; assert b.items() == [10, 13]

        b.append(14); assert b.items() == [10, 13, 14]

        assert (b * 0).items() == [], "b*0.items() = %s" % (b*0).items()
        assert (b * 1).items() == [10, 13, 14], "b*1.items() = %s" % (b*1).items()
        c = b * 2
        assert c.items() == [10, 13, 14, 10, 13, 14], "b*2.items() = %s" % c.items()
        assert b.count(9) == 0, "b.count(9) = %s" % b.count(9)
        assert b.count(10) == 1, "b.count(10) = %s" % b.count(10)
        assert c.count(10) == 2, "c.count(10) = %s" % c.count(10)
        c = b * 3
        assert c.items() == [10, 13, 14, 10, 13, 14, 10, 13, 14], "b*3.items() = %s" % c.items()
        c.count(14) == 3, "b*3.count(14) = %s" % c.count(14)

        b = b.prepend(8, 9); assert b.items() == [8, 9, 10, 13, 14], "b.items() = %s" % b.items()
        assert b.last_sublist() == Sll(14), "b.last_sublist() = %s; b.items = %s" % (b.last_sublist(), b.items())

        assert b.find(13) == Sll(13, 14), "b.find(13) = %s" % b.find(13)
        assert b.find(0) == None, "b.find(0) = %s" % b.find(0)
        assert b.find('heart') == None, "b.find('heart') = %s" % b.find('heart')

        c = Sll(15)
        b = b + c; assert len(b)==6

        del b[0]; assert b.items() == [9, 10, 13, 14, 15], "b.items() = %s" % b.items()
        del b[4]; assert b.items() == [9, 10, 13, 14], "b.items() = %s" % b.items()

        assert next(b) == 9
        assert next(b) == 10
        assert next(b) == 13
        assert next(b) == 14

        assert b.reverse() == Sll(14, 13, 10, 9), "b.reverse() = %s" % b.reverse()
        assert c.reverse() == Sll(15), "c.reverse() = %s" % c.reverse()
        d = Sll()
        assert d.reverse() == Sll(), "d.reverse() = %s" % d.reverse()

        del b; assert 'b' not in dir()

        return True

if __name__ == '__main__':
    Sll.test()
