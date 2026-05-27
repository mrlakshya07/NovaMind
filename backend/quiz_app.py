import spacy
from rapidfuzz import fuzz
import os
import random

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

# -------------------------------
# Helper Functions
# -------------------------------

def read_notes(file_path="notes.txt"):
    """Reads notes from a text file and returns sentences."""
    if not os.path.exists(file_path):
        print("⚠️ notes.txt not found.")
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().strip()
        # Split by periods or newlines
        return [sent.strip() for sent in text.replace("\n", ". ").split(".") if sent.strip()]

def generate_qa_pairs(notes):
    """Generate questions and answers from sentences using spaCy."""
    qa_pairs = []
    for sentence in notes:
        doc = nlp(sentence)

        subject = ""
        verb = ""
        obj = ""
        
        # Extract basic subject, verb, object
        for token in doc:
            if "subj" in token.dep_:
                subject = token.text
            if "obj" in token.dep_:
                obj = token.text
            if token.pos_ == "VERB":
                verb = token.lemma_

        # Create simple question based on patterns
        if "name" in sentence.lower():
            question = "What is your name?"
            answer = [token.text for token in doc if token.ent_type_ == "" and token.text.lower() not in ["my","is"]]
            answer = " ".join(answer)
            if answer:
                qa_pairs.append((question, answer))
        elif subject and verb and obj:
            question = f"Who {verb} {obj}?"
            answer = subject
            qa_pairs.append((question, answer))
        elif subject and verb:
            question = f"What did {subject} {verb}?"
            answer = obj if obj else ""
            if answer:
                qa_pairs.append((question, answer))
    return qa_pairs

def fuzzy_check(user_ans, correct_ans, threshold=70):
    return fuzz.partial_ratio(user_ans.lower(), correct_ans.lower()) >= threshold

def run_quiz(qa_pairs):
    if not qa_pairs:
        print("No questions generated from notes.")
        return

    random.shuffle(qa_pairs)
    score = 0
    for q, a in qa_pairs:
        print("\nQ:", q)
        user = input("Your answer: ").strip()
        if fuzzy_check(user, a):
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Wrong! Correct answer: {a}")
    print(f"\n🎉 Final Score: {score}/{len(qa_pairs)}")

# -------------------------------
# Main Program
# -------------------------------
if __name__ == "__main__":
    notes = read_notes("notes.txt")
    qa_pairs = generate_qa_pairs(notes)
    run_quiz(qa_pairs)