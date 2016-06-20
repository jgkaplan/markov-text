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
    
    def generate_text(self, caps=False):
        if not caps:
            seed = random.randint(0, self.word_len - self.gen_number - 1)
        else:
            seed = random.choice([index for index, item in enumerate(self.words) if item[0] in string.uppercase])
        working_words = [self.words[seed+y] for y in xrange(self.gen_number)]
        while True: 
            yield working_words[0]
            working_words = working_words[1:] + [random.choice(self.dict[tuple(working_words)])]
            if working_words == self.words[-len(working_words):]: #switch to finding a specific thing at the end (EOF type of thing), which I would put in at the end of generation
                break
        for w in working_words:
            yield w
    
    def make_text(self, length=25):
        counter = 0
        created = []
        for word in self.generate_text():
            created.append(word)
            counter+=1
            if counter == length:
                break
        return ' '.join(created)
    
    def make_sentence(self, number = 1):
        sentences = []
        for i in xrange(number):
            gen = self.generate_text(True)
            sentence = []
            squotes = True
            dquotes = True
            for word in gen:
                sentence.append(word)
                if word[0] == "'":
                    squotes = False
                elif word[0] == '"':
                    dquotes = False

                if word[-1] == "'":
                    squotes = True
                elif word[-1] == '"':
                    dquotes = True

                if word[-1] in ['.','!','?'] and squotes and dquotes:
                    break
            sentences.append(" ".join(sentence))
        return " ".join(sentences)

#generate using given seed words
if __name__ == '__main__':
    creator = Markov('jeeves.txt', 3)
    print creator.make_text(100)
    print "\n"
    creator.set_gen_number(4)
    print creator.make_text(100)
