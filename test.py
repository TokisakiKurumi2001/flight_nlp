from models import DataLoader, Tokenizer, SequenceTagger, MaltParser, GrammarRelation, LogicalForm, ProceduralSem
from collections import Counter

if __name__ == "__main__":
    queries = DataLoader()
    queries.load('input/queries.txt')
    tokenizer = Tokenizer()
    seqtag = SequenceTagger()
    ls = []
    for i in range(len(queries)):
        # if i in [0]:
        #     continue
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
        # with open(f'output/grammar_relation/out_{i}.txt', 'w+') as file:
        #     file.write(f"{grammar_rel}")
        logical_form = LogicalForm(grammar_rel)
        # with open(f'output/logical_form/out_{i}.txt', 'w+') as file:
        #     file.write(f"{sent}\n")
        #     file.write(f"{logical_form}")
        proc_sem = ProceduralSem(logical_form)
        with open(f'output/procedure_semantic/out_{i}.txt', 'w+') as file:
            file.write(f"{sent}\n")
            file.write(f"{proc_sem}")
        print(sent)
        print(proc_sem)
        # break
