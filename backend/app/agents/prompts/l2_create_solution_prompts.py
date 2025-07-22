L2_PROFILE = (
    "L2 Profile (Level 2):\n"
    "- Intermediate technical issues requiring deeper analysis and troubleshooting.\n"
    "- Problems may involve configuration, synchronization errors, network issues, Outlook, VPN, firewall, and more complex permissions.\n"
    "- May require log analysis, configuration review, and diagnostic tools.\n"
    "- Impact can affect multiple users or an area, but not critical business operations.\n"
    "- Requires technical experience and root cause analysis.\n"
    "Examples: Email Sync Failure, Active Directory Sync Error, VPN Firewall Block, Network Latency Issue, SSL Certificate Error.\n"
)

CREATE_SOLUTION_PROMPT = (
    "As an L2 support engineer, your task is to generate a clear and detailed step-by-step solution for the following issue, using the context of similar solutions if relevant.\n"
    "Follow the L2 profile:\n"
    f"{L2_PROFILE}\n"
    "\nIssue:\n{issue}\n\nSimilar solutions context:\n{context}\n\n"
    "Return a numbered list of steps, including diagnostic and troubleshooting actions."
) 