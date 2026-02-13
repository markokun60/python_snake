import os

def read_variables_from_file(file_path):
    """
    Reads key=value pairs from a text file and returns them as a dictionary.
    Handles type conversion for int, float, and bool.
    """
    variables = {}

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                print(f"Skipping invalid line: {line}")
                continue

            key, value = map(str.strip, line.split("=", 1))

            # Try to convert value to int, float, or bool
            if value.lower() in ("true", "false"):
                variables[key] = value.lower() == "true"
            else:
                try:
                    if "." in value:
                        variables[key] = float(value)
                    else:
                        variables[key] = int(value)
                except ValueError:
                    variables[key] = value  # Keep as string if conversion fails

    return variables


