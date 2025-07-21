from langchain.prompts import PromptTemplate

rewrite_prompt = PromptTemplate(
    input_variables=["question"],
    template=(
        "Look at the input and try to reason about the underlying semantic intent / meaning.\n"
        "Here is the initial question:"
        "\n ------- \n"
        "{question}"
        "\n ------- \n"
        "Formulate an improved question:"
    )
)