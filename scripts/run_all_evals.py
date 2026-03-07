import subprocess
import sys


def run():
    subprocess.run([sys.executable, "-m", "pytest"], check=True)

    subprocess.run([sys.executable, "-m", "tests.rag_eval.ragas_eval"], check=True)

    subprocess.run([sys.executable, "-m", "tests.rag_eval.deepeval_eval"], check=True)


if __name__ == "__main__":
    run()