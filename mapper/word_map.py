from nltk.corpus import wordnet as wn
from graphviz import Digraph


class WordNode:
    def __init__(self, word, level, depth):
        self.word = word
        self.level = level
        self.depth = depth

        self.hypernyms = None
        self.hyponyms = None

    def extract(self):
        synset = wn.synsets(self.word)[0]

        if self.level >= 0:
            hypernyms = [hn.lemma_names()[0] for
                         hn in synset.hypernyms()]
            hypernyms = [WordNode(hn, self.level+1, self.depth-1) for
                         hn in hypernyms]

            if self.depth > 1:
                for hn in hypernyms:
                    hn.extract()

            self.hypernyms = hypernyms

        if self.level <= 0:
            hyponyms = [hn.lemma_names()[0] for
                        hn in synset.hyponyms()]
            hyponyms = [WordNode(hn, self.level-1, self.depth-1) for
                        hn in hyponyms]

            if self.depth > 1:
                for hn in hyponyms:
                    hn.extract()

            self.hyponyms = hyponyms


class WordMap:
    def __init__(self, depth=1):
        self.node = None
        self.depth = depth

    def fit_word(self, word):
        node = WordNode(word, 0, self.depth)
        node.extract()
        self.node = node

    def extract_graph(self):
        words = [self.node.word]
        graph = []

        stack = [self.node]

        while len(stack) > 0:
            wn = stack.pop(-1)
            loc = len(words)-1

            if wn.hypernyms is not None:
                for hn in wn.hypernyms:
                    stack.append(hn)
                    words.append(hn.word)
                    graph.append((len(words)-1, loc))

            if wn.hyponyms is not None:
                for hn in wn.hyponyms:
                    stack.append(hn)
                    words.append(hn.word)
                    graph.append((loc, len(words)-1))

        return words, graph

    def save_image(self):
        words, graph = self.extract_graph()

        dot = Digraph()

        for indx, word in enumerate(words):
            dot.node(str(indx), word)

        for edge in graph:
            dot.edge(str(edge[0]), str(edge[1]))

        dot.render('output/graph.gv', view=True)


def save_word_map(word, depth=2):
    wm = WordMap()
    wm.fit_word(word)
    wm.save_image()
