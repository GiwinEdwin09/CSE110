from enum import Enum

# HOMEWORK: For each AST node you will need
# to write a "three_addr_code" function which
# writes the three address code instruction
# for each node.

# HOMEWORK: For each AST node you should also
# write a "linearize" function which provides
# a list of 3 address instructions for the node
# and its descendants.

# Hint: you may want to utilize the class hierarchy
# to avoid redundant code.

# enum for data types in ClassIeR
class Type(Enum):
    INT = 1
    FLOAT = 2

# base class for an AST node. Each node
# has a type and a VR
class ASTNode():
    def __init__(self) -> None:
        self.node_type = None
        self.vr = None

    def three_addr_code(self, vr_allocator) -> str:
        pass

    def linearize(self, vr_allocator) -> list[str]:
        pass

# AST leaf nodes
class ASTLeafNode(ASTNode):
    def __init__(self, value: str) -> None:
        self.value = value
        super().__init__()

######
# A number leaf node

# The value passed in should be a number
# (probably as a string).

# HOMEWORK: Determine if the number is a float
# or int and set the type
######
class ASTNumNode(ASTLeafNode):
    def __init__(self, value: str) -> None:        
        super().__init__(value)
        if '.' in value:
            self.node_type = Type.FLOAT
        else:
            self.node_type = Type.INT

    def three_addr_code(self, vr_allocator) -> str:
        self.vr = vr_allocator.mk_new_vr()
        if self.node_type == Type.INT:
            return f"{self.vr} = int2vr({self.value});"
        else:
            return f"{self.vr} = float2vr({self.value});"

    def linearize(self, vr_allocator) -> list[str]:
        return [self.three_addr_code(vr_allocator)]
######
# A program variable leaf node

# The value passed in should be an id name
# eventually it should be the new name generated
# by the symbol table to handle scopes.

# When you create this node, you will also need
# to provide its data type
######
class ASTVarIDNode(ASTLeafNode):
    def __init__(self, value: str, value_type) -> None:
        super().__init__(value)
        self.node_type = value_type
        
    def three_addr_code(self, vr_allocator) -> str:
        #I need a new_name
        self.vr = vr_allocator.mk_new_vr()
        return f"{self.vr} = {self.value};"

    def linearize(self, vr_allocator) -> list[str]:
        return [self.three_addr_code(vr_allocator)]

######
# An IO leaf node

# The value passed in should be an id name.
# Because it is an IO node, you do not need
# to get a new name for it.

# When you create this node, you will also need
# to provide its data type. It is recorded in
# the symbol table
######
class ASTIOIDNode(ASTLeafNode):
    def __init__(self, value: str, value_type) -> None:
        super().__init__(value)
        self.node_type = value_type

    def three_addr_code(self, vr_allocator) -> str:
        self.vr = vr_allocator.mk_new_vr()
        if self.node_type == Type.INT:
            return f"{self.vr} = int2vr({self.value});"
        else:
            return f"{self.vr} = float2vr({self.value});"

    def linearize(self, vr_allocator) -> list[str]:
        return [self.three_addr_code(vr_allocator)]

######
# Binary operation AST Nodes

# These nodes require their left and right children to be
# provided on creation
######
class ASTBinOpNode(ASTNode):
    def __init__(self, l_child, r_child) -> None:
        self.l_child = l_child
        self.r_child = r_child
        super().__init__()

    def linearize(self, vr_allocator) -> list[str]:
        code = []
        code.extend(self.l_child.linearize(vr_allocator))
        code.extend(self.r_child.linearize(vr_allocator))
        code.append(self.three_addr_code(vr_allocator))
        return code

class ASTPlusNode(ASTBinOpNode):
    def __init__(self, l_child, r_child) -> None:
        super().__init__(l_child, r_child)
        self.node_type = self.l_child.node_type

    def three_addr_code(self, vr_allocator) -> str:
        self.vr = vr_allocator.mk_new_vr()
        if self.node_type == Type.INT:
            return f"{self.vr} = addi({self.l_child.vr}, {self.r_child.vr});"
        else:
            return f"{self.vr} = addf({self.l_child.vr}, {self.r_child.vr});"

