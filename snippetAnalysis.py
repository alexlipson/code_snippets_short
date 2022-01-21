import csv
import sys

# maximum number of characters supported by csv in a snippet
maxInt = sys.maxsize
while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)


fileReadDir = "snippets-dev-reduced.csv"
fileCleanReadDir = "snippets.csv"
fileWriteDir = "snippetsSyntaxNoiseIgnoreLangs.csv"

ignoredLangs = [
    "UNKNOWN", 
    "DOTFILE", 
    "Jupyter", 
    "Text", 
    "CSV", 
    "TSV", 
    "Bash", 
    "Shell", 
    "Markdown", 
    "YAML", 
    "JSON", 
    "PowerShell"
]

def countBasicChars(snippet: str) -> int:
    # counts the number of basic characters in a string
    return sum((
        c.isdigit() or 
        c.isalpha() or 
        c.isspace() or 
        c == '_') 
        for c in snippet)



with open(fileReadDir, errors = "ignore", encoding = "utf-8") as csvfile:
    # replace all nul bytes with empty string
    reader = csv.DictReader(x.replace('\0', '') for x in csvfile)
    with open(fileWriteDir, 'w', newline = '', encoding = "utf-8") as csvfile:
        fieldnames = ["noise_char_ratio", "language", "starting_line"]
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        for row in reader:
            l = len(row["snippet"])
            if row["language"] not in ignoredLangs: # ignore unknown languages
                writer.writerow({
                    'noise_char_ratio': (l - countBasicChars(row['snippet'])) / l,
                    'language': row['language'], 
                    'starting_line': row['starting_line_number']})





    