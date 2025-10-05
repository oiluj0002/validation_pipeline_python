# Python Validation from CSV File

## 💡 Business Problem

Given a file named `funcionarios.csv` containing employee information for a company.

The mission is to:

1.  **Validate the data** for each record based on the rules below:
    * `nome`: Must not be empty and cannot contain numbers.
    * `area`: Must be one of the following: *Vendas*, *TI*, *Financeiro*, *RH*, *Operações*.
    * `salario`: Must be a positive number or zero.

Bonus Percentage: Must be a number between 0 and 1 (inclusive).
1.  **Calculate the final bonus** for each valid employee using the formula:
    ```
    BASE_BONUS = 1000
    final_bonus = BASE_BONUS + salary * bonus_percentage
    ```
2.  **Generate reports**:
    * `validated.csv`: Contains only valid records.
    * `errors.csv`: Contains invalid records with the reason for the error.
    * `kpis.json`: An aggregated report containing:
        * Number of employees by area.
        * Average salary by area.
        * Total overall bonus payout.
        * Top 3 employees with the highest final bonus.


## 🛠️ Project Workflow

The project operates in two main stages, orchestrated by `main.py`: **Data Validation** and **Report Generation**.

### 1. Data Validation (`validate.py`)

* **Input**: The process starts by reading the raw data from `data/funcionarios.csv`.
* **Processing**: The `CsvValidator` class iterates through each row of the CSV file. Each row is checked against a set of predefined **Validation Rules** (see below).
* **Segregation**:
    * If a row is valid, it is stored in a temporary list of valid employees.
    * If a row fails validation for any reason, it is stored in a separate list for invalid records, and a `motivo` (reason) column is added to explain the error.
* **Output**: This stage generates two files in the `out/` directory:
    * `validated.csv`: A clean CSV containing only the rows that passed all validation checks. This file serves as the input for the next stage.
    * `erros.csv`: A CSV containing all rejected rows and the corresponding reason for failure.

### 2. Report Generation (`report.py`)

* **Input**: The `ReportGenerator` class reads the clean data from `out/validated.csv`.
* **Processing**:
    1.  The script calculates the `final_bonus` for each employee using the specified formula.
    2.  It then aggregates the data to compute several Key Performance Indicators (KPIs):
        * Groups employees by `area` to count them and calculate the average salary.
        * Sums the `final_bonus` of all employees to get the total bonus payout.
        * Sorts employees by their `final_bonus` to identify the top 3 earners.
* **Output**: This stage generates the final report in the `out/` directory:
    * `kpis.json`: A JSON file containing the aggregated metrics (employee count and average salary by area, total bonus, and top 3 employees by bonus).


## ⚙️ Requirements

* **Python 3.9+** is recommended to support the type hints used in the project.
* **No external libraries are needed.** This project is written in pure Python, using only standard libraries like `csv`, `json`, and `pathlib`.


## 🚀 How to Run

1.  Clone this repository or ensure all project files (`main.py`, `modules/`, etc.) are in the same directory.
2.  Place your input file at `data/funcionarios.csv`.
3.  From the project's root directory, run the main script via the command line:
    ```bash
    python main.py
    ```
4.  The output files will be generated in the `out/` directory.
