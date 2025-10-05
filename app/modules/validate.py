import csv
from pathlib import Path
from typing import Any, Optional

class CsvValidator:
    """Validates employee data from a CSV file."""
    
    def __init__(self):
        """Initializes the CsvValidator, setting up the valid areas."""
        self.valid_areas = {"Vendas", "TI", "Financeiro", "RH", "Operações"}

    def _validate_row(self, row: dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validates a single row of data against a set of rules.

        Args:
            row (dict[str, Any]): A dictionary representing a single row of employee data.

        Returns:
            tuple (tuple[bool, Optional[str]]): A tuple containing a boolean for validity
                and a string with the error reason if invalid.
        """
        try:
            name = str(row['nome']).strip()
            area = str(row['area']).strip()
            salary = float(row['salario'])
            bonus = float(row['bonus_percentual'])
            
            # Removes fields with blank names
            if not name:
                return False, "Field 'nome' is null."

            # Removes fields with names with numbers
            if any(part.isdigit() for part in name.split()):
                return False, "Field 'nome' has a number."

            # Removes fields that aren't in the areas specified
            if area not in self.valid_areas:
                return False, f"Field {area} is not valid"

            # Removes fields that have negative sallaries
            if salary < 0:
                return False, "Field 'salário' has negative values."

            # Removes fields that have bonuses off the range
            if not 0 <= bonus <= 1:
                return False, "Field 'bonus' out of bounds"
        
        except(ValueError, TypeError, KeyError) as e:
            return False, f"Type Error: {e}"

        return True, None

    def _export_csv(self, path: str, filename: str, data: list[dict[str, Any]]):
        """Exports a list of rows to a specified CSV file.

        Args:
            path (str): The directory path for the output file.
            filename (str): The name of the CSV file to be created.
            data (list[dict[str, Any]]): A list of dictionaries to be written to the file.
        """
        output_path = Path(path)
        output_path.mkdir(parents=True, exist_ok=True)

        file_path = output_path / filename
        with open(file_path, "w", newline='', encoding='utf-8') as f:
            if not data:
                print(f"File '{filename}' was not written because there is no data.")
                return
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

        print(f"File '{filename}' written with {len(data)} rows.")

    def process(self, input_path: str, output_path: str):
        """Processes an entire CSV file, validating and splitting the data.

        Reads an input CSV, validates each row, and exports the valid and
        invalid rows into separate 'validated.csv' and 'errors.csv' files.

        Args:
            input_path (str): The path to the input CSV file.
            output_path (str): The directory where the output files will be saved.
        """
        valids: list[dict[str, Any]] = []
        invalids: list[dict[str, Any]] = []

        try:
            with open(input_path, "r", encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    is_valid, reason = self._validate_row(row)
                    if is_valid:
                        valids.append(row)
                    else:
                        row['motivo'] = reason
                        invalids.append(row)
        
        except FileNotFoundError as e:
            print(f"File '{input_path}' not found: {e}")
            return
        
        # Export files
        self._export_csv(output_path, "validated.csv", valids)
        self._export_csv(output_path, "errors.csv", invalids)
