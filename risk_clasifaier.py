# https://static1.squarespace.com/static/5a14be9fd0e62827bd667d1f/t/5f1afc8de5b6684a6cc62bb0/1776366981604/2019-12-31+Grable-Lytton-Risk-Assessment.pdf
# https://team-treatment.squarespace.com/s/2019-12-31-Grable-Lytton-Risk-Assessment.pdf
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

total_score = 0

for q in questions:

    print("\n" + q["question"])

    for i, ans in enumerate(q["answers"]):
        print(f"{i+1}. {ans}")

    while True:

        try:
            choice = int(input("Enter your answer number: "))

            if 1 <= choice <= len(q["answers"]):
                break

            print("Invalid choice.")

        except:
            print("Please enter a number.")

    total_score += q["scores"][choice - 1]

print("\n===================================")
print(f"FINAL SCORE: {total_score}")
print("===================================\n")

if total_score <= 18:

    profile = "Low tolerance for risk"

elif total_score <= 22:

    profile = "Below-average tolerance for risk"

elif total_score <= 28:

    profile = "Average / Moderate tolerance for risk"

elif total_score <= 32:

    profile = "Above-average tolerance for risk"

else:

    profile = "High tolerance for risk"

if profile == "Low tolerance for risk" or profile == "Below-average tolerance for risk":

    profile = "Risk Averse"
elif profile == "Average / Moderate tolerance for risk":

    profile = "Risk Neutral"
else:

    profile = "Risk Seeking"
print("Investor Profile:")
print(profile)