from nltk.corpus import wordnet as wn
from graphviz import Digraph


class WordNode:
    def __init__(self, word=None, synset=None, level=0, depth=3):
        if word is not None:
            self.word = word
        else:
            self.word = synset.lemma_names()[0]

        self.synset = synset
        self.level = level
        self.depth = depth

        self.hypernyms = None
        self.hyponyms = None

    def extract(self):
        if self.synset is None:
            synset = wn.synsets(self.word)[0]
        else:
            synset = self.synset

        if self.level >= 0:
            hypernyms = [WordNode(synset=hn,
                                  level=self.level+1,
                                  depth=self.depth-1) for
                         hn in synset.hypernyms()]

            if self.depth > 1:
                for hn in hypernyms:
                    hn.extract()

            self.hypernyms = hypernyms

        if self.level <= 0:
            hyponyms = [WordNode(synset=hn,
                                 level=self.level-1,
                                 depth=self.depth-1) for
                        hn in synset.hyponyms()]

            if self.depth > 1:
                for hn in hyponyms:
                    hn.extract()

            self.hyponyms = hyponyms


class WordMap:
    def __init__(self, depth=1):
        self.node = None
        self.depth = depth

    def fit_word(self, word):
        node = WordNode(word=word, level=0, depth=self.depth)
        node.extract()
        self.node = node

    def extract_graph(self):
        words = [self.node.word]
        graph = []

        stack = [(None, None, self.node)]

        while len(stack) > 0:
            hpo, hpr, wn = stack.pop(-1)
            words.append(wn.word)
            loc = len(words)-1

            if hpr is not None:
                graph.append((hpr, loc))

            if hpo is not None:
                graph.append((loc, hpo))

            if wn.hypernyms is not None:
                for hn in wn.hypernyms:
                    stack.append((loc, None, hn))

            if wn.hyponyms is not None:
                for hn in wn.hyponyms:
                    stack.append((None, loc, hn))

        return words, graph

    def save_image(self):
        words, graph = self.extract_graph()

        dot = Digraph()
        dot.format = 'png'

        for indx, word in enumerate(words):
            dot.node(str(indx), word)

        for edge in graph:
            dot.edge(str(edge[0]), str(edge[1]))

        dot.render('test-output/graph.gv')


def save_word_map(word, depth=2):
    wm = WordMap(depth=depth)
    wm.fit_word(word)
    wm.save_image()
