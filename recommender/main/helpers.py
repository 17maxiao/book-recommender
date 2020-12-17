import csv
from pathlib import Path

def getresults(title):
    matchedbooks = []
    base_path = Path(__file__).parent
    filepath = (base_path / "./df_books.csv").resolve()
    reader = csv.reader(open(filepath))
    for row in reader:
        curr = row[4]
        if title.lower() in curr.lower():
            matchedbooks.append(curr)
    for book in matchedbooks:
        print(book)
    return matchedbooks