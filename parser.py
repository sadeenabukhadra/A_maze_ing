from typing import TypeAlias

ConfigValue: TypeAlias = int | str | bool | tuple[int, int]


class Parser:
    def _init_(self, filename: str) -> None:
        self.filename = filename

    def parse(self) -> dict[str, ConfigValue]:
        config: dict[str, ConfigValue] = {}

        try:
            with open(self.filename, "r") as f:
                for line in f:
                    line = line.strip()

                    if not line:
                        continue

                    if line.startswith("#"):
                        continue

                    if "=" not in line:
                        raise ValueError(f"Invalid configuration line: {line}")

                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()

                    if key == "WIDTH" or key == "HEIGHT":
                        try:
                            config[key] = int(value)
                        except ValueError:
                            raise ValueError(f"{key} must be an integer, got: {value}")

                    elif key == "ENTRY" or key == "EXIT":
                        try:
                            x, y = value.split(",")
                            config[key] = (
                                int(x.strip()),
                                int(y.strip()),
                            )
                        except ValueError:
                            raise ValueError(
                                f"{key} must have format x,y, got: {value}"
                            )

                    elif key == "PERFECT":
                        if value == "True":
                            config[key] = True
                        elif value == "False":
                            config[key] = False
                        else:
                            raise ValueError("PERFECT must be True or False")

                    elif key == "OUTPUT_FILE":
                        if not value:
                            raise ValueError("OUTPUT_FILE cannot be empty")

                        config[key] = value

                    else:
                        raise ValueError(f"Unknown configuration key: {key}")

        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.filename}")

        if not config:
            raise ValueError("Configuration file is empty")

        return config
