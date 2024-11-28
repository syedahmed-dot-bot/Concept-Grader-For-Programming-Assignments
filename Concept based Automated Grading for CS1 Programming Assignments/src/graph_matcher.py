import networkx as nx
from feedback import generate_feedback

def match_nodes(CG_student, CG_reference):
    """
    Matches nodes between the student's Concept Graph and the reference Concept Graph.
    Returns the node similarity score.
    """
    student_nodes = set(CG_student.nodes(data="label"))
    reference_nodes = set(CG_reference.nodes(data="label"))

    # Exact matches
    matched_nodes = student_nodes.intersection(reference_nodes)

    # Node similarity score
    node_similarity = len(matched_nodes) / max(len(reference_nodes), 1)
    return node_similarity, student_nodes - matched_nodes, reference_nodes - matched_nodes

def match_edges(CG_student, CG_reference):
    """
    Matches edges between the student's Concept Graph and the reference Concept Graph.
    Returns the edge similarity score.
    """
    student_edges = set(CG_student.edges())
    reference_edges = set(CG_reference.edges())

    # Exact matches
    matched_edges = student_edges.intersection(reference_edges)

    # Edge similarity score
    edge_similarity = len(matched_edges) / max(len(reference_edges), 1)
    return edge_similarity, student_edges - matched_edges, reference_edges - matched_edges

def calculate_similarity(CG_student, CG_reference):
    """
    Calculates the overall similarity between the student's CG and the reference CG.
    Returns the similarity score and feedback.
    """
    # Match nodes
    node_similarity, missing_nodes, extra_nodes = match_nodes(CG_student, CG_reference)

    # Match edges
    edge_similarity, missing_edges, extra_edges = match_edges(CG_student, CG_reference)

    # Combine node and edge similarities
    similarity_score = 0.7 * node_similarity + 0.3 * edge_similarity  # Weighted combination

    # Generate feedback
    feedback = []
    if missing_nodes:
        feedback.append(f"Missing nodes: {missing_nodes}")
    if extra_nodes:
        feedback.append(f"Extra nodes: {extra_nodes}")
    if missing_edges:
        feedback.append(f"Missing edges: {missing_edges}")
    if extra_edges:
        feedback.append(f"Extra edges: {extra_edges}")

    return similarity_score, feedback

def calculate_similarity(CG_student, CG_reference):
    """
    Calculates the overall similarity between the student's CG and the reference CG.
    Returns the similarity score and detailed feedback.
    """
    # Match nodes
    node_similarity, missing_nodes, extra_nodes = match_nodes(CG_student, CG_reference)
    print(f"Matched Nodes: {node_similarity}")
    print(f"Missing Nodes: {missing_nodes}")
    print(f"Extra Nodes: {extra_nodes}")

    # Match edges
    edge_similarity, missing_edges, extra_edges = match_edges(CG_student, CG_reference)
    print(f"Matched Edges: {edge_similarity}")
    print(f"Missing Edges: {missing_edges}")
    print(f"Extra Edges: {extra_edges}")

    # Combine node and edge similarities
    similarity_score = 0.7 * node_similarity + 0.3 * edge_similarity  # Weighted combination
    
    # Generate feedback
    feedback = generate_feedback(missing_nodes, extra_nodes, missing_edges, extra_edges)

    return similarity_score, generate_feedback(missing_nodes, extra_nodes, missing_edges, extra_edges)
