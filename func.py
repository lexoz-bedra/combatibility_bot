from random import randint
from database import connect


def get_merge():
    return randint(20, 100)


def conf_bot(name1, name2):
    merge = get_merge()
    data = connect(name1, name2, merge)
    return data


class Consts:
    name1, name2 = 'вероника', 'максим'

    def __init__(self):
        self.merge = conf_bot(self.name1, self.name2)

    def set_your_name(self, name):
        self.name1 = name.lower()

    def set_partner_name(self, name):
        self.name2 = name.lower()
