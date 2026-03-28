"""Reusable sample retrieved contexts for Bumbiro AI tests."""

GROUNDED_CONSTITUTIONAL_CONTEXTS = [
    "Section 328 of the Constitution provides that the Constitution may be amended by a bill passed by at least two-thirds of the members of Parliament and approved by at least two-thirds of the members of the Senate.",
    "Under section 67, every Zimbabwean citizen has the right to free, fair and regular elections and to make political choices freely, including the right to form and join political parties.",
    "Section 56 states that all persons are equal before the law and have the right to equal protection and benefit of the law, and women and men have the right to equal treatment.",
]

WEAK_IRRELEVANT_CONTEXTS = [
    "The weather in Harare is generally warm and sunny throughout the year.",
    "Zimbabwe has a rich history of traditional music and dance forms.",
    "The national currency is the Zimbabwean dollar, which has undergone several redenominations.",
    "Harare International Airport serves as the main gateway for international travel.",
    "The country is known for its wildlife reserves and national parks.",
]

EMPTY_CONTEXT = ""

MULTI_CHUNK_CONTEXTS = [
    {
        "chunks": [
            "Section 50 of the Constitution provides rights for arrested persons.",
            "Any person who is arrested must be informed promptly of the reason for arrest.",
            "The arrested person must be permitted to contact a spouse, relative, or legal practitioner.",
            "An arrested person must be treated humanely and with respect for dignity.",
            "If not released, the person must be brought before a court within 48 hours.",
        ],
        "combined": "Section 50 of the Constitution provides rights for arrested persons. Any person who is arrested must be informed promptly of the reason for arrest. The arrested person must be permitted to contact a spouse, relative, or legal practitioner. An arrested person must be treated humanely and with respect for dignity. If not released, the person must be brought before a court within 48 hours."
    },
    {
        "chunks": [
            "Section 6 recognizes the following languages as officially recognized in Zimbabwe:",
            "Chewa, Chibarwe, English, Kalanga, Koisan, Nambya, Ndau, Ndebele, Shangani, Shona,",
            "sign language, Sotho, Tonga, Tswana, Venda and Xhosa.",
        ],
        "combined": "Section 6 recognizes the following languages as officially recognized in Zimbabwe: Chewa, Chibarwe, English, Kalanga, Koisan, Nambya, Ndau, Ndebele, Shangani, Shona, sign language, Sotho, Tonga, Tswana, Venda and Xhosa."
    }
]
