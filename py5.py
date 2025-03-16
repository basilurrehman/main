import sys
import io

# Set the encoding for standard output to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
def process_arguments(arg1, arg2):
    if arg1 == "sorrybasil" and arg2 == "sorrybasil":
        return "sorry"
    elif arg1 == "newbasil" and arg2 == "sorrybasil":
        return "dev"
    elif arg1 == "sorrybasil" and arg2 == "newbasil":
        return "des"
    elif arg1 == "newbasil" and arg2 == "newbasil":
        return "dev"
    else:
        return "Invalid input"

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python py4.py <arg1> <arg2>")
    else:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        result = process_arguments(arg1, arg2)
        print(result)