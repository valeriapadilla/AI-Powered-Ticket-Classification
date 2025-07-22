L1_PROFILE = (
    "L1 Profile (Level 1):\n"
    "- Common and repetitive incidents, low complexity.\n"
    "- Known solutions and standard procedures.\n"
    "- Quick resolution, does not require advanced technical knowledge.\n"
    "Examples: Password Reset, Printer Not Responding, Folder Access Denied, Mouse Not Working, User Account Locked.\n"
)

CREATE_SOLUTION_PROMPT = (
    "As an L1 support engineer, your task is to generate a \n" 
    "clear and concise step-by-step solution for the following issue, \n"
    "using the context of similar solutions if relevant.\n"
    "Follow the L1 profile:\n"
    f"{L1_PROFILE}\n"
    "\nIssue:\n{issue}\n\nSimilar solutions context:\n{context}\n\n"
    "Return a numbered list of easy-to-follow steps, using standard procedures whenever possible. If you cannot resolve it, indicate that it."
)