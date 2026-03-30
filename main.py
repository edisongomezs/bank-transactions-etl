from src.data_generator import generate_dataset
from src.transform import transform_data
from src.load import create_connection, load_to_db, run_query
from src.visualize import plot_income_vs_expense, plot_transaction_types

if __name__ == "__main__":

    # 1. Generate
    generate_dataset()

    # 2. Transform
    clean_df, rejected_df = transform_data("data/raw_transactions.csv")

    clean_df.to_csv("data/clean_transactions.csv", index=False)
    rejected_df.to_csv("data/rejected_transactions.csv", index=False)

    print(f"Clean records: {len(clean_df)}")
    print(f"Rejected records: {len(rejected_df)}")

    # 3. Plot
    plot_income_vs_expense(clean_df)
    plot_transaction_types(clean_df)

    # 4. Load
    conn = create_connection()
    load_to_db(clean_df, conn)

    print("\n--- QUERIES ---")

    # 5. Queries reales
    run_query("SELECT COUNT(*) FROM transactions;", conn)

    run_query("""
        SELECT account_id, SUM(amount)
        FROM transactions
        GROUP BY account_id
        LIMIT 5;
    """, conn)

    run_query("""
        SELECT description, COUNT(*)
        FROM transactions
        GROUP BY description;
    """, conn)

    print("\n--- BUSINESS QUERIES ---")

    run_query("""
        SELECT 
            CASE 
                WHEN amount > 0 THEN 'INCOME'
                ELSE 'EXPENSE'
            END as type,
            SUM(amount)
        FROM transactions
        GROUP BY type;
    """, conn)

    run_query("""
        SELECT account_id, COUNT(*) as total_txn
        FROM transactions
        GROUP BY account_id
        ORDER BY total_txn DESC
        LIMIT 5;
    """, conn)

    run_query("""
        SELECT *
        FROM transactions
        WHERE ABS(amount) > 2000;
    """, conn)

    conn.close()