from app.generation.generator import Generator

def test_generator_returns_answer():

    generator = Generator()

    response = generator.generate(
        prompt="Distinguish between Machine Learning (ML) and Deep Learning (DL).",
         )

    assert len(response) > 0