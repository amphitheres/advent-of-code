
class Trie:
    def __init__(self,enum):
        self.value = None
        self.children = [None]*len(enum)
        self.Is_Terminal = False
        
        
        
