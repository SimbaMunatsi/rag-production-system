"""RAGAS evaluation script for Bumbiro AI RAG system."""

import json
import os
import sys
from pathlib import Path

# Add repo root to path for imports
REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from dotenv import load_dotenv

load_dotenv()

# TODO: Conditional import based on RAGAS version
# RAGAS 0.4.3 may have different API than later versions
try:
    from ragas import evaluate
    from ragas.metrics import (
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    )
except ImportError:
    print("ERROR: RAGAS not installed. Install with: pip install ragas")
    sys.exit(1)

from datasets import Dataset

from app.rag.service import create_rag_pipeline


def load_eval_dataset(dataset_path: str) -> list:
    """Load evaluation dataset from JSON file."""
    with open(dataset_path, "r") as f:
        return json.load(f)


def generate_answers(pipeline, dataset: list) -> list:
    """Generate answers for each question using the RAG pipeline."""
    results = []

    for idx, example in enumerate(dataset):
        question = example["question"]
        print(f"Generating answer for question {idx + 1}/{len(dataset)}: {question[:50]}...")

        try:
            # TODO: Handle session_id management for stateful evaluation
            # Currently using question hash as session_id for determinism
            session_id = f"eval-session-{hash(question) % 10000}"

            result = pipeline.run(query=question, session_id=session_id)

            example["answer"] = result.get("answer", "")
            example["generated_sources"] = result.get("sources", [])

            results.append(example)
        except Exception as e:
            print(f"  WARNING: Failed to generate answer for question {idx}: {e}")
            example["answer"] = ""
            example["generated_sources"] = []
            results.append(example)

    return results


def prepare_dataset_for_ragas(data: list) -> Dataset:
    """
    Prepare data for RAGAS evaluation.
    
    Expected format:
    - question: str
    - answer: str (generated)
    - ground_truth: str
    - contexts: List[str]
    """
    formatted_data = {
        "question": [],
        "answer": [],
        "ground_truth": [],
        "contexts": [],
    }

    for item in data:
        formatted_data["question"].append(item["question"])
        formatted_data["answer"].append(item.get("answer", ""))
        formatted_data["ground_truth"].append(item.get("ground_truth", ""))
        formatted_data["contexts"].append(item.get("contexts", []))

    return Dataset.from_dict(formatted_data)


def run_evaluation(ragas_dataset: Dataset) -> dict:
    """
    Run RAGAS evaluation on the dataset.
    
    TODO: RAGAS 0.4.3 API may differ from later versions.
    If evaluate() fails, check RAGAS documentation for the correct API.
    """
    print("Running RAGAS evaluation...")

    try:
        # Standard RAGAS evaluate call
        results = evaluate(
            ragas_dataset,
            metrics=[
                faithfulness,
                answer_relevancy,
                context_precision,
                context_recall,
            ],
        )

        return results
    except Exception as e:
        print(f"ERROR during evaluation: {e}")
        print("This may be due to RAGAS version mismatch or missing dependencies.")
        return None


def main():
    """Main evaluation function."""
    dataset_path = REPO_ROOT / "eval" / "datasets" / "constitution_eval_dataset.json"

    if not dataset_path.exists():
        print(f"ERROR: Dataset not found at {dataset_path}")
        sys.exit(1)

    print(f"Loading evaluation dataset from {dataset_path}...")
    dataset = load_eval_dataset(str(dataset_path))
    print(f"Loaded {len(dataset)} examples.")

    print("\nCreating RAG pipeline...")
    pipeline = create_rag_pipeline()

    print("\nGenerating answers for evaluation...")
    # TODO: Consider sampling for faster iteration during development
    # eval_sample = dataset[:2]  # Use first 2 for quick test
    dataset_with_answers = generate_answers(pipeline, dataset)

    print("\nPreparing dataset for RAGAS...")
    ragas_dataset = prepare_dataset_for_ragas(dataset_with_answers)

    print("\nRunning RAGAS metrics evaluation...")
    results = run_evaluation(ragas_dataset)

    if results is None:
        print("Evaluation failed. Check logs above.")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("RAGAS EVALUATION RESULTS")
    print("=" * 60)

    # TODO: Parse and display results based on RAGAS version output format
    try:
        print(results)

        # Attempt to save results
        output_path = REPO_ROOT / "eval" / "results" / "ragas_results.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert results to dictionary for JSON serialization
        if hasattr(results, "to_dict"):
            results_dict = results.to_dict()
        else:
            results_dict = dict(results)

        with open(output_path, "w") as f:
            json.dump(results_dict, f, indent=2)

        print(f"\nResults saved to {output_path}")
    except Exception as e:
        print(f"WARNING: Could not save results: {e}")


if __name__ == "__main__":
    main()
