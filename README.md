# Meme Generator & Quote Engine

Generate captioned memes from images and quotes. You can:
- Use built-in quote datasets (TXT, DOCX, PDF, CSV).
- Provide your own quote text and author.
- Select an image or let the app pick a random one from a configured category.

## Features

- CLI to generate a meme image with a quote.
- Quote ingestion from multiple file formats via a unified Ingestor interface.
- Configurable image category via a simple config.ini file.
- Modular components: MemeEngine for image composition and QuoteEngine for quote representation.

## Requirements

- Python 3.13.5
- Packages:
  - click
  - flask
  - jinja2
  - pillow
  - requests
  - werkzeug

You can install them with pip:
```
 pip3 install pillow flask click jinja2 requests werkzeug
```
## Project Layout (high-level)

- meme.py — CLI entry point for generating memes.
- MemeEngine/ — image composition (placing text onto an image, outputting a meme).
- QuoteEngine/ — quote representation and utilities.
- Ingestor — parses quotes from TXT/DOCX/PDF/CSV.
- _data/ — example images and quotes.
  - _data/photos/dog/
  - _data/photos/sadhguru/
  - _data/DogQuotes/ (TXT, DOCX, PDF, CSV datasets)
- config.ini — optional configuration (e.g., image category).
- tmp/ — output directory for generated memes.

Note: Exact module paths may vary depending on your local structure.

## Installation

1) Clone or copy the project files locally.
2) Ensure you have Python 3.13.5.
3) Install dependencies:
```
 pip3 install pillow flask click jinja2 requests werkzeug
```

4) Verify you have the _data/ folders and files (images and quotes) in place.

## Configuration

Create a config.ini in the project root (same folder as meme.py):
```
ini [DEFAULT] category = sadhguru
```


Valid categories in the default implementation:
- dog
- sadhguru

This determines which image pool is used when no image path is passed.

## Usage

### 1) Generate a meme with a random image and random quote
```
python3 meme.py
```

This will:
- Read config.ini to determine the category (dog or sadhguru).
- Pick a random image from that category folder.
- Pick a random quote from the built-in datasets.
- Output the absolute path of the generated meme (also saved to ./tmp).

### 2) Generate a meme with a specific image and random quote
```
python3 meme.py --path ./_data/photos/dog/xander_1.jpg
```
Notes:
- Use the full or relative path to an image file.
- The image must be a supported format (e.g., JPG, PNG).

### 3) Generate a meme with your own quote and author (random image)
```
python3 meme.py --body "Life begins at the end of your comfort zone." --author "Neale Donald Walsch"
```

The will:
- Use the configured category to pick a random image.
- Place your provided quote text and author.

If you provide --body, you must also provide --author.

### 4) Generate a meme with your own quote and author using a specific image
```
python3 meme.py
--path ./_data/photos/sadhguru/sg_2.jpg
--body "Inner engineering is a technology for well-being."
--author "Sadhguru"
```

### CLI Argument Reference

- --path: Path to an image file. If omitted, a random one is chosen from the configured category.
- --body: Quote text. If omitted, a random quote is selected from datasets.
- --author: Quote author. Required when --body is provided.

## Programmatic Usage

If you want to call it from Python and get the output path of the generated meme:
python from meme import generate_meme
### Random image and random quote
`out_path = generate_meme() print(out_path)`
### Specific image, random quote
`out_path = generate_meme(path=["./_data/photos/dog/xander_1.jpg"]) print(out_path)`
### Custom quote, random image
`out_path = generate_meme(body="Simplicity is the soul of efficiency.", author="Austin Freeman") print(out_path)`


## Output

Generated memes are saved under ./tmp, and the program prints the full path to the generated image.

## Troubleshooting

- No such file or directory for images:
  - Ensure the path you pass-to --path exists.
  - Ensure _data/photos/<category>/ contains images if you rely on random selection.
- Missing category in config.ini:
  - The app can use a default fallback (e.g., "sadhguru"), but adding a config.ini is recommended.
- Unsupported quote files:
  - Ensure the Ingestor supports the file format. The default setup typically handles TXT, DOCX, PDF, and CSV.
- Fonts on different platforms:
  - If MemeEngine relies on system fonts and fails, make sure appropriate fonts are installed or the code uses a bundled font.

## License

MIT (or your chosen license).

## Acknowledgments

- Pillow for image manipulation.
- The included datasets and images for testing/demo purposes.
