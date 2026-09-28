# 📚 Library Dashboard

A **menu-driven Library Dashboard** built with Python for analyzing and managing library borrowing transactions.

The project uses **Object-Oriented Programming (OOP)** along with **Pandas, NumPy, Matplotlib, and Seaborn** to perform data cleaning, analysis, filtering, statistical calculations, and visualization.

---

## 📌 Project Overview

The Library Dashboard analyzes library transaction data stored in a CSV file.

The dataset contains:

* Transaction ID
* Date
* User ID
* Book Title
* Genre
* Borrowing Duration (Days)

The application provides a simple **command-line menu** through which users can load, clean, analyze, filter, visualize, and save library data.

---

## 🎯 Objectives

* Load library transaction data from a CSV file.
* Validate required columns and data types.
* Detect missing and invalid records.
* Clean the dataset.
* Calculate borrowing statistics.
* Identify popular books and frequent borrowers.
* Analyze late returns.
* Filter transactions based on different conditions.
* Generate useful charts and reports.
* Save the cleaned dataset.

---

## 🛠️ Technologies Used

| Technology | Purpose                             |
| ---------- | ----------------------------------- |
| Python     | Main programming language           |
| Pandas     | Data loading, cleaning and analysis |
| NumPy      | Numerical calculations              |
| Matplotlib | Data visualization                  |
| Seaborn    | Advanced visualization              |
| OOP        | Modular project design              |

---

## 📂 Project Structure

```text
Library-Dashboard/
│
├── library_dashboard.py
├── library_transactions.csv
├── clean_library_data.csv
└── README.md
```

> `clean_library_data.csv` is generated after using the **Save Clean Data** option.

---

## 📊 Dataset

The input file should be:

```text
library_transactions.csv
```

Required columns:

```text
Transaction ID
Date
User ID
Book Title
Genre
Borrowing Duration (Days)
```

Supported genres include:

```text
Fiction
Science
Technology
History
Self-Help
Fantasy
```

---

## ⚙️ Main Features

### 1. Load Data

Loads the CSV file and checks:

* File existence
* CSV extension
* Required columns
* Date format
* Borrowing duration format

It also checks the dataset for missing, duplicate, and invalid records.

---

### 2. Display Data

Displays the first 20 rows of the dataset along with:

* Total number of records
* Number of records in the current filtered view

---

### 3. Data Cleaning

The cleaning process handles:

* Blank values
* `N/A`
* `NA`
* `null`
* `None`
* `##`
* `@@`
* Missing Transaction IDs
* Duplicate Transaction IDs
* Invalid borrowing durations
* Missing dates
* Missing genre/book/user values

Invalid borrowing durations are replaced using the median of valid borrowing durations.

---

### 4. Computed Columns

The program creates additional columns:

```text
Late Days
Late Return
Borrow Frequency
Frequent Borrower
```

A borrowing duration greater than **14 days** is considered a late return.

A user with **3 or more borrowings** is considered a frequent borrower.

---

### 5. NumPy Analysis

NumPy is used to calculate:

* Average borrowing duration
* Median borrowing duration
* Standard deviation
* Minimum borrowing duration
* Maximum borrowing duration

Example:

```text
Average Borrowing Duration: XX days
Median: XX
Standard Deviation: XX
Minimum Borrowing Days: XX
Maximum Borrowing Days: XX
```

---

### 6. Pandas Analysis

Pandas is used for:

* Dataset shape
* Column information
* Missing-value analysis
* Statistical summary
* Genre-wise borrowing analysis
* Average borrowing duration by genre

---

### 7. Most Borrowed Books

Displays books according to their borrowing frequency.

This helps identify the most popular books in the library.

---

### 8. Frequent Borrowers

Counts the number of books borrowed by each user.

Users with **3 or more borrowings** are displayed as frequent borrowers.

---

### 9. Late Return Analysis

Identifies transactions where:

```text
Borrowing Duration > 14 days
```

The program displays:

* On-time returns
* Late returns
* Total late returns

---

### 10. Statistics

The dashboard calculates important statistics such as:

* Total transactions
* Most borrowed book
* Number of times the book was borrowed
* Average borrowing duration
* Standard deviation
* Busiest date
* Busiest weekday
* Late returns
* Frequent borrowers

---

## 🔎 Filtering

Transactions can be filtered using:

* Genre
* Start date
* End date
* Minimum borrowing duration
* Maximum borrowing duration

Example:

