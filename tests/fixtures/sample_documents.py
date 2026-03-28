"""Reusable mocked document objects for Bumbiro AI tests."""

from langchain_core.documents import Document

# Clearly relevant constitutional document chunk
RELEVANT_CONSTITUTIONAL_DOC_1 = Document(
    page_content="Section 328 of the Constitution provides that the Constitution may be amended by a bill passed by at least two-thirds of the members of Parliament and approved by at least two-thirds of the members of the Senate.",
    metadata={
        "source": "Zimbabwe Constitution",
        "section": "328",
        "title": "Amendment of Constitution",
        "page": 150
    }
)

# Second relevant chunk
RELEVANT_CONSTITUTIONAL_DOC_2 = Document(
    page_content="Under section 67, every Zimbabwean citizen has the right to free, fair and regular elections and to make political choices freely, including the right to form and join political parties.",
    metadata={
        "source": "Zimbabwe Constitution",
        "section": "67",
        "title": "Political Rights",
        "page": 85
    }
)

# Irrelevant chunk
IRRELEVANT_DOC = Document(
    page_content="The weather in Harare is generally warm and sunny throughout the year with temperatures ranging from 15°C to 30°C.",
    metadata={
        "source": "Tourism Brochure",
        "title": "Harare Climate Guide",
        "page": 5
    }
)

# List of sample documents for testing
SAMPLE_DOCUMENTS = [
    RELEVANT_CONSTITUTIONAL_DOC_1,
    RELEVANT_CONSTITUTIONAL_DOC_2,
    IRRELEVANT_DOC
]
