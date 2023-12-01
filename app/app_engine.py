class WordsPair:
    def __init__(self, word, translate, count=0):
        self.word = word
        self.translate = [i.strip() for i in translate.split(',')]
        self.count = count
        self.right_answer_count = 0
        self.wrong_answer_count = 0

    def counter(self):
        self.count += 1

    def exam(self):
        pass

    def set_world(self, another_word):
        self.word = another_word

    def set_translate(self):
        pass


class Collection:
    def __init__(self, name):
        self.name = name
