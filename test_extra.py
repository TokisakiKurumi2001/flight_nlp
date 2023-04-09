from models import DataLoader, Tokenizer, Token

if __name__ == "__main__":
    queries = DataLoader()
    queries.load('input/extra.txt')
    tokenizer = Tokenizer()
    for i in range(len(queries)):
        sent = queries[i]
        print(tokenizer.tokenize(sent))
