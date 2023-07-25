# ============== Questions Helper Function ================

def questions_helper(input) -> dict:
    return {
        "id": str(input["_id"]),
        "generated_questions": input["generated_questions"],
        "created_at": str(input["created_at"])
    }