import sys
import os
import re
from collections import Counter

LOG_PATH = '../logs/events.log'

def load_logs():
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines if "registered" in line]

def get_last_registered(logs):
    if logs:
        last_entry = logs[-1]
        name = re.findall(r'Name: (.+?) registered', last_entry)
        return name[0] if name else "Unknown"
    return "No data found."

def get_most_frequent(logs):
    names = [re.findall(r'Name: (.+?) registered', line)[0] for line in logs]
    counter = Counter(names)
    more_than_once = [f"{k} registered {v} time(s)" for k, v in counter.items() if v > 1]
    return more_than_once or ["No one registered more than once."]

def get_all_counts(logs):
    names = [re.findall(r'Name: (.+?) registered', line)[0] for line in logs]
    counter = Counter(names)
    return [f"{k} registered {v} time(s)" for k, v in counter.items()]

def handle_query(query):
    query = query.lower().strip()
    logs = load_logs()

    if any(greet in query for greet in ["hi", "hello", "hey"]):
        return "Hello! How can I assist you today?"
    
    elif any(phrase in query for phrase in ["last person", "registered last", "last registered"]):
        return f"Last registered person: {get_last_registered(logs)}"

    elif any(phrase in query for phrase in ["more than once", "multiple times", "repeatedly"]):
        result = get_most_frequent(logs)
        return "\n".join(result) if result else "No one registered more than once."

    elif any(phrase in query for phrase in ["how many", "count", "total registered", "number of people"]):
        return "\n".join(get_all_counts(logs))

    elif "who" in query and "registered" in query:
        return "\n".join(get_all_counts(logs))

    else:
        return "Sorry, I don't understand the question."

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No query received")
        sys.exit(1)

    query = sys.argv[1]
    reply = handle_query(query)
    print(reply)
