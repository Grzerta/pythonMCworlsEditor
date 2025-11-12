import json
from nbtlib import nbt

def main():
    print("Welcome to the SNBT/JSON Parser!")
    choice = input("Enter '1' to parse SNBT or '2' to parse JSON: ")

    if choice == '1':
        snbt_input = input("Enter SNBT data: ")
        try:
            parsed_data = parse_snbt(snbt_input)
            print("Parsed Data:", json.dumps(parsed_data, indent=4))
        except Exception as e:
            print(f"Error parsing SNBT: {e}")

    elif choice == '2':
        json_input = input("Enter JSON data: ")
        try:
            parsed_data = json.loads(json_input)
            print("Parsed Data:", json.dumps(parsed_data, indent=4))
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")

    else:
        print("Invalid choice. Please enter '1' or '2'.")

def parse_snbt(snbt_string):
    return nbt.load(snbt_string)

if __name__ == "__main__":
    main()