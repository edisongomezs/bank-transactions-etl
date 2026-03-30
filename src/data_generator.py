from faker import Faker
import pandas as pd
import numpy as np
import random
from datetime import datetime

fake = Faker()

# ------------------------------------------
# CONFIG
# ------------------------------------------
CONFIG = {
    "num_transactions": 50,
    "num_accounts": 5,
    "error_rate": 0.05,
    "outlier_rate": 0.02,
    "date_range_days": 30,

    "amount_ranges": {
        "SALARY": (482, 5000),
        "POS": (-200, -1),
        "ATM": (-500, -10),
        "TRANSFER": (-5000, 5000),
        "UTILITY": (-500, -1)
    },

    "outlier_multiplier": 10
}

# ------------------------------------------
# GENERATE ACCOUNTS
# ------------------------------------------
def generate_accounts(n):
    return [f"ACC{1000+i}" for i in range(n)]

# ------------------------------------------
# NON-UNIFORM DISTRIBUTION
# ------------------------------------------
def generate_transaction_distribution(accounts, total_txns):

    weights = np.random.exponential(scale=2, size=len(accounts))
    weights = weights / weights.sum()

    txn_counts = (weights * total_txns).astype(int)

    # Ajustar diferencia
    difference = total_txns - txn_counts.sum()

    for i in range(abs(difference)):
        idx = i % len(txn_counts)

        if difference > 0:
            txn_counts[idx] += 1
        elif difference < 0 and txn_counts[idx] > 0:
            txn_counts[idx] -= 1

    return dict(zip(accounts, txn_counts))

# ------------------------------------------
# RANDOM DATE
# ------------------------------------------
def random_date(days_back):
    return fake.date_time_between(
        start_date=f"-{days_back}d",
        end_date="now"
    )

# ------------------------------------------
# TRANSACTION TYPE
# ------------------------------------------
def get_transaction_type():
    return random.choices(
        ["SALARY", "POS", "ATM", "TRANSFER", "UTILITY"],
        weights=[5, 50, 20, 15, 10],
        k=1
    )[0]

# ------------------------------------------
# GENERATE AMOUNT
# ------------------------------------------
def generate_amount(txn_type):
    min_val, max_val = CONFIG["amount_ranges"][txn_type]
    return round(random.uniform(min_val, max_val), 2)

# ------------------------------------------
# CHANNEL
# ------------------------------------------
def get_channel(txn_type):
    mapping = {
        "SALARY": "TRANSFER",
        "POS": "POS",
        "ATM": "ATM",
        "TRANSFER": "ONLINE",
        "UTILITY": "ONLINE"
    }
    return mapping.get(txn_type, "UNKNOWN")

# ------------------------------------------
# STATUS
# ------------------------------------------
def get_status():
    return random.choice(["SUCCESS", "FAILED"])

# ------------------------------------------
# GENERATE MERCHANT
# ------------------------------------------
def generate_merchant(txn_type):
    if txn_type == "SALARY":
        return "COMPANY_" + fake.company()
    elif txn_type == "ATM":
        return "BANK_ATM"
    else:
        return fake.company()

# ------------------------------------------
# GENERATE DESCRIPTION
# ------------------------------------------
def generate_description(txn_type):
    mapping = {
        "SALARY": "SALARY_PAYMENT",
        "POS": "POS_PURCHASE",
        "ATM": "ATM_WITHDRAWAL",
        "TRANSFER": "TRANSFER",
        "UTILITY": "UTILITY_PAYMENT"
    }
    return mapping.get(txn_type, "UNKNOWN")

# ------------------------------------------
# APPLY OUTLIER
# ------------------------------------------
def apply_outlier(amount):
    if random.random() < CONFIG["outlier_rate"]:
        return amount * CONFIG["outlier_multiplier"]
    return amount

# ------------------------------------------
# APPLY ERRORS
# ------------------------------------------
def apply_errors(record):
    if random.random() < CONFIG["error_rate"]:
        
        error_type = random.choice(["NULL", "INVALID_AMOUNT", "INVALID_DATE"])

        if error_type == "NULL":
            record["merchant"] = None

        elif error_type == "INVALID_AMOUNT":
            record["amount"] = "ERROR"

        elif error_type == "INVALID_DATE":
            record["timestamp"] = "2024-99-99"

    return record

# ------------------------------------------
# GENERATE DATASET
# ------------------------------------------
def generate_dataset():

    accounts = generate_accounts(CONFIG["num_accounts"])
    distribution = generate_transaction_distribution(
        accounts, CONFIG["num_transactions"]
    )

    data = []
    txn_id = 1

    for account, count in distribution.items():

        for _ in range(count):

            txn_type = get_transaction_type()
            amount = generate_amount(txn_type)
            amount = apply_outlier(amount)

            record = {
                "transaction_id": f"TXN{txn_id:06d}",
                "account_id": account,
                "timestamp": random_date(CONFIG["date_range_days"]),
                "amount": amount,
                "currency": "USD",
                "channel": get_channel(txn_type),
                "merchant": generate_merchant(txn_type),
                "description": generate_description(txn_type),
                "status": get_status()
            }

            record = apply_errors(record)

            data.append(record)
            txn_id += 1

    df = pd.DataFrame(data)

    # Guardar
    df.to_csv("data/raw_transactions.csv", index=False)

    print(f"Dataset generado con {len(df)} registros")

if __name__ == "__main__":
    generate_dataset()