# Python
from Ingestor.ingestor import Ingestor

files = [
    './_data/DogQuotes/DogQuotesTXT.txt',
    './_data/DogQuotes/DogQuotesDOCX.docx',
    './_data/DogQuotes/DogQuotesPDF.pdf',
    './_data/DogQuotes/DogQuotesCSV.csv',
]

all_quotes = []
for f in files:
    try:
        if Ingestor.can_ingest(f):
            all_quotes.extend(Ingestor.parse(f))
            print(f"Parsed {len(all_quotes)} quotes so far from: {f}")
        else:
            print(f"Cannot ingest: {f}")
    except Exception as e:
        print(f"Failed on {f}: {e}")

print(f"Total quotes: {len(all_quotes)}")
if all_quotes:
    print(all_quotes[0])
