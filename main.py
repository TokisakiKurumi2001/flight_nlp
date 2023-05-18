from models import DataLoader, Tokenizer, SequenceTagger, MaltParser, GrammarRelation, LogicalForm, ProceduralSem, QueryTransform, QueryDB
import os

if __name__ == "__main__":
    queries = DataLoader()
    queries.load('input/queries.txt')
    tokenizer = Tokenizer()
    seqtag = SequenceTagger()
    querydb = QueryDB('input/nlp.db')
    ls = []

    if not os.path.exists("output"):
        os.makedirs("output")

    query_file_range = "abcdefghijklmnopqrstuvwxyz"
    for i in range(len(queries)):
        out_file = f'output/query_{query_file_range[i]}.txt'
        content = "Query: "

        sent = queries[i]
        content += f"{sent}\n\n"

        # tokenizer word
        content += "Tokenizer output: "
        tokens = tokenizer.tokenize(sent)
        content += f"{tokens}\n\n"

        # sequence tagging on tokens
        content += "Sequence tagger output: "
        toks = seqtag(tokens)
        content += "\n"
        content += "\n".join([str(tok) for tok in toks])
        content += "\n\n"

        # Malt parser
        content += "Malt parser output: "
        parser = MaltParser(toks)
        graphs = parser()
        content += "\n"
        content += "\n".join([str(g) for g in graphs])
        content += "\n\n"

        # Grammatical relation
        content += "Grammatical relation: \n"
        grammar_rel = GrammarRelation(graphs)
        content += f"{grammar_rel}\n"

        # Logial form
        content += "Logical form: "
        logical_form = LogicalForm(grammar_rel)
        content += f"{logical_form}\n\n"

        # Procedural semantic form
        content += "Procedural semantic form: "
        proc_sem = ProceduralSem(logical_form)
        content += f"{proc_sem}\n\n"

        # Query dataset
        content += "SQL query: "
        query = QueryTransform(proc_sem.easy_query())
        content += f"{query}\n\n"

        # Final result
        content += "Final result: "
        res = querydb.query_db(query)
        content += f"{res}\n"

        with open(out_file, "w+") as file:
            file.write(content)

    querydb.close()
