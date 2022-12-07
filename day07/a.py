class Tree:

    class Node:
        def __init__(self, name, pai, size = 0):
            self.name = name
            self.pai = pai
            self.filhos = []
            self.size = size
       
    class Dir(Node):
        def __init__(self, name, pai):
            super().__init__(name, pai)
        
        def __repr__(self) -> str:
            return f'- {self.name} (dir, size={self.size})'
    
    class File(Node):
        def __init__(self, name, pai, size):
            super().__init__(name, pai, size)
        
        def __repr__(self) -> str:
            return f'- {self.name} (file, size={self.size})'

    def __init__(self, commands):
        print("Creating Tree")
        self.root = Tree.Dir(name='/', pai=None)
        index = 1
        curr_dir = self.root
        while index < len(commands):
            curr_command = commands[index].split()         
            if curr_command[1] == 'ls':
                index = self.insert_filhos(curr_dir, commands, index+1) 
                continue
            elif curr_command[-1] == '..':
                curr_dir = curr_dir.pai
            else:
                curr_dir = self.__cd_node(curr_command[-1], curr_dir)
            index += 1
        self.emprime()

    def insert_filhos(self, curr_dir, commands, index):
        while index < len(commands) and commands[index][0] != '$':
            command = commands[index].split()
            self.create_node(command, curr_dir)
            index += 1
        return index

    def __cd_node(self, node_name, curr):
        for filho in curr.filhos:
            if filho.name == node_name:
                return filho
        
    def create_node(self, command, curr_dir):
        first, second = command
        if first == 'dir':
            new_node = Tree.Dir(second, curr_dir)
        else:
            new_node = Tree.File(second, curr_dir, size=int(first))
            self.update_size(curr_dir, int(first))
        
        curr_dir.filhos.append(new_node)

    def update_size(self, curr_dir, size):
        curr_dir.size += size
        if isinstance(curr_dir.pai, Tree.Dir):
            self.update_size(curr_dir.pai, size)

    def emprime(self):
        self.__emprime(self.root)

    def __emprime(self, curr, level=0):
        tab = level * '  '
        print(f'{tab}{curr}')
        for filho in curr.filhos:
            self.__emprime(filho, level+1)

    def sum_small_files(self):
        return self.__sum_small_files(self.root)

    def __sum_small_files(self, curr):
        total = 0
        if isinstance(curr, Tree.Dir):
            if curr.size <= 100_000:
                total += curr.size
            for filho in curr.filhos:
                total += self.__sum_small_files(filho)
        return total
            

input = [line.strip() for line in open('input.txt')]

files = Tree(input)

print(files.sum_small_files())
