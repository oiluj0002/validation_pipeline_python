from modules.validate import CsvValidator
from modules.report import ReportGenerator

if __name__ == "__main__":
    validator = CsvValidator()
    report = ReportGenerator()

    validator.process("data/funcionarios.csv", "out")
    report.generate_report("out/validated.csv", "out")
