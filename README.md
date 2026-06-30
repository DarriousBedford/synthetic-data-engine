# Synthetic Data Engine
**Python | ISAN 3305 Business Programming Capstone | Texas State University | June 2026**

---

## What It Does

This program reads any CSV file, learns the statistical patterns inside it, and generates a completely fake but mathematically realistic version of that dataset. It then audits itself — comparing the fake data's distributions against the original to prove the output actually reflects the source patterns.

The whole thing runs as a 5-phase modular pipeline:

1. **File Acquisition & Validation** — Opens the file, reads it into a single string, and checks for structural integrity (empty file, mismatched quotes) before touching anything else
2. **Matrix Formatting** — Parses the raw string into a clean 2D grid (list of lists), strips whitespace, and separates the header row if one exists
3. **Double-Entry Profile Verification** — Counts value frequencies per column using two completely independent methods (one from raw text, one from the clean matrix) and compares them — if they disagree, the program halts and shows you exactly where the mismatch is
4. **Synthetic Record Production** — Builds a weighted random pool for each column by duplicating values proportionally to their frequency, then picks randomly from that pool to generate each new row
5. **Statistical Distribution Auditing** — Calculates what percentage of the total each value represents in both the original and synthetic datasets, then prints a side-by-side variance report

---

## Why This Matters

Companies working under **GDPR** (EU) or **HIPAA** (US healthcare) cannot use real customer records, patient data, or financial transactions in development and testing environments. Synthetic data solves this — it preserves the statistical shape of real data without containing any actual identities or sensitive records.

This is the same core concept behind enterprise tools like **Gretel.ai**, **Mostly AI**, and **Tonic.ai** — except this version is built from raw Python fundamentals, no external data libraries, to demonstrate a ground-level understanding of how the mechanics actually work.

---

## How to Run It

**Requirements:**
- Python 3.x
- No external libraries required (standard library only: `tkinter`, `random`)

**Steps:**
1. Clone or download this repo
2. Run `bedford_synthetic_engine.py` in any Python environment (IDLE, VS Code, terminal)
3. A file picker window will open — select any `.csv` file
4. Answer whether the file has a header row (yes/no)
5. Enter how many synthetic rows you want to generate
6. Enter an output filename (e.g. `synthetic_output.csv`)
7. The variance audit report prints to the console automatically

**Test file included:** `sample_accounting_ledger.csv` — a 40-row financial transaction dataset with columns for TxnID, Date, Account, Description, Debit, and Credit

---

## Sample Output

```
=== STATISTICAL DISTRIBUTION AUDIT REPORT ===
--- Column 2 ---
Payroll Expense   | Original: 17.5 % | Synthetic: 20.0 % | Delta: 2.5
Accounts Payable  | Original: 12.5 % | Synthetic: 12.0 % | Delta: 0.5
Equipment         | Original: 12.5 % | Synthetic: 12.0 % | Delta: 0.5
Rent Expense      | Original: 20.0 % | Synthetic: 24.0 % | Delta: 4.0
Inventory         | Original: 7.5 %  | Synthetic: 4.0 %  | Delta: 3.5
Cash              | Original: 15.0 % | Synthetic: 8.0 %  | Delta: 7.0
```

Small, non-zero deltas confirm the weighted random sampling is working correctly. A report of all 0.00% deltas would indicate the program copied the original rows instead of generating new ones — the engine is specifically designed to catch and flag that case.

---

## Technical Constraints (Assignment Rules)

This project was built under strict constraints to demonstrate mastery of programming fundamentals:

- **No `csv` module** — all file parsing done manually using `open()`, `.read()`, `.split()`, and `.strip()`
- **No list comprehensions or `enumerate()`** — all loops written explicitly with `while` and `for`
- **No `random.choices()` with weights** — weighted sampling implemented manually via frequency-based pool duplication and `random.randint()`
- **No external data libraries** — no pandas, NumPy, or any Chapter 10+ tools
- **Single-purpose functions** — every function does exactly one thing; `main()` is a pure traffic controller

---

## Architecture

```
synthetic_engine.py
│
├── request_file_path()          # file picker dialog (provided snippet)
├── read_file_blob()             # reads entire file into one string
├── validate_blob()              # checks for empty file / mismatched quotes
├── preview_first_lines()        # prints first 3 lines for analyst review
├── ask_header_exists()          # yes/no header prompt → True/False
├── build_matrix()               # parses blob into 2D list of lists
├── split_header()               # separates header row from data rows
│
├── build_profile_streaming()    # Method 3A: frequency count from raw text
├── build_profile_from_matrix()  # Method 3B: frequency count from matrix
├── compare_profiles()           # double-entry verification
│
├── get_synthetic_row_count()    # user inputs desired row count
├── get_output_filename()        # user inputs output file name
├── generate_synthetic_matrix()  # builds synthetic rows via weighted pool
├── write_synthetic_file()       # writes output CSV
│
├── calculate_percentages()      # converts counts to % of total
├── print_variance_report()      # prints original vs synthetic audit
│
└── main()                       # traffic controller — calls everything
```

---

## What I'd Build Next

This version deliberately uses only raw Python to demonstrate fundamentals. A production version would look like:

- **Rebuild in pandas** — `pd.read_csv()`, `df.value_counts()`, and `df.sample()` would reduce the parsing/profiling logic to ~20 lines
- **Add `sdv` library** — the Synthetic Data Vault (the actual research paper cited in this assignment) handles covariance relationships between columns that frequency-based sampling misses
- **CLI arguments** — replace the `input()` prompts with `argparse` so the engine can run in automated pipelines
- **Output a JSON profile report** — export the frequency dictionaries as structured JSON alongside the CSV for downstream use

---

## About

Built by **Darrious Bedford** as the capstone project for ISAN 3305 Business Programming at Texas State University.

- 📧 DarriousBedford77@gmail.com
- 💼 [LinkedIn](https://linkedin.com/in/DarriousBedford)
- 🐙 [GitHub](https://github.com/DarriousBedford)

*Graduating Spring 2027 | Targeting Data Engineering & Analytics internships | Houston, TX*
