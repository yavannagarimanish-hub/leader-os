from fastapi import FastAPI

app = FastAPI(title="LeaderOS")

# In-memory storage (MVP)
decisions = []


@app.get("/")
def home():
    return {
        "product": "LeaderOS",
        "status": "running"
    }


# Create Decision
@app.post("/decision")
def create_decision(title: str, description: str):

    decision = {
        "id": len(decisions) + 1,
        "title": title,
        "description": description,
        "status": "pending"
    }

    decisions.append(decision)

    return decision


# Get All Decisions
@app.get("/decisions")
def get_decisions():
    return decisions


# Update Decision Status
@app.put("/decision/{decision_id}")
def update_decision(decision_id: int, status: str):

    for decision in decisions:
        if decision["id"] == decision_id:
            decision["status"] = status
            return decision

    return {"error": "Decision not found"}


# Delete Decision
@app.delete("/decision/{decision_id}")
def delete_decision(decision_id: int):

    global decisions

    decisions = [
        d for d in decisions if d["id"] != decision_id
    ]

    return {"message": "Decision deleted"}


# Dashboard Analytics
@app.get("/dashboard")
def dashboard():

    total = len(decisions)

    completed = len(
        [d for d in decisions if d["status"] == "completed"]
    )

    pending = total - completed

    execution_score = 0

    if total > 0:
        execution_score = (completed / total) * 100

    return {
        "total_decisions": total,
        "completed": completed,
        "pending": pending,
        "execution_score": execution_score
    }
