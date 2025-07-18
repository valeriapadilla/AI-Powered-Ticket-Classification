from langchain.prompts import PromptTemplate

level_template = PromptTemplate(
    input_variables=["question", "context"],
        template=(
            "You are a help-desk assistant.\n"
            "Using ONLY the context below, assign a level (L1, L2, L3) to the request.\n"
            "nknowing that L1 is for Procedural, routine tasks with low complexity.\n"
            "L2 is for Intermediate technical issues, system-specific configurations, integration problems.\n"
            "L3 is for Expert-level diagnostics, code-level bugs, architectural issues, critical incidents..\n"
            "Context:\n{context}\n"
            "Request:\n{question}\n"
            "Answer with exactly one of: L1, L2, L3."
        ),
)
