from parser import Parser

parser = Parser("config.txt")
config = parser.parse()

print(config)
