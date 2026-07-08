import sys

def check_and_update_paragraph(input_paragraph, file_path='text-design.txt'):
    try:
        # Try reading the file with utf-8 encoding
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                existing_paragraphs = [line.strip() for line in file if line.strip()]
        except UnicodeDecodeError:
            # If utf-8 fails, try reading with a different encoding (e.g., latin-1)
            with open(file_path, 'r', encoding='latin-1') as file:
                existing_paragraphs = [line.strip() for line in file if line.strip()]

        # Check if the paragraph already exists
        if input_paragraph.strip() in existing_paragraphs:
            print("sorrybasil")
        else:
            # Insert new paragraph at the top of the list
            existing_paragraphs.insert(0, input_paragraph.strip())
            print("newbasil")
            
        # Keep only the latest 50 paragraphs
        if len(existing_paragraphs) > 100:
            existing_paragraphs = existing_paragraphs[:100]

        # Write the updated paragraphs back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            for paragraph in existing_paragraphs:
                file.write(paragraph + '\n')

    except FileNotFoundError:
        # If file doesn't exist, create it and write the paragraph
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(input_paragraph.strip() + '\n')
        print("newbasil")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py '<paragraph_to_check>'")
        sys.exit(1)

    input_paragraph = sys.argv[1]
    check_and_update_paragraph(input_paragraph)