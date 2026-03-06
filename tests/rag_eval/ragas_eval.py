import json
from ragas import evaluate
from ragas.metrics.collections import faithfulness, answer_relevancy

from app.rag.pipeline import RAGPipeline

def run_ragas_eval():

    with open("tests/rag_eval/eval_dataset.json") as f:
        dataset = json.load(f)

    rag = RAGPipeline()

    questions = []
    answers = []
    contexts = []
    ground_truths = []

    for item in dataset:

        result = rag.run(item["question"])

        questions.append(item["question"])
        answers.append(result["answer"])
        contexts.append(result["context"])
        ground_truths.append(item["ground_truth"])

    eval_dataset = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    }

    score = evaluate(
        eval_dataset,
        metrics=[faithfulness, answer_relevancy]
    )

    print(score)