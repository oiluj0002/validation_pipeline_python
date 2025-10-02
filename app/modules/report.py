import csv
import json
from pathlib import Path
from typing import Any, Optional

Row = dict[str, Any]

class ReportGenerator:
    def __init__(self):
        pass

    def _calculate_bonus(self, row: Row) -> float:
        BASE_BONUS = 1000
        salary = float(row['salario'])
        perc_bonus = float(row['bonus_percentual'])
        
        total_bonus = BASE_BONUS + salary * perc_bonus

        return total_bonus
    
    def _export_json(self, path: str, filename: str, data: dict[str, Any]):
        output_path = Path(path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        file_path = output_path / filename
        with open(file_path, "w", newline='', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Report '{filename}' generated with success!")
    
    def generate_report(self, input_path:str, output_path: str):
        report: dict[str, Any] = {}

        try:
            with open(input_path, "r") as f:
                reader = csv.DictReader(f)
                employees = list(reader)

                # Create grouped dict for salaries
                salaries_by_area: dict[str, list[float]] = {}
                for row in employees:
                    area = row['area']
                    salary = float(row['salario'])
                    salaries_by_area.setdefault(area, []).append(salary)

                # Calculate grouped metrics by area
                avg_salary_by_area = {
                    area: round(sum(salaries) / len(salaries), 2)
                    for area, salaries in salaries_by_area.items()
                }
                report["average_salary_by_area"] = avg_salary_by_area

                count_by_area = {
                    area: len(salaries)
                    for area, salaries in salaries_by_area.items()
                }
                report["count_employees_by_area"] = count_by_area

                # Create list dict with bonus calculation
                employees_with_bonus: list[dict[str, Any]] = [
                    {**row, 'bonus_final': self._calculate_bonus(row)}
                    for row in employees
                ]

                # Sort dict by biggest bonus value
                top_3_sorted_by_bonus = sorted(
                    employees_with_bonus,
                    key=lambda row: row['bonus_final'],
                    reverse=True
                )[:3]
                top_3_employees_by_bonus = {
                    row['nome']: row['bonus_final']
                    for row in top_3_sorted_by_bonus
                }
                report["top_3_employees_bonus"] = top_3_employees_by_bonus

                # Calculate total bonus value
                total_bonus = sum(row['bonus_final'] for row in employees_with_bonus)
                report["total_bonus_value"] = total_bonus

        except FileNotFoundError:
            print(f"Erro: O arquivo no caminho '{input_path}' não foi encontrado.")
        
        # Export files
        self._export_json(output_path, "kpis.json", report)
