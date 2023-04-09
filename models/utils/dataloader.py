class DataLoader:
    def __init__(self):
        self.sents = [
	"Máy bay nào đến thành phố Huế luc 13:30HR ?.",
		
        ]
        self.curr_idx = 0
    
    def __len__(self):
        return len(self.sents)

    def get_next_item(self):
        self.curr_idx += 1
        return self.sents[self.curr_idx]

    def __getitem__(self, idx):
        return self.sents[idx]
