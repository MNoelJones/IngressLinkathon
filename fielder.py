class Link(object):
    def __init__(self, p1, p2):
        self._p1 = p1
        self._p2 = p2

    def __str__(self):
        return "LINK {self._p1} -> {self._p2}"


class DLink(Link):
    pass


class Field(object):
    def __init__(self, p1, p2, p3):
        self._p1 = p1
        self._p2 = p2
        self._p3 = p3
        self._portals = [p1, p2, p3]

    def gen(self):
        links = []
        for p1 in self._portals[0:2]:
            for p2 in self._portals[1:]:
                links.append(DLink(p1, p2))
        return And(*links)

    def __str__(self):
        return f"FIELD {self._p1} <-> {self._p2} <-> {self._p3}"


class Portal(object):
    def __init__(self, name=None, location=None):
        self._name = name
        self._location = location

    def __str__(self):
        return f"{self._name}"


class Or(object):
    def __init__(self, first, second):
        self._first = first
        self._second = second

    def __str__(self):
        return "OR\n\t{self._first}\n\t{self._second}"


class _And(object):
    def __init__(self, first, second):
        self._first = first
        self._second = second

    def __str__(self):
        return "AND\n\t{self._first}\n\t{self._second}"


class And(object):
    def __init__(self, *args):
        self._args = args

    def __str__(self):
        return "AND{}".format(
            "".join("\n\t{}".format(item) for item in self._args)
        )
