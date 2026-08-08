from parser import Parser


parser = Parser("config.txt")

try:
    config = parser.parse()
    print(config)

except (ValueError, FileNotFoundError) as e:
    print(e)