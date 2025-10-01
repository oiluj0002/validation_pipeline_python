from modules.validate import ValidateCsv

if __name__ == "__main__":
    validator = ValidateCsv("data/funcionarios.csv")
    validated, errors = validator.validate()
    
    validator.export(validated=validated, errors=errors)
