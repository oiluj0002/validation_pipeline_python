from modules.validate import CsvValidator

if __name__ == "__main__":
    validator = CsvValidator("data/funcionarios.csv")
    validated, errors = validator.validate()
    path = "out"
    
    validator.export(path, validated, errors)