class ASTMultNode(ASTBinOpNode):
    def __init__(self, l_child, r_child) -> None:
        super().__init__(l_child, r_child)
        self.node_type = self.l_child.node_type

    def three_addr_code(self, vr_allocator) -> str:
        self.vr = vr_allocator.mk_new_vr()
        if self.node_type == Type.INT:
            return f"{self.vr} = multi({self.l_child.vr}, {self.r_child.vr});"
        else:
            return f"{self.vr} = mulf({self.l_child.vr}, {self.r_child.vr});"

class ASTMinusNode(ASTBinOpNode):
    def __init__(self, l_child, r_child) -> None:
        super().__init__(l_child, r_child)
        self.node_type = self.l_child.node_type

    def three_addr_code(self, vr_allocator) -> str:
        self.vr = vr_allocator.mk_new_vr()
        if self.node_type == Type.INT:
            return f"{self.vr} = subi({self.l_child.vr}, {self.r_child.vr});"
        else:
            return f"{self.vr} = subf({self.l_child.vr}, {self.r_child.vr});"

class ASTDivNode(ASTBinOpNode):
    def __init__(self, l_child, r_child) ->None:
        super().__init__(l_child, r_child)
        self.node_type = self.l_child.node_type

    def three_addr_code(self, vr_allocator) -> str:
        self.vr = vr_allocator.mk_new_vr()
        if self.node_type == Type.INT:
            return f"{self.vr} = divi({self.l_child.vr}, {self.r_child.vr});"
        else:
            return f"{self.vr} = divf({self.l_child.vr}, {self.r_child.vr});"

######
# Special BinOp nodes for comparisons

# These operations always return an int value
# (as an untyped register):
# 0 for false and 1 for true.

# Because of this, their node type is always
# an int. However, the operations (eq and lt)
# still need to be typed depending
# on their inputs. If their children are floats
# then you need to use eqf, ltf, etc.
######
class ASTEqNode(ASTBinOpNode):
    def __init__(self, l_child, r_child) ->None:
        self.node_type = Type.INT
        super().__init__(l_child, r_child)

    def three_addr_code(self, vr_allocator) -> str:
        self.vr = vr_allocator.mk_new_vr()
        if self.l_child.node_type == Type.INT:
            return f"{self.vr} = eqi({self.l_child.vr}, {self.r_child.vr});"
        else:
            return f"{self.vr} = eqf({self.l_child.vr}, {self.r_child.vr});"

class ASTLtNode(ASTBinOpNode):
    def __init__(self, l_child, r_child: ASTNode) -> None:
        self.node_type = Type.INT
        super().__init__(l_child, r_child)

    def three_addr_code(self, vr_allocator) -> str:
        self.vr = vr_allocator.mk_new_vr()
        if self.l_child.node_type == Type.INT:
            return f"{self.vr} = lti({self.l_child.vr}, {self.r_child.vr});"
        else:
            return f"{self.vr} = ltf({self.l_child.vr}, {self.r_child.vr});"

######
# Unary operation AST Nodes

# The only operations here are converting
# the bits in a virtual register to another
# virtual register of a different type,
# i.e. corresponding to the CLASSIeR instructions:
# vr_int2float and vr_float2int
######
class ASTUnOpNode(ASTNode):
    def __init__(self, child) -> None:
        self.child = child
        super().__init__()

    def linearize(self, vr_allocator) -> list[str]:
        code = self.child.linearize(vr_allocator)
        code.append(self.three_addr_code(vr_allocator))
        return code
        
class ASTIntToFloatNode(ASTUnOpNode):
    def __init__(self, child) -> None:
        super().__init__(child)
        self.node_type = Type.FLOAT

    def three_addr_code(self, vr_allocator) -> str:
        self.vr = vr_allocator.mk_new_vr()
        return f"{self.vr} = vr_int2float({self.child.vr});"

class ASTFloatToIntNode(ASTUnOpNode):
    def __init__(self, child) -> None:
        super().__init__(child)
        self.node_type = Type.INT

    def three_addr_code(self, vr_allocator) -> str:
        self.vr = vr_allocator.mk_new_vr()
        return f"{self.vr} = vr_float2int({self.child.vr});"