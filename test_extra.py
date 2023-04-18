from models import DataLoader, Tokenizer, SequenceTagger, MaltParser
from collections import Counter

if __name__ == "__main__":
    queries = DataLoader()
    queries.load('input/extra.txt')
    tokenizer = Tokenizer()
    seqtag = SequenceTagger()
    ls = []
    for i in range(len(queries)):
        sent = queries[i]
        # tokenizer word
        tokens = tokenizer.tokenize(sent)
        print(tokens)
        # print(tokens)
        # sequence tagging on tokens
        # toks = seqtag(tokens)
        # parser = MaltParser(toks)
        # graphs = parser()
        # for g in graphs:
        #     print(g)
        break
        # print(toks)
        # ls.extend(toks)

    # tags = []
    # for t in ls:
    #     tags.append(t.tag)
    # for t in set(tags):
    #     print(t)
