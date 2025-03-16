import sys
import io

# Set the encoding for standard output to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def process_arguments(arg1, para1, arg2, para2):
    if arg1 == "sorrybasil" and arg2 == "sorrybasil":
        return "sorry"
    elif arg1 == "newbasil" and arg2 == "sorrybasil":
        return para1
    elif arg1 == "sorrybasil" and arg2 == "newbasil":
        return para2
    elif arg1 == "newbasil" and arg2 == "newbasil":
        return para1
    else:
        return "Invalid input"

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python py4.py <arg1> <para1> <arg2> <para2>")
    else:
        arg1 = sys.argv[1]
        para1 = sys.argv[2]
        arg2 = sys.argv[3]
        para2 = sys.argv[4]
        result = process_arguments(arg1, para1, arg2, para2)
        print(result)