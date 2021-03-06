import graphviz


dot = graphviz.Digraph(comment='Polish Expression Calculator')

#Node class used to create the tree
class Node():
    def __init__(self, value=None, role=None, father=None, left=None, right=None) -> None:
        # role is either 'symbol' or 'number', so that means value either holds a symbol or a number 
        self.__content = {
            "value" : value,
            "role" : role,
            "right" : right,
            "left" : left,
            "father" : father, 
        }

    def set_attr(self, attr, value):
        self.__content[attr] = value

    def set_attrs(self, attrs: dict):
        for key, value in attrs:
            self.set_attr(key, value)

    def get_attr(self, attr):
        return self.__content[attr]

    def childs_already_used(self):
        return self.get_attr("left") != None and self.get_attr("right") != None

    def atleast_one_child_used(self):
        return self.get_attr("left") != None or self.get_attr("right") != None
    
    def atleast_one_child_free(self):
        return self.get_attr("left") == None or self.get_attr("right") == None

    def return_direction_of_free_child(self):
        if self.get_attr("left") == None:
            return "left"
        return "right"

    def __repr__(self) -> str:
        value = self.get_attr("value")
        return f"Node object with value: {value}"
    
def return_text():
    with open("polish_expression.txt") as file:
        return file.read()    
#this returns a list of each symbol/number
def read_expression():
    """
        The expression will be read from polish_expression.txt
        All symbols/numbers, will be separated with a space between each other 
    """
    l = []
    with open("polish_expression.txt", "r") as file:
        l = file.read().split()
    
    return l

#a function that check if a value is a symbol or not
def is_symbol(value):
    return value in "-+*/%^"

#returns True if value is a number
def is_number(value):
    return not is_symbol(value)

# a function that gives a role, a role is either 'symbol' or 'number'
def give_role(value):
    if is_symbol(value) == True:
        return "symbol"
    if is_number(value) == True:
        return "number"
    return None

#this part will create the tree representation
def create_tree():
    
    prop = read_expression()
    
    
    def create_node(father=None):
        nou = Node(value=prop[0], role=give_role(prop[0]), father=father)
        return nou
    
    root = create_node()



    # the actual function for creating the tree
    # nod is the current nod we are in
    # k represent the index i am currently in prop
    # ONLY SYMBOLS CAN HAVE CHILDS, NUMBERS ARE LEAFS, that means that nod is always a symbol

    def generating_tree(father, l: list):
        # if i run out of symbol/numbers, there's nothing more to do, just stop
        
        if len(l) == 0:
            return
        
        # value = l[0]
        # as long as one child is free, and i have more elements in the list, i should continue
        while father.atleast_one_child_free() and len(l):
            # nou is created in each iteration so it can work on recursive calls
            # nou will always be the node with the value that is at l[0]
            nou = create_node(father)
            child = father.return_direction_of_free_child()
            father.set_attr(child, nou)
            # afther i connected nou with his father, i cant remove this value, pop l[0]
            l.pop(0)
            # because i inserted a symbol in the tree, i continue to call the functions with the new node
            if nou.get_attr("role") == "symbol":
                generating_tree(nou, l)
            else:
                # because i inserted a number in the tree, i continue to call the function in the father, because numbers are leafs
                # so there in no going down from a number
                generating_tree(father, l)            



    prop.pop(0)
    generating_tree(root, prop)

    return root

# this will traverse the tree generated by create_tree
# it uses divide and conquer algorithm
# at each step the problem splits in 2 smaller problems
def evaluate_expression():
    root = create_tree()

    # for making function calculator() shorter, i created this function, that is responsible with splitting the problem
    # symbol, is the operation
    # left is the left node of the symbol node
    # right is the right node to the symbol node
    # fn is the functin, this will always be calculator() 
    def operation(left, right, symbol, fn):
        if symbol == "-":
            # - may be unary, so in that case, right may be None
            if right == None:
                return - fn(left)
            else:
                return fn(left) - fn(right)
        if symbol == "+":
            if right == None:
                return fn(left)
            return fn(left) + fn(right)
        if symbol == "*":
            return fn(left) * fn(right)
        if symbol == "/":
            return fn(left) / fn(right)
        if symbol == "%":
            return fn(left) % fn(right)
        if symbol == "^":
            return fn(left) ** fn(right)

    def calculator(nod: Node):
        if nod.get_attr("role") == 'number':
            return int(nod.get_attr("value"))

        left = nod.get_attr("left") 
        right = nod.get_attr("right") 
        symbol = nod.get_attr("value") 
        
        return operation(left, right, symbol, calculator)

    

    return calculator(root)
                
# traverse the tree in VLR, value, left, right, preorder
def order(nod: Node):
    print(nod.get_attr("value"))
    if nod.get_attr("left"):
        order(nod.get_attr("left"))

    if nod.get_attr("right"):
        order(nod.get_attr("right"))



def design_tree():
    """
        dot.node(<name>, <content>) , <name> will be the name of the node, and <content> will be it's value
        dot.edge(<name1>, <name2>) , where <name1> and <name2> are the names of 2 different nodes

        The names will be created in the following way:
        If the father will have it's name equal to k, then the left child will have it's name equal to ( 2 * k ), and the right one will have it ( 2 * k + 1 )
    """
    root = create_tree()


    def display_expression():
        prop = return_text()
        dot.node("start", "The polish expression is: ", shape="plaintext")
        dot.node("expression", prop, shape="plaintext")
        dot.node("graph", "The syntax tree of the expression is:", shape="plaintext")

        dot.node("sentinel", "", shape="plaintext")

    def display_result():
        rez = evaluate_expression()
        dot.node("result_text", "The evaluation of this expression equals to:", shape="plaintext")
        dot.node("result", str(rez), shape="plaintext")

        dot.edge("sentinel", "result_text", color="white")
        dot.edge("result_text", "result", color="white") 

    # using the preorder method to create the names of each node
    def preorder(nod: Node, k: int):
        dot.node(str(k), nod.get_attr("value"))
        if k != 1:
            dot.edge(str(k // 2), str(k))

            # this is a leaf, i want to create a sentinel in order to atach the node with the result to the sentinel, just for a better visual display
            if nod.get_attr("role") == "number":
                dot.edge(str(k), "sentinel", color="white")

        else:
            dot.edge("start", "expression", label="", color="white")
            dot.edge("expression", "graph", label="", color="white")
            dot.edge("graph", "1", label="", color="white")

        left = nod.get_attr("left")
        right = nod.get_attr("right")
        if left:
            preorder(left, 2 * k)
        if right:
            preorder(right, 2 * k + 1)




    display_expression()
    preorder(root, 1)   
    display_result() 
    

def main():
    design_tree()

main()
dot.render('doctest-owutput/Polish Expression Calculator_example_2.gv', view=True)