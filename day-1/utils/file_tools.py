from re import split


def read_file(path):
    """Read file content safely."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.readlines()
    except FileNotFoundError:
        print("ERROR: File not found — please check the name and try again.")
        return None
    except PermissionError:
        print("ERROR: Cannot read file — access denied.")
        return None
    except Exception as error:
        print(f"Unexpected error: {error}")
        return None

def get_words_size(line_array):
    words_total = 0
    for line in line_array:
        words_total += len(line.split())
    return words_total

def get_character_size(line_array):
    char_total = 0
    for line in line_array:
        char_total += len(line)
    return char_total
        


def analyze_text(text):
    properties = {
        "lines" : len(text),
        "words" : get_words_size(text),
        "characters" : get_character_size(text)
    }
    return properties
