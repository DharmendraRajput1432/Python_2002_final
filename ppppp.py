"""
Library Dashboard (menu version)

Works with library_transactions.csv, which has these columns:
    Transaction ID, Date, User ID, Book Title, Genre, Borrowing Duration (Days)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

COLUMNS = ["Transaction ID", "Date", "User ID", "Book Title", "Genre",
           "Borrowing Duration (Days)"]
DURATION = "Borrowing Duration (Days)"

ALLOWED_DAYS = 14        # keeping a book longer than this is a late return
FREQUENT_MIN = 3         # this many borrowings or more = frequent borrower
VALID_GENRES = ["Fiction", "Science", "Technology", "History", "Self-Help", "Fantasy"]


class LibraryDashboard:

    def __init__(self, file_name="library_transactions.csv"):
        self.file_name = file_name
        self.df = None          # the full data
        self.filtered = None    # the data we are currently looking at

    # --------------------------------------------------
    # helper: stop early if no data has been loaded
    # --------------------------------------------------
    def has_data(self):
        if self.df is None:
            print("\nPlease load data first.")
            return False
        if self.filtered is None or self.filtered.empty:
            print("\nNo data to analyse (the filter may have matched nothing).")
            return False
        return True

    # --------------------------------------------------
    # 1. LOAD DATA (validate the file, then load with Pandas)
    # --------------------------------------------------
    def load_data(self):

        # Check the file
        if not os.path.isfile(self.file_name):
            print("\nFile not found:", self.file_name)
            return
        if not self.file_name.lower().endswith(".csv"):
            print("\nFile must be a .csv file.")
            return

        try:
            df = pd.read_csv(self.file_name)
        except Exception as e:
            print("\nError:", e)
            return

        # Check the columns
        for column in COLUMNS:
            if column not in df.columns:
                print("\nMissing column:", column)
                return

        # Fix the data types (bad values become NaN / NaT)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df[DURATION] = pd.to_numeric(df[DURATION], errors="coerce")

        self.df = df
        self.filtered = df

        print("\nData loaded successfully!")
        print("Total Records:", len(df))

        # Loop through the rows and report problems
        self.check_rows()

    def check_rows(self):
        problems = []
        seen_ids = []

        for index, row in self.df.iterrows():
            row_number = index + 2      # the CSV header is row 1

            if pd.isna(row["Transaction ID"]):
                problems.append((row_number, "Missing Transaction ID"))
            elif row["Transaction ID"] in seen_ids:
                problems.append((row_number, "Duplicate Transaction ID"))
            else:
                seen_ids.append(row["Transaction ID"])

            if pd.isna(row["Date"]):
                problems.append((row_number, "Missing or invalid Date"))
            if pd.isna(row["User ID"]):
                problems.append((row_number, "Missing User ID"))
            if pd.isna(row["Book Title"]):
                problems.append((row_number, "Missing Book Title"))

            if pd.isna(row["Genre"]):
                problems.append((row_number, "Missing Genre"))
            elif row["Genre"] not in VALID_GENRES:
                problems.append((row_number, "Unknown Genre: " + str(row["Genre"])))

            days = row[DURATION]
            if pd.isna(days):
                problems.append((row_number, "Missing Borrowing Duration"))
            elif days <= 0:
                problems.append((row_number, "Borrowing Duration must be positive"))

        print("\nProblems found:", len(problems))
        for row_number, message in problems:
            print("  Row", row_number, "-", message)

    # --------------------------------------------------
    # 2. DISPLAY DATA
    # --------------------------------------------------
    def display_data(self):

        if self.df is None:
            print("\nPlease load data first.")
            return

        print("\n========== LIBRARY DATA (first 20 rows) ==========")
        print(self.df.head(20).to_string())
        print("\nTotal rows:", len(self.df), "| Rows in current view:", len(self.filtered))

    # --------------------------------------------------
    # 3. DATA CLEANING
    # --------------------------------------------------
    def clean_data(self):

        if self.df is None:
            print("\nPlease load data first.")
            return

        print("\n========== DATA CLEANING ==========")
        df = self.df.copy()

        # Turn blank-looking text into NaN
        for column in df.columns:
            df[column] = df[column].replace(
                ["", "N/A", "NA", "null", "None", "##", "@@"], np.nan)

        # Remove rows with no Transaction ID, and duplicate IDs
        before = len(df)
        df = df.dropna(subset=["Transaction ID"])
        df = df.drop_duplicates(subset="Transaction ID")
        print("Rows removed (missing or duplicate ID):", before - len(df))

        # Invalid borrowing days: use the median of the good values
        good_days = df[DURATION][df[DURATION] > 0]
        median_days = good_days.median()

        fixed = 0
        for i in df.index:
            value = df.loc[i, DURATION]
            if pd.isna(value) or value <= 0:
                df.loc[i, DURATION] = median_days
                fixed += 1
        print("Borrowing durations fixed:", fixed)

        # Missing dates: use the previous row's date (data is in date order)
        df = df.sort_values("Date")
        df["Date"] = df["Date"].ffill().bfill()

        # Missing text values get a label
        df["Genre"] = df["Genre"].fillna("Unknown")
        df["Book Title"] = df["Book Title"].fillna("Unknown")
        df["User ID"] = df["User ID"].fillna("UNKNOWN")

        self.df = df.reset_index(drop=True)
        self.filtered = self.df
        print("Data cleaning completed.")

    # --------------------------------------------------
    # 4. CREATE COMPUTED COLUMNS
    # --------------------------------------------------
    def create_columns(self):

        if self.df is None:
            print("\nPlease load data first.")
            return

        print("\n========== COMPUTED COLUMNS ==========")
        df = self.df

        # Late return
        df["Late Days"] = df[DURATION] - ALLOWED_DAYS
        df["Late Days"] = df["Late Days"].apply(lambda x: x if x > 0 else 0)
        df["Late Return"] = np.where(df["Late Days"] > 0, "Yes", "No")

        # Frequent borrower
        frequency = df["User ID"].value_counts()
        df["Borrow Frequency"] = df["User ID"].map(frequency)
        df["Frequent Borrower"] = np.where(
            df["Borrow Frequency"] >= FREQUENT_MIN, "Yes", "No")

        self.df = df
        self.filtered = df
        print("Computed columns created.")
        print(df.head().to_string())

    # --------------------------------------------------
    # 5. NUMPY ANALYSIS
    # --------------------------------------------------
    def numpy_analysis(self):

        if not self.has_data():
            return

        borrow_array = np.array(self.filtered[DURATION], dtype=float)
        borrow_array = borrow_array[~np.isnan(borrow_array)]

        if len(borrow_array) == 0:
            print("\nNo valid borrowing data.")
            return

        print("\n========== NUMPY ANALYSIS ==========")
        print("Borrowing Times:", borrow_array)
        print("Average Borrowing Duration:", round(np.mean(borrow_array), 2), "days")
        print("Median:", np.median(borrow_array))
        print("Standard Deviation:", round(np.std(borrow_array), 2))
        print("Minimum Borrowing Days:", np.min(borrow_array))
        print("Maximum Borrowing Days:", np.max(borrow_array))

    # --------------------------------------------------
    # 6. PANDAS SUMMARY
    # --------------------------------------------------
    def pandas_analysis(self):

        if not self.has_data():
            return

        print("\n========== PANDAS ANALYSIS ==========")

        print("\nDataset Shape:")
        print(self.filtered.shape)

        print("\nColumn Information:")
        self.filtered.info()

        print("\nMissing Values:")
        print(self.filtered.isnull().sum())

        print("\nStatistical Summary:")
        print(self.filtered.describe())

        print("\nBorrowings and average duration per genre:")
        table = self.filtered.groupby("Genre").agg(
            total_borrowings=("Transaction ID", "count"),
            avg_duration=(DURATION, "mean"))
        table["avg_duration"] = table["avg_duration"].round(2)
        print(table.sort_values("total_borrowings", ascending=False))

    # --------------------------------------------------
    # 7. MOST BORROWED BOOKS
    # --------------------------------------------------
    def popular_books(self):

        if not self.has_data():
            return

        result = self.filtered["Book Title"].value_counts()

        print("\n========== MOST BORROWED BOOKS ==========")
        print(result)

    # --------------------------------------------------
    # 8. FREQUENT BORROWERS
    # --------------------------------------------------
    def frequent_borrowers(self):

        if not self.has_data():
            return

        result = self.filtered["User ID"].value_counts()

        print("\n========== BORROWER FREQUENCY ==========")
        print(result)

        print("\nFrequent Borrowers (", FREQUENT_MIN, "or more books ):")
        for borrower, count in result.items():
            if count >= FREQUENT_MIN:
                print(borrower, "->", count, "books borrowed")

    # --------------------------------------------------
    # 9. LATE RETURN ANALYSIS
    # --------------------------------------------------
    def late_return_analysis(self):

        if not self.has_data():
            return

        if "Late Return" not in self.filtered.columns:
            print("\nPlease create computed columns first (option 4).")
            return

        result = self.filtered["Late Return"].value_counts()

        print("\n========== LATE RETURN ANALYSIS ==========")
        print(result)

        late_count = (self.filtered["Late Return"] == "Yes").sum()
        print("\nTotal Late Returns:", late_count)

    # --------------------------------------------------
    # 10. CALCULATE STATISTICS
    # --------------------------------------------------
    def calculate_statistics(self):

        if not self.has_data():
            return {}

        df = self.filtered
        book_counts = df["Book Title"].value_counts()
        date_counts = df["Date"].dt.date.value_counts()
        weekday_counts = df["Date"].dt.day_name().value_counts()
        user_counts = df["User ID"].value_counts()
        days = np.array(df[DURATION], dtype=float)
        days = days[~np.isnan(days)]

        stats = {
            "total_transactions": len(df),
            "most_borrowed_book": book_counts.idxmax(),
            "times_borrowed": int(book_counts.max()),
            "avg_borrow_days": round(float(np.mean(days)), 2),
            "std_borrow_days": round(float(np.std(days)), 2),
            "busiest_date": date_counts.idxmax(),
            "busiest_date_count": int(date_counts.max()),
            "busiest_weekday": weekday_counts.idxmax(),
            "late_returns": int((df[DURATION] > ALLOWED_DAYS).sum()),
            "frequent_borrowers": int((user_counts >= FREQUENT_MIN).sum()),
        }
        return stats

    # --------------------------------------------------
    # 11. FILTER TRANSACTIONS
    # --------------------------------------------------
    def filter_transactions(self, condition):

        if self.df is None:
            print("\nPlease load data first.")
            return None

        # condition can hold: genre, start_date, end_date, min_duration, max_duration
        rows = self.df

        if "genre" in condition:
            rows = rows[rows["Genre"].str.lower() == condition["genre"].lower()]
        if "start_date" in condition:
            rows = rows[rows["Date"] >= pd.to_datetime(condition["start_date"])]
        if "end_date" in condition:
            rows = rows[rows["Date"] <= pd.to_datetime(condition["end_date"])]
        if "min_duration" in condition:
            rows = rows[rows[DURATION] >= condition["min_duration"]]
        if "max_duration" in condition:
            rows = rows[rows[DURATION] <= condition["max_duration"]]

        self.filtered = rows.reset_index(drop=True)
        print("\nFound", len(self.filtered), "transactions")
        return self.filtered

    def ask_for_filter(self):
        print("\nFilter the data (press Enter to skip a question)")
        condition = {}

        genre = input("  Genre: ").strip()
        if genre != "":
            condition["genre"] = genre

        start = input("  Start date (YYYY-MM-DD): ").strip()
        if start != "":
            condition["start_date"] = start

        end = input("  End date (YYYY-MM-DD): ").strip()
        if end != "":
            condition["end_date"] = end

        try:
            low = input("  Minimum borrowing duration (days): ").strip()
            if low != "":
                condition["min_duration"] = int(low)

            high = input("  Maximum borrowing duration (days): ").strip()
            if high != "":
                condition["max_duration"] = int(high)

            self.filter_transactions(condition)
        except ValueError:
            print("\nInvalid date or number entered. Filter not applied.")

    def reset_filter(self):
        if self.df is None:
            print("\nPlease load data first.")
            return
        self.filtered = self.df
        print("\nFilter cleared. Using all", len(self.df), "transactions.")

    # --------------------------------------------------
    # 12. GENERATE REPORT
    # --------------------------------------------------
    def generate_report(self):

        stats = self.calculate_statistics()
        if not stats:
            return

        print("\n" + "=" * 44)
        print("        LIBRARY TRANSACTION REPORT")
        print("=" * 44)
        print("Total transactions   :", stats["total_transactions"])
        print("Most borrowed book   :", stats["most_borrowed_book"],
              "(", stats["times_borrowed"], "times )")
        print("Average borrowing    :", stats["avg_borrow_days"], "days")
        print("Std deviation        :", stats["std_borrow_days"])
        print("Busiest date         :", stats["busiest_date"],
              "(", stats["busiest_date_count"], "borrows )")
        print("Busiest weekday      :", stats["busiest_weekday"])
        print("Late returns         :", stats["late_returns"])
        print("Frequent borrowers   :", stats["frequent_borrowers"])
        print("=" * 44)

    # --------------------------------------------------
    # 13. BAR CHART: TOP 5 BOOKS
    # --------------------------------------------------
    def book_chart(self):

        if not self.has_data():
            return

        top5 = self.filtered["Book Title"].value_counts().head(5)

        plt.figure(figsize=(9, 5))
        sns.barplot(x=top5.values, y=top5.index, color="steelblue",
                    label="Borrowings")
        plt.xlabel("Number of Borrowings")
        plt.ylabel("Book")
        plt.title("Top 5 Most Borrowed Books")
        plt.legend()
        plt.tight_layout()
        plt.show()

    # --------------------------------------------------
    # 14. LINE GRAPH: BORROWING TREND BY MONTH
    # --------------------------------------------------
    def monthly_chart(self):

        if not self.has_data():
            return

        months = self.filtered["Date"].dt.strftime("%Y-%m")
        per_month = self.filtered.groupby(months).size()

        plt.figure(figsize=(9, 5))
        plt.plot(per_month.index, per_month.values, marker="o",
                 color="darkgreen", label="Borrowings per month")
        plt.xlabel("Month")
        plt.ylabel("Number of Borrowings")
        plt.title("Borrowing Trend by Month")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.show()

    # --------------------------------------------------
    # 15. PIE CHART: GENRES
    # --------------------------------------------------
    def genre_chart(self):

        if not self.has_data():
            return

        genre_counts = self.filtered["Genre"].value_counts()

        plt.figure(figsize=(8, 7))
        plt.pie(genre_counts.values, autopct="%1.1f%%", startangle=90)
        plt.title("Books Borrowed by Genre")
        plt.legend(genre_counts.index, title="Genre",
                   loc="center left", bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        plt.show()

    # --------------------------------------------------
    # 16. HEATMAP: WEEKDAY AND MONTH
    # --------------------------------------------------
    def heatmap_chart(self):

        if not self.has_data():
            return

        df = self.filtered
        table = pd.crosstab(df["Date"].dt.day_name(),
                            df["Date"].dt.strftime("%Y-%m"))
        days = ["Monday", "Tuesday", "Wednesday", "Thursday",
                "Friday", "Saturday", "Sunday"]
        table = table.reindex(days, fill_value=0)

        plt.figure(figsize=(10, 5))
        sns.heatmap(table, annot=True, fmt="g", cmap="YlOrRd",
                    cbar_kws={"label": "Number of borrowings"})
        plt.xlabel("Month")
        plt.ylabel("Weekday")
        plt.title("Borrowing Activity by Weekday and Month")
        plt.tight_layout()
        plt.show()

    # --------------------------------------------------
    # 17. BORROWING DURATION CHART
    # --------------------------------------------------
    def borrowing_chart(self):

        if not self.has_data():
            return

        plt.figure(figsize=(8, 5))
        sns.histplot(self.filtered[DURATION], bins=10, kde=True,
                     color="teal", label="Borrowings")
        plt.xlabel("Borrowing Duration (Days)")
        plt.ylabel("Number of Books")
        plt.title("Distribution of Borrowing Duration")
        plt.legend()
        plt.tight_layout()
        plt.show()

    # --------------------------------------------------
    # 18. LATE RETURN CHART
    # --------------------------------------------------
    def late_return_chart(self):

        if not self.has_data():
            return

        late = int((self.filtered[DURATION] > ALLOWED_DAYS).sum())
        on_time = len(self.filtered) - late

        plt.figure(figsize=(6, 5))
        plt.bar("On time", on_time, color="seagreen", label="On time")
        plt.bar("Late", late, color="tomato", label="Late (over " + str(ALLOWED_DAYS) + " days)")
        plt.xlabel("Return status")
        plt.ylabel("Number of Records")
        plt.title("Late Return Analysis")
        plt.legend()
        plt.tight_layout()
        plt.show()

    # --------------------------------------------------
    # 19. TOP BORROWERS CHART
    # --------------------------------------------------
    def borrower_chart(self):

        if not self.has_data():
            return

        borrower_count = self.filtered["User ID"].value_counts().head(10)

        plt.figure(figsize=(9, 5))
        sns.barplot(x=borrower_count.index, y=borrower_count.values,
                    color="slateblue", label="Books borrowed")
        plt.xlabel("User ID")
        plt.ylabel("Number of Books")
        plt.title("Top Borrowers")
        plt.legend()
        plt.tight_layout()
        plt.show()

    # --------------------------------------------------
    # 20. SAVE CLEAN DATA
    # --------------------------------------------------
    def save_data(self):

        if self.df is None:
            print("\nPlease load data first.")
            return

        self.df.to_csv("clean_library_data.csv", index=False)
        print("\nClean data saved as 'clean_library_data.csv'")


# ======================================================
# MENU DRIVEN PROGRAM
# ======================================================
def main():
    file_name = input("Enter the CSV file name [library_transactions.csv]: ").strip()
    if file_name == "":
        file_name = "library_transactions.csv"

    dashboard = LibraryDashboard(file_name)

    while True:

        print("\n")
        print("=" * 50)
        print("          LIBRARY DASHBOARD")
        print("=" * 50)

        print(" 1. Load Data")
        print(" 2. Display Data")
        print(" 3. Clean Data")
        print(" 4. Create Computed Columns")
        print(" 5. NumPy Analysis")
        print(" 6. Pandas Analysis")
        print(" 7. Most Borrowed Books")
        print(" 8. Frequent Borrowers")
        print(" 9. Late Return Analysis")
        print("10. Calculate Statistics")
        print("11. Filter Transactions")
        print("12. Clear Filter")
        print("13. Generate Report")
        print("14. Bar Chart - Top 5 Books")
        print("15. Line Graph - Monthly Trend")
        print("16. Pie Chart - Genres")
        print("17. Heatmap - Weekday and Month")
        print("18. Borrowing Duration Chart")
        print("19. Late Return Chart")
        print("20. Top Borrowers Chart")
        print("21. Save Clean Data")
        print(" 0. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            dashboard.load_data()
        elif choice == "2":
            dashboard.display_data()
        elif choice == "3":
            dashboard.clean_data()
        elif choice == "4":
            dashboard.create_columns()
        elif choice == "5":
            dashboard.numpy_analysis()
        elif choice == "6":
            dashboard.pandas_analysis()
        elif choice == "7":
            dashboard.popular_books()
        elif choice == "8":
            dashboard.frequent_borrowers()
        elif choice == "9":
            dashboard.late_return_analysis()
        elif choice == "10":
            stats = dashboard.calculate_statistics()
            for name, value in stats.items():
                print(" ", name, ":", value)
        elif choice == "11":
            dashboard.ask_for_filter()
        elif choice == "12":
            dashboard.reset_filter()
        elif choice == "13":
            dashboard.generate_report()
        elif choice == "14":
            dashboard.book_chart()
        elif choice == "15":
            dashboard.monthly_chart()
        elif choice == "16":
            dashboard.genre_chart()
        elif choice == "17":
            dashboard.heatmap_chart()
        elif choice == "18":
            dashboard.borrowing_chart()
        elif choice == "19":
            dashboard.late_return_chart()
        elif choice == "20":
            dashboard.borrower_chart()
        elif choice == "21":
            dashboard.save_data()
        elif choice == "0":
            print("\nThank you for using Library Dashboard!")
            break
        else:
            print("\nInvalid choice! Please select a valid option.")


if __name__ == "__main__":
    main()