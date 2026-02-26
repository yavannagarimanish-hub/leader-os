# LeaderOS Decision Tracker

decisions = []

def add_decision(decision):
    decisions.append(decision)
    print("Decision Added:", decision)

def view_decisions():
    for d in decisions:
        print("-", d)

add_decision("Launch LeaderOS MVP")
view_decisions()
