# risk_classifier.py

# https://static1.squarespace.com/static/5a14be9fd0e62827bd667d1f/t/5f1afc8de5b6684a6cc62bb0/1776366981604/2019-12-31+Grable-Lytton-Risk-Assessment.pdf

questions = [

    {
        "question": "1. In general, how would your best friend describe you as a risk taker?",
        "answers": [
            "A real gambler",
            "Willing to take risks after completing adequate research",
            "Cautious",
            "A real risk avoider"
        ],
        "scores": [4, 3, 2, 1]
    },

    {
        "question": "2. You are on a TV game show and can choose one of the following; which would you take?",
        "answers": [
            "$1,000 in cash",
            "50% chance at winning $5,000",
            "25% chance at winning $10,000",
            "5% chance at winning $100,000"
        ],
        "scores": [1, 2, 3, 4]
    },

    {
        "question": "3. You lose your job three weeks before a vacation. What would you do?",
        "answers": [
            "Cancel the vacation",
            "Take a modest vacation",
            "Go as scheduled",
            "Extend the vacation"
        ],
        "scores": [1, 2, 3, 4]
    },

    {
        "question": "4. If you unexpectedly received $20,000 to invest, what would you do?",
        "answers": [
            "Bank account / CD",
            "Safe bonds",
            "Stocks or stock mutual funds"
        ],
        "scores": [1, 2, 3]
    },

    {
        "question": "5. How comfortable are you investing in stocks?",
        "answers": [
            "Not at all comfortable",
            "Somewhat comfortable",
            "Very comfortable"
        ],
        "scores": [1, 2, 3]
    },

    {
        "question": "6. When you think of the word risk, what comes to mind first?",
        "answers": [
            "Loss",
            "Uncertainty",
            "Opportunity",
            "Thrill"
        ],
        "scores": [1, 2, 3, 4]
    },

    {
        "question": "7. What would you do if hard assets were expected to rise?",
        "answers": [
            "Hold bonds",
            "Half money market / half hard assets",
            "All hard assets",
            "Borrow more to buy hard assets"
        ],
        "scores": [1, 2, 3, 4]
    },

    {
        "question": "8. Which investment would you prefer?",
        "answers": [
            "$200 gain / $0 loss",
            "$800 gain / $200 loss",
            "$2600 gain / $800 loss",
            "$4800 gain / $2400 loss"
        ],
        "scores": [1, 2, 3, 4]
    },

    {
        "question": "9. Choose between:",
        "answers": [
            "Sure gain of $500",
            "50% chance to gain $1,000"
        ],
        "scores": [1, 3]
    },

    {
        "question": "10. Choose between:",
        "answers": [
            "Sure loss of $500",
            "50% chance to lose $1,000"
        ],
        "scores": [1, 3]
    },

    {
        "question": "11. How would you invest a $100,000 inheritance?",
        "answers": [
            "Savings account",
            "Stocks and bonds mutual fund",
            "15 common stocks",
            "Gold / silver / oil"
        ],
        "scores": [1, 2, 3, 4]
    },

    {
        "question": "12. Which portfolio is most appealing?",
        "answers": [
            "60% low-risk / 30% medium / 10% high",
            "30% low-risk / 40% medium / 30% high",
            "10% low-risk / 40% medium / 50% high"
        ],
        "scores": [1, 2, 3]
    },

    {
        "question": "13. How much would you invest in a risky gold venture?",
        "answers": [
            "Nothing",
            "One month's salary",
            "Three months' salary",
            "Six months' salary"
        ],
        "scores": [1, 2, 3, 4]
    }
]


def calculate_score(selected_answers):
    """
    selected_answers = [0,2,1,0,...]

    כל איבר הוא אינדקס התשובה שנבחר (מתחיל מ-0).
    """

    if len(selected_answers) != len(questions):
        raise ValueError("Number of answers does not match number of questions.")

    total_score = 0

    for i, answer_index in enumerate(selected_answers):
        total_score += questions[i]["scores"][answer_index]

    return total_score


def get_profile(total_score):

    if total_score <= 18:
        return "Risk Averse"

    elif total_score <= 22:
        return "Risk Averse"

    elif total_score <= 28:
        return "Risk Neutral"

    else:
        return "Risk Seeking"


def evaluate(selected_answers):
    """
    מחזיר:
    score, profile
    """

    score = calculate_score(selected_answers)
    profile = get_profile(score)

    return score, profile


if __name__ == "__main__":

    # מאפשר גם להריץ מהטרמינל לבדיקה

    answers = []

    for q in questions:

        print()
        print(q["question"])

        for i, ans in enumerate(q["answers"]):
            print(f"{i+1}. {ans}")

        while True:

            try:
                choice = int(input("Choose: ")) - 1

                if 0 <= choice < len(q["answers"]):
                    answers.append(choice)
                    break

            except:
                pass

            print("Invalid choice.")

    score, profile = evaluate(answers)

    print("\n===========================")
    print("Score:", score)
    print("Profile:", profile)
    print("===========================")