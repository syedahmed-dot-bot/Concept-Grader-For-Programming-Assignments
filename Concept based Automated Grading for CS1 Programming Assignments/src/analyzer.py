import ast
import networkx as nx

class CFGBuilder(ast.NodeVisitor):
    """
    A helper class to build the Control-Flow Graph (CFG) from the AST of a Python program.
    """
    def __init__(self):
        self.cfg = nx.DiGraph()
        self.current_block = None
        self.block_counter = 0

    def add_block(self, label):
        """
        Creates a new basic block and returns its identifier.
        """
        block_id = f"Block_{self.block_counter}"
        self.cfg.add_node(block_id, label=label)
        self.block_counter += 1
        return block_id

    def connect_blocks(self, source, target):
        """
        Adds an edge between two basic blocks.
        """
        self.cfg.add_edge(source, target)

    def visit_FunctionDef(self, node):
        """
        Handles function definitions as entry points for the CFG.
        """
        block = self.add_block(f"Function: {node.name}")
        if self.current_block:
            self.connect_blocks(self.current_block, block)
        self.current_block = block
        self.generic_visit(node)

    def visit_If(self, node):
        """
        Handles if-else branches in the AST.
        """
        block = self.add_block("Condition: If")
        self.connect_blocks(self.current_block, block)
        self.current_block = block
        self.visit(node.test)

    # True branch
        true_block = self.add_block("If: True Block")
        self.connect_blocks(block, true_block)
        self.current_block = true_block
        for stmt in node.body:
            self.visit(stmt)

    # False branch
        if node.orelse:
            false_block = self.add_block("If: False Block")
            self.connect_blocks(block, false_block)
            self.current_block = false_block
            for stmt in node.orelse:
                self.visit(stmt)

    def visit_For(self, node):
        """
        Handles for-loops.
        """
        loop_block = self.add_block("Loop: For")
        self.connect_blocks(self.current_block, loop_block)
        self.current_block = loop_block
        for stmt in node.body:
            self.visit(stmt)

        # Connect back for looping
        self.connect_blocks(loop_block, loop_block)

    def visit_While(self, node):
        """
        Handles while-loops.
        """
        loop_block = self.add_block("Loop: While")
        self.connect_blocks(self.current_block, loop_block)
        self.current_block = loop_block
        for stmt in node.body:
            self.visit(stmt)

    # Connect back for looping
        self.connect_blocks(loop_block, loop_block)

def build_cfg(ast_tree):
    """
    Builds a Control-Flow Graph (CFG) for the given AST tree.
    """
    builder = CFGBuilder()
    builder.visit(ast_tree)
    return builder.cfg

def abstract_node(node):
    """
    Abstracts an AST node into a programming concept using rules.
    """
    # Table 1 abstraction rules
    if "Function" in node:
        return node
    if "Loop: For" in node:
        return "Concept: For Loop"
    if "Loop: While" in node:
        return "Concept: While Loop"
    if "Condition: If" in node:
        return "Concept: If Condition"
    if "If: True Block" in node or "If: False Block" in node:
        return "Concept: Conditional Branch"
    return "Concept: General"

def abstract_edges(cfg):
    """
    Abstracts CFG edges into concept edges.
    """
    concept_edges = []
    for bsrc, btgt in cfg.edges():
        csrc = cfg.nodes[bsrc]['label']
        ctgt = cfg.nodes[btgt]['label']
        concept_edges.append((csrc, ctgt))
    return concept_edges

def construct_concept_graph(cfg):
    """
    Constructs the Concept Graph (CG) from the given Control-Flow Graph (CFG).
    """
    concept_graph = nx.DiGraph()

    # Abstract nodes and add them to the Concept Graph
    for node in cfg.nodes():
        abstracted_node = abstract_node(cfg.nodes[node]['label'])
        concept_graph.add_node(node, label=abstracted_node)

    # Abstract edges and add them to the Concept Graph
    for bsrc, btgt in cfg.edges():
        csrc = abstract_node(cfg.nodes[bsrc]['label'])
        ctgt = abstract_node(cfg.nodes[btgt]['label'])
        concept_graph.add_edge(csrc, ctgt)

    return concept_graph
