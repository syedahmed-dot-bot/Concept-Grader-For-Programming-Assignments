def generate_feedback(missing_nodes, extra_nodes, missing_edges, extra_edges):
    """
    Generates feedback based on differences in nodes and edges between the student's CG and the reference CG.
    """
    feedback = []

    # Feedback for missing nodes
    if missing_nodes:
        feedback.append("The following concepts are missing from your code:")
        for node in missing_nodes:
            feedback.append(f"  - {node}")

    # Feedback for extra nodes
    if extra_nodes:
        feedback.append("Your code includes unnecessary or incorrect concepts:")
        for node in extra_nodes:
            feedback.append(f"  - {node}")

    # Feedback for missing edges
    if missing_edges:
        feedback.append("The following relationships between concepts are missing:")
        for edge in missing_edges:
            feedback.append(f"  - {edge[0]} → {edge[1]}")

    # Feedback for extra edges
    if extra_edges:
        feedback.append("Your code includes unnecessary or incorrect relationships:")
        for edge in extra_edges:
            feedback.append(f"  - {edge[0]} → {edge[1]}")

    # Return formatted feedback
    return "\n".join(feedback)
