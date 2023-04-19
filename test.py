from models import DataLoader, Tokenizer, SequenceTagger, MaltParser, GrammarRelation
from collections import Counter

if __name__ == "__main__":
    queries = DataLoader()
    queries.load('input/queries.txt')
    tokenizer = Tokenizer()
    seqtag = SequenceTagger()
    ls = []
    for i in range(len(queries)):
        sent = queries[i]
        # tokenizer word
        tokens = tokenizer.tokenize(sent)
        # print(tokens)
        # sequence tagging on tokens
        toks = seqtag(tokens)
        # print(toks)
        parser = MaltParser(toks)
        graphs = parser()
        # with open(f'output/maltparser/out_{i}.txt', 'w+') as file:
        #     for g in graphs:
        #         file.write(f"{g}\n")
        grammar_rel = GrammarRelation(graphs)
        with open(f'output/grammar_relation/out_{i}.txt', 'w+') as file:
            file.write(f"{grammar_rel}")
