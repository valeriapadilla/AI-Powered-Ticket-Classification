from langchain.prompts import PromptTemplate

eta_template = PromptTemplate(
    input_variables=["question", "context"],
    template=(
        "Given the following support ticket:\n"
        "{question}\n\n"
        "And the following similar past tickets:\n"
        "{context}\n\n"
        "If any of the past tickets are nearly identical to the current ticket, use the ETA from that ticket. "
        "Otherwise, estimate the ETA (in days) based on the most relevant ticket. "
        "Respond ONLY with a single integer (the ETA in days)."
    ),
)