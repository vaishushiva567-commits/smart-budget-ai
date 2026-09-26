from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Smart Budget & Recommendations Assistant</title>

        <style>
            body {
                font-family: Arial;
                text-align: center;
                background: #f2f6ff;
                padding-top: 100px;
            }

            h1 {
                color: #173b7a;
            }

            h2 {
                color: #333;
            }

            button {
                background: #173b7a;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 8px;
                font-size: 18px;
                cursor: pointer;
            }

            button:hover {
                background: #0d2855;
            }
        </style>
    </head>

    <body>

        <h1>SMART BUDGET</h1>

        <h2>& RECOMMENDATIONS ASSISTANT</h2>

        <h3>NAAN MUDHALVAN GROUP PROJECT</h3>

        <p>Welcome to our Smart Budget Assistant</p>

        <br>

        <a href="/start">
            <button>START PROJECT</button>
        </a>

    </body>
    </html>
    """


@app.route("/start", methods=["GET", "POST"])
def start():

    result = ""
    recommendation = ""

    if request.method == "POST":

        income = float(request.form["income"])
        food = float(request.form["food"])
        travel = float(request.form["travel"])
        shopping = float(request.form["shopping"])
        education = float(request.form["education"])
        bills = float(request.form["bills"])

        total_expense = (
            food +
            travel +
            shopping +
            education +
            bills
        )

        balance = income - total_expense

        result = f"""
        <h2>Budget Analysis</h2>

        <p><b>Monthly Income:</b> ₹{income:.2f}</p>

        <p><b>Total Expense:</b> ₹{total_expense:.2f}</p>

        <p><b>Remaining Balance:</b> ₹{balance:.2f}</p>
        """

        if balance < 0:
            recommendation = """
            <h3 style="color:red;">
            ⚠️ Your expenses are higher than your income.
            Try to reduce unnecessary expenses.
            </h3>
            """

        elif shopping > income * 0.20:
            recommendation = """
            <h3 style="color:orange;">
            💡 Your shopping expense is high.
            Try reducing shopping expenses.
            </h3>
            """

        elif food > income * 0.30:
            recommendation = """
            <h3 style="color:orange;">
            💡 Your food expense is high.
            Try controlling food expenses.
            </h3>
            """

        elif balance >= income * 0.20:
            recommendation = """
            <h3 style="color:green;">
            ✅ Good budgeting!
            You are maintaining a healthy balance.
            </h3>
            """

        else:
            recommendation = """
            <h3 style="color:blue;">
            💡 Try to save more and reduce unnecessary spending.
            </h3>
            """

    return f"""
    <html>

    <head>

        <title>Smart Budget Dashboard</title>

        <style>

            body {{
                font-family: Arial;
                background: #f2f6ff;
                text-align: center;
                padding: 30px;
            }}

            .box {{
                background: white;
                max-width: 500px;
                margin: auto;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0px 0px 10px #aaa;
            }}

            input {{
                width: 80%;
                padding: 12px;
                margin: 7px;
                border: 1px solid #aaa;
                border-radius: 6px;
            }}

            button {{
                background: #173b7a;
                color: white;
                padding: 12px 25px;
                border: none;
                border-radius: 7px;
                font-size: 16px;
            }}

        </style>

    </head>

    <body>

        <div class="box">

            <h1>Smart Budget Dashboard</h1>

            <form method="POST">

                <input
                    type="number"
                    name="income"
                    placeholder="Monthly Income"
                    required
                >

                <input
                    type="number"
                    name="food"
                    placeholder="Food Expense"
                    required
                >

                <input
                    type="number"
                    name="travel"
                    placeholder="Travel Expense"
                    required
                >

                <input
                    type="number"
                    name="shopping"
                    placeholder="Shopping Expense"
                    required
                >

                <input
                    type="number"
                    name="education"
                    placeholder="Education Expense"
                    required
                >

                <input
                    type="number"
                    name="bills"
                    placeholder="Bills Expense"
                    required
                >

                <br><br>

                <button type="submit">
                    CALCULATE BUDGET
                </button>

            </form>

            {result}

            {recommendation}

        </div>

    </body>

    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)