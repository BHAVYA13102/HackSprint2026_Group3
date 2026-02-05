
import json

class ContextBuilder:
    """
    Assembles retrieved data into a coherent context block for the LLM.
    Ensures clear separation of data sources.
    """
    
    @staticmethod
    def build_structured_context(profile, tenure, attendance, leaves):
        """Formats structured facts into string representation."""
        context = []
        if profile:
            context.append(f"--- SOURCE: Employee Master ---\n{json.dumps(profile, indent=2, default=str)}")
        if tenure:
            context.append(f"--- SOURCE: Calculated Tenure ---\nYears: {tenure['years']}, Months: {tenure['months']}, Total Days: {tenure['total_days']}")
        if attendance:
            context.append(f"--- SOURCE: Attendance Logs ---\nPresent Days: {attendance['days_present']}\nSample Logs: {json.dumps(attendance['records'], indent=2, default=str)}")
        if leaves:
            context.append(f"--- SOURCE: Leave History ---\n{json.dumps(leaves, indent=2, default=str)}")
        
        return "\n\n".join(context)

    @staticmethod
    def build_vector_context(policy_docs):
        """Formats vector results into string representation."""
        context = ["--- SOURCE: HR Policy PDF ---"]
        for i, doc in enumerate(policy_docs):
            page_meta = f"(Page {doc.metadata.get('page', 'Unknown')})"
            context.append(f"Snippet {i+1} {page_meta}:\n{doc.page_content.strip()}")
        
        return "\n\n".join(context)
