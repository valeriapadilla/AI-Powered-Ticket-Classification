from langchain.prompts import PromptTemplate

eta_template = PromptTemplate(
    input_variables=["question", "context"],
    template=(
        "You are a help-desk assistant.\n"
        "Using ONLY the context below, estimate the ETA in days as a single integer.\n"
        "Respond with exactly one number (e.g., \"3\"), without any extra text or labels.\n"
        "If the problem could be result in a hours please select 1 day\n"
        "Context:\n{context}\n"
        "Request:\n{question}"
    ),
)