```text
Genre: Fiction
Start date: 2026-01-01
End date: 2026-03-31
Minimum borrowing duration: 5
Maximum borrowing duration: 14
```

The filter can also be cleared to return to the complete dataset.

---

## 📈 Data Visualizations

The dashboard provides several visualizations.

### 📊 Bar Chart

**Top 5 Most Borrowed Books**

Shows the five books with the highest number of borrowings.

### 📈 Line Graph

**Borrowing Trend by Month**

Shows the number of borrowings for each month.

### 🥧 Pie Chart

**Books Borrowed by Genre**

Shows the distribution of borrowing across genres.

### 🔥 Heatmap

**Borrowing Activity by Weekday and Month**

Shows borrowing activity across different weekdays and months.

### 📉 Histogram

**Distribution of Borrowing Duration**

Shows how borrowing durations are distributed.

### 📊 Late Return Chart

Compares:

* On-time returns
* Late returns

### 👥 Top Borrowers Chart

Displays the top 10 users based on the number of books borrowed.

---

## 🖥️ Menu Options

When the program starts, the following menu is displayed:

```text
==================================================
          LIBRARY DASHBOARD
==================================================

 1. Load Data
 2. Display Data
 3. Clean Data
 4. Create Computed Columns
 5. NumPy Analysis
 6. Pandas Analysis
 7. Most Borrowed Books
 8. Frequent Borrowers
 9. Late Return Analysis
10. Calculate Statistics
11. Filter Transactions
12. Clear Filter
13. Generate Report
14. Bar Chart - Top 5 Books
15. Line Graph - Monthly Trend
16. Pie Chart - Genres
17. Heatmap - Weekday and Month
18. Borrowing Duration Chart
19. Late Return Chart
20. Top Borrowers Chart
21. Save Clean Data
 0. Exit
```

---

## 💻 Installation

Make sure Python is installed on your computer.

Install the required libraries:

```bash
pip install pandas numpy matplotlib seaborn
```

---

## ▶️ How to Run

Place the following files in the same folder:

```text
library_dashboard.py
library_transactions.csv
```

Open Command Prompt or PowerShell in that folder and run:

```bash
python library_dashboard.py
```

The program will ask:

```text
Enter the CSV file name [library_transactions.csv]:
```

You can press **Enter** to use the default file.

---

## 🔄 Recommended Workflow

For the best results, use the menu in this order:

```text
1. Load Data
       ↓
2. Display Data
       ↓
3. Clean Data
       ↓
4. Create Computed Columns
       ↓
5. NumPy Analysis
       ↓
6. Pandas Analysis
       ↓
7–12. Detailed Analysis / Filtering
       ↓
13. Generate Report
       ↓
14–20. Visualizations
       ↓
21. Save Clean Data
```

---

## 🧠 Python Concepts Used

This project demonstrates several important Python concepts:

* Variables
* Conditional statements
* `if-elif-else`
* `for` loops
* Functions
* Classes and objects
* Constructor (`__init__`)
* Encapsulation
* Lists
* Dictionaries
* Exception handling
* Lambda functions
* File handling
* Menu-driven programming

---

## 📊 Data Analysis Concepts Used

The project demonstrates:

* Data validation
* Data cleaning
* Missing-value handling
* Duplicate detection
* Type conversion
* GroupBy
* Aggregation
* Value counts
* Filtering
* Statistical analysis
* Date/time analysis
* Data visualization

---

## 📁 Output File

After selecting:

```text
21. Save Clean Data
```

the cleaned dataset is saved as:

```text
clean_library_data.csv
```

---

## ⚠️ Important Notes

* The input file must be in CSV format.
* Required columns must exist in the dataset.
* Load the data before performing analysis.
* Create computed columns before using late-return analysis.
* Filters affect the current analysis view.
* Use **Clear Filter** to return to the complete dataset.

---

## 👨‍💻 Project Type

**Python Data Analysis Project**

### Skills Demonstrated

```text
Python
OOP
NumPy
Pandas
Data Cleaning
Data Analysis
Matplotlib
Seaborn
Data Visualization
Menu-Driven Programming
```

---

## 🚀 Future Improvements

Possible future enhancements:

* Add a graphical user interface (GUI).
* Add login/authentication.
* Add database connectivity.
* Add book inventory management.
* Add member management.
* Add export to Excel/PDF.
* Add interactive dashboards.
* Add automated report generation.

---

## 📜 License

This project is created for **learning and educational purposes**.

