from langchain_core.prompts import PromptTemplate

priority_template = PromptTemplate(
    input_variables=["question", "context"],
    template=(
        "You are a help-desk assistant.\n"
        "Using ONLY the context below, assign a priority (Low, Medium, High).\n"
        "Context:\n{context}\n"
        "Request:\n{question}\n"
        "Answer with exactly one of: Low, Medium, High."
    ),
)