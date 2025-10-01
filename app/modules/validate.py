import csv
from pathlib import Path
from typing import Any

Row = dict[str, Any]

class CsvValidator():
    def __init__(self, path:str):
        self.file:list[dict] = []
        self.area_validation = ("Vendas", "TI", "Financeiro", "RH", "Operações")

        with open(path, "r") as f:
            for i in csv.DictReader(f):
                self.file.append(i)

    def validate(self) -> tuple[list[dict], list[dict]]:
        valids = []
        invalids = []

        for fields in self.file:
            try:
                name = str(fields['nome']).strip()
                area = str(fields['area']).strip()
                sallary = float(fields['salario'])
                bonus = float(fields['bonus_percentual'])
                
                # Removes fields with blank names
                if not name:
                    fields["motivo"] = "Campo 'nome' em branco."
                    invalids.append(fields)
                    continue

                # Removes fields with names with numbers
                if any(part.isdigit() for part in name.split()):
                    fields["motivo"] = "Campo 'nome' possui número."
                    invalids.append(fields)
                    continue

                # Removes fields that aren't in the areas specified
                if area not in self.area_validation:
                    fields["motivo"] = f"{area} fora das áreas especificadas."
                    invalids.append(fields)
                    continue

                # Removes fields that have negative sallaries
                if sallary < 0:
                    fields["motivo"] = "Campo 'salário' possui valor negativo."
                    invalids.append(fields)
                    continue

                # Removes fields that have bonuses off the range
                if bonus < 0 or bonus > 1:
                    fields["motivo"] = "Campo 'bonus' fora do limite"
                    invalids.append(fields)
                    continue

                valids.append(fields)
            
            except(ValueError, TypeError):
                fields["motivo"] = "Variável inserida com tipo não aceitável"
                invalids.append(fields)
                continue

        return valids, invalids

    def export(self, path:str, validated:list[dict], errors:list[dict]):
        output_path = Path(path)
        validated_path = "validated.csv"
        errors_path = "errors.csv"

        if not output_path.exists():
            output_path.mkdir()
            print(f"Directory '{output_path}' created.")

        with open(output_path / validated_path, "w", newline='', encoding='utf-8') as f:
            buffer = csv.DictWriter(f, fieldnames=validated[0].keys())
            buffer.writeheader()
            buffer.writerows(validated)
            print(f"File '{validated_path}' written.")

        with open(output_path / errors_path, "w", newline='', encoding='utf-8') as f:
            buffer = csv.DictWriter(f, fieldnames=errors[0].keys())
            buffer.writeheader()
            buffer.writerows(errors)
            print(f"File '{errors_path}' written.")
