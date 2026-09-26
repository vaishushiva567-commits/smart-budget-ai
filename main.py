from flask import Flask, request, session

app = Flask(__name__)
app.secret_key = "smart-budget-secret"


@app.route("/", methods=["GET", "POST"])
def home():

    balance = None
    income = 0
    food = 0
    travel = 0
    shopping = 0
    other = 0

    suggestion = ""
    savings_percentage = 0

    food_warning = ""
    travel_warning = ""
    shopping_warning = ""

    history = session.get("history", [])

    if request.method == "POST":

        income = float(request.form["income"])
        food = float(request.form["food"])
        travel = float(request.form["travel"])
        shopping = float(request.form["shopping"])
        other = float(request.form["other"])

        total_expenses = food + travel + shopping + other

        balance = income - total_expenses

        if income > 0:
            savings_percentage = (balance / income) * 100

        history.append({
            "income": income,
            "food": food,
            "travel": travel,
            "shopping": shopping,
            "other": other,
            "balance": balance
        })

        session["history"] = history

        if food > income * 0.30:
            food_warning = "⚠️ Food expense is high."

        if travel > income * 0.20:
            travel_warning = "⚠️ Travel expense is high."

        if shopping > income * 0.20:
            shopping_warning = "⚠️ Shopping expense is high."

        if balance < 0:
            suggestion = "Your expenses are higher than your income."

        elif balance < income * 0.20:
            suggestion = "Your savings are low. Try to reduce unnecessary expenses."

        else:
            suggestion = "Good job! Your budget is under control."

    return f"""
<!DOCTYPE html>
<html>

<head>

    <title>Smart Budget AI</title>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>

        body {{
            font-family: Arial;
            background-color: #f2f2f2;
            text-align: center;
            padding: 30px;
        }}

        .container {{
            background: white;
            width: 500px;
            margin: auto;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 0 10px gray;
        }}

        input {{
            width: 90%;
            padding: 10px;
            margin: 8px;
        }}

        button {{
            padding: 10px 20px;
            margin: 10px;
            cursor: pointer;
        }}

        .chart-box {{
            width: 350px;
            margin: 30px auto;
        }}

        table {{
            background: white;
            margin: auto;
            border-collapse: collapse;
        }}

        th, td {{
            padding: 8px;
        }}

    </style>

</head>

<body>

<div class="container">

    <h1>Smart Budget AI</h1>
    <p class="subtitle">
    Track your income, manage expenses and improve your savings.
</p>

    <form method="POST">

        <p>Income:</p>
        <input type="number" name="income" required>

        <p>Food:</p>
        <input type="number" name="food" value="0">

        <p>Travel:</p>
        <input type="number" name="travel" value="0">

        <p>Shopping:</p>
        <input type="number" name="shopping" value="0">

        <p>Other:</p>
        <input type="number" name="other" value="0">

        <br>

        <button type="submit">Calculate</button>
        <button type="reset">Reset</button>
        <button type="button" onclick="alert('Budget saved successfully!')">
    💾 Save Budget
</button>

    </form>


    {
        "<h2>Remaining Balance: ₹" + str(round(balance, 2)) + "</h2>"
        if balance is not None else ""
    }


    {
        "<p><b>AI Suggestion:</b> " + suggestion + "</p>"
        if balance is not None else ""
    }


    {
        "<p><b>Savings:</b> " + str(round(savings_percentage, 2)) + "%</p>"
        if balance is not None else ""
    }


    <h2>Expense Summary</h2>


    <div style="display:flex; justify-content:center; gap:15px; flex-wrap:wrap;">

        <div style="background:#e8f5e9; padding:15px; border-radius:10px;">
            <h3>Total Income</h3>
            <p>₹{income}</p>
        </div>


        <div style="background:#ffebee; padding:15px; border-radius:10px;">
            <h3>Total Expenses</h3>
            <p>₹{food + travel + shopping + other}</p>
        </div>


        <div style="background:#e3f2fd; padding:15px; border-radius:10px;">
            <h3>Balance</h3>
            <p>₹{balance if balance is not None else 0}</p>
        </div>

    </div>


    <p>🍔 Food: ₹{food}</p>
    <p style="color:red;">{food_warning}</p>

    <p>🚗 Travel: ₹{travel}</p>
    <p style="color:red;">{travel_warning}</p>

    <p>🛍️ Shopping: ₹{shopping}</p>
    <p style="color:red;">{shopping_warning}</p>

    <p>📦 Other: ₹{other}</p>


    <h3>🎯 Savings Goal</h3>

    <p>Try to save at least 20% of your income.</p>

    <p>
        Your current savings:
        ₹{balance if balance is not None else 0}
    </p>

    <p>
        Target savings:
        ₹{round(income * 0.20, 2) if balance is not None else 0}
    </p>
    <div style="background:#fff3e0; padding:15px; margin:20px; border-radius:10px;">
    <h3>📊 Budget Status</h3>
    <p>Track your expenses regularly to manage your budget better.</p>
</div>

    <h2>Expense Chart</h2>

    <div class="chart-box">

        <canvas id="expenseChart"></canvas>

    </div>


</div>


<h2>Expense History</h2>


<table border="1">

    <tr>

        <th>Income</th>
        <th>Food</th>
        <th>Travel</th>
        <th>Shopping</th>
        <th>Other</th>
        <th>Balance</th>

    </tr>


    {''.join(

        f"<tr>"
        f"<td>₹{h['income']}</td>"
        f"<td>₹{h['food']}</td>"
        f"<td>₹{h['travel']}</td>"
        f"<td>₹{h['shopping']}</td>"
        f"<td>₹{h['other']}</td>"
        f"<td>₹{h['balance']}</td>"
        f"</tr>"

        for h in history

    )}

</table>


<script>

const ctx = document.getElementById('expenseChart');

new Chart(ctx, {{

    type: 'pie',

    data: {{

        labels: [
            'Food',
            'Travel',
            'Shopping',
            'Other'
        ],

        datasets: [{{

            data: [
                {food},
                {travel},
                {shopping},
                {other}
            ]

        }}]

    }},

    options: {{

        responsive: true

    }}

}});

</script>


</body>

</html>
"""


if __name__ == "__main__":
    app.run(debug=True)