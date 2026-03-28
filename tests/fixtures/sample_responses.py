"""Reusable sample responses for Bumbiro AI tests."""

# Grounded answer based on constitutional context
GROUNDED_RESPONSE = {
    "answer": "Section 328 of the Constitution provides that the Constitution may be amended by a bill passed by at least two-thirds of the members of Parliament and approved by at least two-thirds of the members of the Senate.",
    "sources": [
        "Section 328 of the Constitution provides that the Constitution may be amended by a bill passed by at least two-thirds of the members of Parliament and approved by at least two-thirds of the members of the Senate."
    ]
}

# Refusal answer for out-of-scope queries
REFUSAL_RESPONSE = {
    "answer": "I can only answer questions based on the Zimbabwe Constitution, and I could not find relevant support for that question in the document.",
    "sources": []
}

# Hallucinated answer example (contains made-up information)
HALLUCINATED_RESPONSE = {
    "answer": "The Constitution can be amended by a simple majority vote in Parliament, and this process was established in 2020 by presidential decree.",
    "sources": [
        "The Constitution can be amended by a simple majority vote in Parliament, and this process was established in 2020 by presidential decree."
    ]
}

# Answer with multiple sources
RESPONSE_WITH_SOURCES = {
    "answer": "Under section 67, every Zimbabwean citizen has the right to free, fair and regular elections and to make political choices freely, including the right to form and join political parties. Section 56 states that all persons are equal before the law and have the right to equal protection and benefit of the law.",
    "sources": [
        "Under section 67, every Zimbabwean citizen has the right to free, fair and regular elections and to make political choices freely, including the right to form and join political parties.",
        "Section 56 states that all persons are equal before the law and have the right to equal protection and benefit of the law."
    ]
}
