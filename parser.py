from typing import TypeAlias


class Parser:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def parse(self) -> dict[str, ConfigValue]:

        ConfigValue: TypeAlias = int | str | bool | tuple[int, int]
        config: dict[str, ConfigValue] = {}

        with open(self.filename, "r") as f:
            for line in f:
                line = line.strip()

                if not line:
                    continue

                elif line.startswith("#"):
                    continue

                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                if key == "WIDTH" or key == "HEIGHT":
                    config[key] = int(value)

                elif key == "ENTRY" or key == "EXIT":
                    x, y = value.split(",")
                    config[key] = (int(x), int(y))

                elif key == "PERFECT":
                    config[key] = value == "True"

                elif key == "OUTPUT_FILE":
                    config[key] = value

        return config