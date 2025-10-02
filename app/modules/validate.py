import csv
from pathlib import Path
from typing import Any, Optional

Row = dict[str, Any]

class CsvValidator:
    def __init__(self):
        self.valid_areas = {"Vendas", "TI", "Financeiro", "RH", "Operações"}

    def _validate_row(self, row: Row) -> tuple[bool, Optional[str]]:
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

    def _export_csv(self, path: str, filename: str, data: list[Row]):
        output_path = Path(path)
        output_path.mkdir(parents=True, exist_ok=True)

        file_path = output_path / filename
        with open(file_path, "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

        print(f"File '{filename}' written with {len(data)} rows.")

    def process(self, input_path: str, output_path: str):
        valids: list[Row] = []
        invalids: list[Row] = []

        try:
            with open(input_path, "r") as f:
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
        
        # Export files
        self._export_csv(output_path, "validated.csv", valids)
        self._export_csv(output_path, "erros.csv", invalids)