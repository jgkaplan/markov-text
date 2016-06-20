import markov

creator = markov.Markov('jeeves.txt', 2)
for i in xrange(5):
    print creator.make_text(5)
    print creator.make_sentence()
#print "\n"
#creator.set_gen_number(4)
#print creator.make_text(100)
