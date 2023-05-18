from models import DataLoader, Tokenizer, SequenceTagger, MaltParser, GrammarRelation, LogicalForm, ProceduralSem, QueryTransform, QueryDB
import os

if __name__ == "__main__":
    queries = DataLoader()
    queries.load('input/queries.txt')
    tokenizer = Tokenizer()
    seqtag = SequenceTagger()
    querydb = QueryDB('input/nlp.db')
    ls = []
    if not os.path.exists('test_output'):
        os.makedirs('test_output')
        dirs = ['maltparser', 'grammar_relation', 'logical_form',
                'procedure_semantic', 'sql_query', 'query_res']
        curr_path = os.getcwd()
        os.chdir("test_output")
        for dir in dirs:
            os.makedirs(f'{dir}')
        os.chdir(curr_path)
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
        with open(f'test_output/maltparser/out_{i}.txt', 'w+') as file:
            for g in graphs:
                file.write(f"{g}\n")
        grammar_rel = GrammarRelation(graphs)
        with open(f'test_output/grammar_relation/out_{i}.txt', 'w+') as file:
            file.write(f"{grammar_rel}")
        logical_form = LogicalForm(grammar_rel)
        with open(f'test_output/logical_form/out_{i}.txt', 'w+') as file:
            file.write(f"{sent}\n")
            file.write(f"{logical_form}")
        proc_sem = ProceduralSem(logical_form)
        with open(f'test_output/procedure_semantic/out_{i}.txt', 'w+') as file:
            file.write(f"{sent}\n")
            file.write(f"{proc_sem}")
        query = QueryTransform(proc_sem.easy_query())
        with open(f'test_output/sql_query/out_{i}.txt', 'w+') as file:
            file.write(f"{sent}\n")
            file.write(f"{query}")
        res = querydb.query_db(query)
        with open(f'test_output/query_res/out_{i}.txt', 'w+') as file:
            file.write(f'{sent}\n')
            file.write(f"{res}")

    querydb.close()
