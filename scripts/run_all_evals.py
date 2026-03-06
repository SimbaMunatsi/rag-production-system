import sys
import os

import subprocess
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run():

    subprocess.run([sys.executable, "-m", "pytest"])

    subprocess.run([sys.executable, "tests/rag_eval/ragas_eval.py"])

    subprocess.run([sys.executable, "tests/rag_eval/deepeval_eval.py"])


if __name__ == "__main__":
    run()