# Natural Language Processing Assignment

- Student Name: Lê Minh Khôi
- Student ID: 1952076

## How to run

```bash
python main.py
```

## Modules inclusion

- `input`: contains queries and database for the assignment
  - `queries.txt`: file contains queries
  - `nlp.db`: file contains the database
  - `make_db.py`: in case there is no `nlp.db` file, run the following snippet
    ```bash
    cd input
    python make_db.py
    cd ..
    ```
- `output`: contains the files result of each query. The format inside the txt file will be as follow

```text
Query: {Content of the query}

Tokenizer output: {Tokenized sequence from the query}

Sequence tagger output:
{"text": {content of the token}, "tag": {tag assigned for the token}} # sequence tagging help tagging the tokens, which make dependency parser works for effectively

Malt parser output:
{Relation name}({head token} -> {tail token})

Grammatical relation:
{grammatical relation output}

Logical form:
{logical form created from the grammatical relation}

Procedural semantic form:
{procedural semantic form create from the logical relation}

SQL query:
{sql query} # using SQLite, therefore, have to use the SQL query to get the result

Final results: {result/answer for the natural query}
```

- `models`: contains files that helps parsing and tagging
  - `utils`: folder contains helper class/function for the program
  - `tokenizer.py`: main class: `Tokenizer`, help identify the Vietnamese words using `WordSegmentor`, create a list of tokens from the input query
  - `seqtagger.py`: main class: `SequenceTagger`, main tasks is to assign tag to the token. This receives a list of tokens from `Tokenizer`, perform add/remove/replace tokens before assign tag by pre-defined rules
  - `malt_parser.py`: main class: `MaltParser`: determine the relationship between tokens, receive a list of tokens and tags from `SequenceTagger`, in order to create a dependency graphs.
  - `grammar_rel.py`: main class: `GrammarRelation`: receives a list of relations from `MaltParser`, extract the neccessary information to create grammatical relation of the query
  - `logical_form.py`: main class: `LogicalForm`: transforms the grammatical relation in to the logical form.
  - `proc_sem.py`: main class: `ProceduralSem`: transforms the logical form into the procedural semantic form that match with the design of the database
  - `dbengine.py`: main class: `QueryTransform` & `QueryDB`. `QueryTransform` converts procedural semantic form into SQL query and the `QueryDB` will take the database and the SQL query to get the result.

## Information
The courses are taught by Ms.Tuoi (pttuoi@gmail.com) and the assignment is graded by Ms.Thuy (thuytin76@gmail.com). 

Have learned a very valuable lesson here that remember to attach all the files within the zip file. I, unfortunately, forgot to put the `main.py` file inside the zip file and receive the score of 3.5 (although later the penalty has been removed and I received the score 5.5). I really want to discuss more about the knowledge within this assignment but was never given a chance. Education here, by my interpretation, is to fit the mind of the students according to the knowledge of teacher (much like fitting the model, ironically).

I hope that I will not make this type of mistake and wish the best of luck for everyone who have read this far.
