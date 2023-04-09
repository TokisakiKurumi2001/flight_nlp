import re

class DataLoader:
    def __init__(self):
        self.sents = []
        self.curr_idx = 0
    
    def load(self, filepath):
        with open(filepath) as file:
            for line in file:
                line = re.sub("\n", "", line)
                self.sents.append(line)

    def __len__(self):
        return len(self.sents)

    def get_next_item(self):
        self.curr_idx += 1
        return self.sents[self.curr_idx]

    def __getitem__(self, idx):
        return self.sents[idx]
