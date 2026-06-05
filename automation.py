import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def load_and_clean_data(file_path):
    """Excel ya CSV file ko load aur clean karne ke liye function."""
    print("[+] File load ho rahi hai...")

    # File format check karna (CSV ya Excel)
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
        df = pd.read_excel(file_path)
    else:
        raise ValueError(
            "Unsupported file format! Kripya CSV ya Excel file use karein."
        )

    # Columns ke naam saaf karna (spaces hatana)
    df.columns = df.columns.str.strip()

    # Date column ko sahi format me lana
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])

    # Amount ko numeric banana (agar koi string character ho toh use hatana)
    if "Amount" in df.columns:
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    # Khali values ko fill karna
    df["Category"] = df["Category"].fillna("Others")
    df["Amount"] = df["Amount"].fillna(0)

    print("[+] Data cleaning poori hui!")
    return df


def generate_expense_summary(df):
    """Category ke hisab se kharchon ka total nikalna."""
    print("\n--- EXPENSE SUMMARY (Category Wise) ---")
    summary = df.groupby("Category")["Amount"].sum().reset_index()
    print(summary.to_string(index=False))
    return summary


def visualize_expenses(summary_df):
    """Kharchon ka ek badhiya Bar Chart banana."""
    print("\n[+] Chart generate ho raha hai...")

    # Seaborn style set karna
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(10, 6))
    ax = sns.barplot(
        x="Category", y="Amount", data=summary_df, palette="Spectral"
    )

    # Bars ke upar amounts likhna
    for p in ax.patches:
        ax.annotate(
            f"₹{p.get_height():.2f}",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            xytext=(0, 9),
            textcoords="offset points",
            fontsize=10,
        )

    plt.title("Monthly Expenses Breakdown", fontsize=16, fontweight="bold")
    plt.xlabel("Expense Category", fontsize=12)
    plt.ylabel("Total Amount Spent (₹)", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Chart ko image format me save karna (GitHub par dikhane ke liye)
    chart_filename = "expense_chart.png"
    plt.savefig(chart_filename)
    print(f"[+] Chart successfully save ho gaya: {chart_filename}")
    plt.show()


if __name__ == "__main__":
    # Test karne ke liye hum ek dummy data ki CSV file pehle hi bana dete hain
    dummy_data_file = "my_transactions.csv"

    if not os.path.exists(dummy_data_file):
        data = {
            "Date": [
                "2026-06-01",
                "2026-06-02",
                "2026-06-03",
                "2026-06-04",
                "2026-06-05",
            ],
            "Category": ["Food", "Rent", "Groceries", "Food", "Entertainment"],
            "Amount": [500, 8000, 1500, 350, 1200],
            "Description": [
                "Zomato dinner",
                "Room rent",
                "Supermarket",
                "Office lunch",
                "Movie night",
            ],
        }
        pd.DataFrame(data).to_csv(dummy_data_file, index=False)
        print(f"[+] Demo ke liye ek file banayi gayi: {dummy_data_file}")

    try:
        # Step 1: Data Load aur Clean karo
        transaction_df = load_and_clean_data(dummy_data_file)

        # Step 2: Automation Summary nikalon
        expense_summary = generate_expense_summary(transaction_df)

        # Step 3: Visualizer se chart dikhao
        visualize_expenses(expense_summary)

    except Exception as e:
        print(f"[-] Koi error aayi: {e}")