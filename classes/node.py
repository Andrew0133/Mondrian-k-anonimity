class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data         

    def print_tree(self):
        if self.left:
            self.left.print_tree()
        
        print(self.data)
        
        if self.right:
            self.right.print_tree()

    def print_leaf(self):
        if self.left is None and self.right is None:
            print(self.data)

        self.left.print_tree()
        self.right.print_tree()
    
    def sort_values(self, qi):
        self.data.sort_values(by=qi, inplace=True)

    def create_partition(self, dim, value, k):
        """
        Partition function
        """
        new_left = self.data.loc[self.data[dim] <= value]
        new_right = self.data.loc[self.data[dim] > value]
        
        if len(new_left) < k or len(new_right) < k:
            return
        
        self.left = Node(new_left)
        self.right = Node(new_right)
