from utils.file_tools import read_file, analyze_text

def main():
    path = input("Enter file path: ")
    text = read_file(path)

    if text is None:
        return exit()

    stats = analyze_text(text)

    print("\n--- File Analysis ---")
    print(f"Characters: {stats['characters']}")
    print(f"Words: {stats['words']}")
    print(f"Lines: {stats['lines']}")
    print("---------------------")

if __name__ == "__main__":
    main()
