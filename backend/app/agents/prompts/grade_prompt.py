from langchain.prompts import PromptTemplate

grade_prompt = PromptTemplate(
    input_variables=["question", "context"],
    template=(
        "You are an evaluator determining if a retrieved ticket is relevant to a support request.\n"
        "Here is the ticket excerpt: \n\n {context} \n\n"
        "Here is the user request: {question} \n"
        "If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n"
        "Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."
    )
)