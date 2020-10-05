import abc


class Group:
    pass


def init_options(cls):
    _options = []
    for group in cls.groups:
        _options += group.options
    return _options


def init_dis(cls):
    _dis = TupleDict()
    for group in cls.groups:
        for (k, v) in group.dis.items():
            _dis.update({k: cls.group_dis[(group, group)] + v})
    for i in range(len(cls.groups)):
        for j in range(i + 1, len(cls.groups)):
            for m in cls.groups[i].options:
                for n in cls.groups[j].options:
                    _dis[(m, n)] = cls.group_dis[(
                        cls.groups[i], cls.groups[j])]
    return _dis


def format(obj, cls):
    return cls(obj[cls.title])


class TupleDict(dict):  # treat key values (i, j) and (j, i) as equivalent
    def __init__(self, dict={}):
        for (tuple, value) in dict.items():
            (i, j) = tuple
            super().__setitem__((i, j), value)
            super().__setitem__((j, i), value)

    def __setitem__(self, tuple, value):
        (i, j) = tuple
        super().__setitem__((i, j), value)
        super().__setitem__((j, i), value)

    def __repr__(self):
        return f"{type(self).__name__}({super().__repr__()})"


class Question:
    __metaclass__ = abc.ABCMeta
    title = ""

    @ abc.abstractmethod
    def to_obj(self):
        pass


class MultipleChoice(Question):
    __metaclass__ = abc.ABCMeta
    options = []
    dis = TupleDict()


class SingleSelection(MultipleChoice):
    __metaclass__ = abc.ABCMeta

    def __init__(self, str):
        self.answer = str

    @ staticmethod
    def distance(ss1, ss2):
        return ss1.dis[(ss1.answer, ss2.answer)]

    def to_obj(self):
        return self.answer


class MultipleSelection(MultipleChoice):
    __metaclass__ = abc.ABCMeta
    alpha = 1.6
    beta = 0.3

    def __init__(self, str):
        self.answer = set([s.strip() for s in str.split(',')])

    @ staticmethod
    def distance(ms1, ms2):
        inter = ms1.answer.intersection(ms2.answer)
        inter_sum = 0
        for i in inter:
            for j in inter:
                if i == j:
                    continue
                if(i in ms1.answer and j in ms2.answer or
                   i in ms2.answer and j in ms1.answer):
                    inter_sum += ms1.dis[(i, j)]

        diff = ms1.answer.difference(ms2.answer)
        diff_sum = 0
        for i in diff:
            for j in diff:
                if i == j:
                    continue
                if(i in ms1.answer and j in ms2.answer or
                   i in ms2.answer and j in ms1.answer):
                    diff_sum += ms1.dis[(i, j)]
        # TODO

        return inter_sum + diff_sum

    def to_obj(self):
        return list(self.answer)
