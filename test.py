from models import DataLoader

if __name__ == "__main__":
    queries = DataLoader()
    queries.load('input/queries.txt')
    for i in range(len(queries)):
        sent = queries[i]
        print(sent)
