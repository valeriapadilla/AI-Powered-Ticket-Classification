L3_PROFILE = (
    "L3 Profile (Level 3):\n"
    "- Complex and critical incidents requiring advanced expertise and access to core infrastructure.\n"
    "- Issues may involve custom applications, database errors, security incidents, CI/CD failures, performance or memory problems.\n"
    "- No standard solution; requires investigation, root cause analysis, and possibly coordination with other teams or vendors.\n"
    "- High business impact, affecting critical processes or systems.\n"
    "- Requires advanced troubleshooting, forensics, and documentation.\n"
    "Examples: Application Crash on Launch, CI/CD Pipeline Failure, Database Connection Error, Security Patch Failure, Application Memory Leak, Security Incident Detected.\n"
)

CREATE_SOLUTION_PROMPT = (
    "As an L3 support engineer, your task is to generate a comprehensive and technically advanced step-by-step solution for the following issue, using the context of similar solutions if relevant.\n"
    "Follow the L3 profile:\n"
    f"{L3_PROFILE}\n"
    "\nIssue:\n{issue}\n\nSimilar solutions context:\n{context}\n\n"
    "Return a detailed, numbered list of advanced troubleshooting and remediation steps. Include root cause analysis, forensics, and coordination with other teams if necessary. Document all findings and actions taken."
) 