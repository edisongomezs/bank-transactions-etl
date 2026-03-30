import matplotlib.pyplot as plt

# ------------------------------------------
# INCOME VS EXPENSE
# ------------------------------------------
def plot_income_vs_expense(df):

    income = df[df["amount"] > 0]["amount"].sum()
    expense = df[df["amount"] < 0]["amount"].sum()

    labels = ["Income", "Expense"]
    values = [income, abs(expense)]

    plt.figure()
    plt.bar(labels, values)
    plt.title("Income vs Expense")
    plt.savefig("output/income_vs_expense.png")
    plt.close()


# ------------------------------------------
# TRANSACTION TYPE
# ------------------------------------------
def plot_transaction_types(df):

    counts = df["description"].value_counts()

    plt.figure(figsize=(8,5))  # más ancho
    counts.plot(kind="bar")

    plt.title("Transactions by Type")
    plt.xticks(rotation=45, ha="right")  # 🔥 clave
    plt.tight_layout()  # 🔥 ajusta márgenes

    plt.savefig("output/transaction_types.png")
    plt.close()