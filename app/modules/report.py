import csv
import json

class ReportGenerator:
    def __init__(self, path:str):
        self.file:list[dict] = []

        with open(path, "r") as f:
            for i in csv.DictReader(f):
                self.file.append(i)

    def add_bonus(self) -> list[dict]:
        # Total Bonus
        file_with_bonus = []
        BASE_BONUS = 1000

        for fields in self.file:
            sallary = float(fields['salario'])
            perc_bonus = float(fields['bonus_percentual'])
            total_bonus = BASE_BONUS + sallary * perc_bonus

            fields['bonus_final'] = total_bonus
            file_with_bonus.append(fields)

        return file_with_bonus
    
    def group_fields_by_sallary(self):
        grouped_fields = {}

        for fields in self.file:
            area = fields['area']
            sallary = float(fields['salario'])

            default:list = grouped_fields.setdefault(area, [])
            default.append(sallary)
        
        return grouped_fields
    
    def calculate(self):
        grouped_fields_by_sallary = self.group_fields_by_sallary()

        sallaries_by_area = {}
        count_by_area = {}

        for areas, sallaries in grouped_fields_by_sallary.items():
            if sallaries:
                count_by_area[areas] = len(sallaries)
                sallaries_by_area[areas] = round(sum(sallaries) / len(sallaries), 2)

        file_with_bonus = self.add_bonus()     

        total_bonus = sum((fields['bonus_final'] for fields in file_with_bonus))

        sorted_bonus = sorted(file_with_bonus, key=lambda fields: fields['bonus_final'], reverse=True)
        
        top_3_sorted = {}
        for fields in sorted_bonus[:3]:
            top_3_sorted[fields['nome']] = fields['bonus_final']

        return sallaries_by_area, count_by_area, total_bonus, top_3_sorted


if __name__ == '__main__':
    test = ReportGenerator("out/validated.csv")

    test.calculate()
