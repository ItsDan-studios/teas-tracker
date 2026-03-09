import json
import csv
import sys

def convert(input_json_path, output_csv_path):
    # Depending on how the JSON is captured, it might be an array or embedded in a text file.
    # This tries standard JSON loading, falling back to attempting to extract valid JSON from text.
    with open(input_json_path, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # Fallback: find the first '[' and last ']' if it was surrounded by markdown blocks
        start = content.find('[')
        end = content.rfind(']') + 1
        if start != -1 and end != 0:
            data = json.loads(content[start:end])
        else:
            print("Error: Could not parse JSON from the provided file.")
            sys.exit(1)

    with open(output_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Phone", "Website", "Email", "Rating", "Reviews"])
        
        for item in data:
            name = item.get("title", "")
            phone = item.get("phone", "")
            website = item.get("website", "")
            emails = item.get("emails", [])
            email = emails[0] if emails else ""
            rating = item.get("totalScore", "")
            reviews = item.get("reviewsCount", "")
            writer.writerow([name, phone, website, email, rating, reviews])
            
    print(f"Successfully converted {len(data)} leads to {output_csv_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_json_to_csv.py <input_json_file> <output_csv_file>")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
