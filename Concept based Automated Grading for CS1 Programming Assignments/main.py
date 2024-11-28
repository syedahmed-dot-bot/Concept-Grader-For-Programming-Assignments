import os
import ast
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.analyzer import build_cfg, construct_concept_graph
from src.graph_matcher import calculate_similarity
from src.feedback import generate_feedback


def grade_submission(student_code, reference_code, rubric):
    """
    Grades a student submission by comparing its Concept Graph with the reference Concept Graph.
    Combines similarity score and rubric-based scoring for the final task score.
    """
    # Step 1: Parse the student and reference code into ASTs
    student_ast = ast.parse(student_code)
    reference_ast = ast.parse(reference_code)

    # Step 2: Build CFGs for both student and reference code
    student_cfg = build_cfg(student_ast)
    reference_cfg = build_cfg(reference_ast)

    # Step 3: Construct Concept Graphs (CG) from CFGs
    student_cg = construct_concept_graph(student_cfg)
    reference_cg = construct_concept_graph(reference_cfg)

    # Step 4: Match Concept Graphs and calculate similarity
    similarity_score, feedback = calculate_similarity(student_cg, reference_cg)

    # Construct Concept Graphs
    student_cg = construct_concept_graph(student_cfg)
    reference_cg = construct_concept_graph(reference_cfg)

    # Debugging: Print extracted concepts
    print(f"Student CG Nodes: {list(student_cg.nodes(data='label'))}")
    print(f"Reference CG Nodes: {list(reference_cg.nodes(data='label'))}")


    # Step 5: Calculate rubric-based concept score
    rubric_score = 0
    max_rubric_score = sum(item["points"] for item in rubric.values())
    for node in student_cg.nodes(data="label"):
        concept = node[1]
        if concept in rubric:
            rubric_score += rubric[concept]["points"]

    print(f"Rubric Score: {rubric_score}/{max_rubric_score}")
    # Normalize rubric score
    normalized_rubric_score = (rubric_score / max_rubric_score) * 100 if max_rubric_score > 0 else 0

    # Step 6: Combine similarity score and rubric-based score
    final_task_score = 0.5 * similarity_score + 0.5 * normalized_rubric_score  # Weighted combination

    return final_task_score, similarity_score, feedback


def evaluate_all_tasks(students_dir, references_dir, results_dir, rubrics_dir):
    """
    Evaluates all tasks for multiple students using rubrics.
    """
    tasks = [f"task{i}" for i in range(1, 8)]  # Task names: task1, task2, ..., task7

    # Ensure results directory exists
    os.makedirs(results_dir, exist_ok=True)

    # Loop through students
    for student in os.listdir(students_dir):
        student_dir = os.path.join(students_dir, student)
        if not os.path.isdir(student_dir):
            continue  # Skip non-directories

        print(f"Evaluating tasks for {student}...")
        student_results_dir = os.path.join(results_dir, student)
        os.makedirs(student_results_dir, exist_ok=True)

        # Loop through tasks
        for task in tasks:
            student_task_file = os.path.join(student_dir, f"{task}.py")
            reference_task_file = os.path.join(references_dir, f"{task}.py")
            rubric_file = os.path.join(rubrics_dir, f"{task}.json")

            # Check if all files exist
            if not (os.path.exists(student_task_file) and os.path.exists(reference_task_file) and os.path.exists(rubric_file)):
                print(f"Missing files for {task} - Skipping...")
                continue

            # Load student code, reference code, and rubric
            with open(student_task_file, "r") as f:
                student_code = f.read()
            with open(reference_task_file, "r") as f:
                reference_code = f.read()
            with open(rubric_file, "r") as f:
                rubric = json.load(f)

            # Grade the submission
            final_task_score, similarity_score, feedback = grade_submission(student_code, reference_code, rubric)

            # Save results
            result_file = os.path.join(student_results_dir, f"{task}_results.txt")
            with open(result_file, "w", encoding="utf-8") as f:
                f.write(f"Task: {task}\n")
                f.write(f"Final Task Score: {final_task_score:.2f}\n")
                f.write(f"Similarity Score: {similarity_score:.2f}\n")
                f.write("Feedback:\n")
                f.write(feedback)


            print(f"Task {task} evaluated for {student}. Results saved to {result_file}.")

if __name__ == "__main__":
    # Directories
    students_dir = "submissions"     # Directory containing student submissions
    references_dir = "correct_code" # Directory containing reference solutions
    results_dir = "results"          # Directory to save results
    rubrics_dir = "concepts"        # Directory containing task rubrics

    # Evaluate all tasks for all students
    evaluate_all_tasks(students_dir, references_dir, results_dir, rubrics_dir)
