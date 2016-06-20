import random
import string

#When done, account for punctuation as separate things
#ignore capitalization also
#account for endings and beginnings
#generate one sentance (to a .?!) or n words

class Markov(object):
    def __init__(self, source_file, gen_number = 2):
        o = open(source_file, 'r')
        source_lines = o.read()
        o.close()
        self.words = source_lines.split()
        #map(lambda q:"".join(filter(lambda s:s not in string.punctuation, list(q))),source_lines.split())
        self.word_len = len(self.words)
        self.gen_number = gen_number
        self.dict = {}
        self.make_dict()

    def set_gen_number(self, n):
        self.gen_number = n
        self.dict = {}
        self.make_dict()

    def split_words(self):
        if self.word_len < self.gen_number + 1:
            return

        for i in xrange(self.word_len - self.gen_number):
            yield tuple(self.words[i+x] for x in xrange(self.gen_number+1))

    def make_dict(self):
        for group in self.split_words():
            key = group[:-1]
            self.dict.setdefault(key, []).append(group[-1])
    
    def make_text(self, length=25):
        seed = random.randint(0, self.word_len - self.gen_number - 1)
        working_words = [self.words[seed+y] for y in xrange(self.gen_number)]
        created = []
        for i in xrange(length):
            created.append(working_words[0])
            working_words = working_words[1:] + [random.choice(self.dict[tuple(working_words)])]
            if working_words == self.words[-len(working_words):]: #switch to finding a specific thing at the end (EOF type of thing), which I would put in at the end of generation
                break
        created.extend(working_words)
        return ' '.join(created)
#generate using given seed words
if __name__ == '__main__':
    creator = Markov('jeeves.txt', 3)
    print creator.make_text(100)
    print "\n"
    creator.set_gen_number(4)
    print creator.make_text(100)
