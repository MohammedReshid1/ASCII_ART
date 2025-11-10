# ASCII Art Viewer - Documentation

## Overview

This Python script downloads and displays ASCII art from published Google Docs pages. The Google Docs contain ASCII art data stored in HTML tables with coordinate-based positioning.

## How It Works

### The Problem

Google Docs published pages store ASCII art in an HTML table format where each character has specific x and y coordinates. The table structure looks like:

```
| x-coordinate | character | y-coordinate |
|--------------|-----------|--------------|
| 0            | █         | 0            |
| 1            | █         | 0            |
| 0            | █         | 1            |
```

### The Solution

The script:
1. Downloads the HTML content from the Google Docs URL
2. Parses the HTML to extract the table data
3. Converts coordinate data into a 2D grid
4. Renders the grid as ASCII art in the terminal

## Code Structure

### GoogleDocsASCIIParser Class

This class extends Python's `HTMLParser` to extract data from HTML tables.

**Attributes:**
- `in_table`: Boolean flag tracking if we're currently inside a table element
- `in_cell`: Boolean flag tracking if we're inside a table cell (td)
- `current_row`: List storing the current row's cell contents
- `table_data`: List of lists containing all extracted table rows
- `cell_content`: String accumulating the content of the current cell

**Methods:**

`handle_starttag(tag, attrs)`: Called when the parser encounters an opening HTML tag
- Sets `in_table = True` when encountering `<table>`
- Sets `in_cell = True` when encountering `<td>` inside a table
- Resets `cell_content` for new cells

`handle_endtag(tag)`: Called when the parser encounters a closing HTML tag
- When `</table>` is found, adds any remaining row to `table_data`
- When `</td>` is found, adds the cell content to `current_row`
- When `</tr>` is found, saves the complete row to `table_data`

`handle_data(data)`: Called when the parser encounters text content
- Accumulates text into `cell_content` when inside a cell

### fetch_and_display_ascii_art(url)

Main function that orchestrates the entire process.

**Steps:**

1. **Download**: Uses `requests.get()` to fetch the HTML from the Google Docs URL
2. **Parse**: Creates a parser instance and feeds it the HTML content
3. **Extract**: Loops through the parsed table data and extracts coordinates and characters
   - Each row should have at least 3 elements: x, character, y
   - Converts x and y to integers
   - Stores as tuples: `(x, y, character)`
4. **Build Grid**:
   - Finds the maximum x and y coordinates to determine grid size
   - Creates a 2D list (grid) filled with spaces
   - Places each character at its (x, y) position
5. **Display**: Prints the grid row by row

### main()

Entry point that runs the script with two URLs:
- Test URL: Should display the letter 'F'
- Final URL: Displays the challenge answer

## Requirements

```python
import requests
from html.parser import HTMLParser
```

Install requests if needed:
```bash
pip install requests
```

## Usage

Run the script directly:
```bash
python3 ascii_art_viewer.py
```

Or import and use the function:
```python
from ascii_art_viewer import fetch_and_display_ascii_art

url = "your-google-docs-url"
fetch_and_display_ascii_art(url)
```

## Example Output

```
ASCII Art:
====
█
█▀▀
█▀▀▀
====
```

## Technical Details

### Grid Construction

The script uses a coordinate-based approach rather than reading line-by-line:

1. Creates an empty 2D grid: `[[' ', ' ', ...], [' ', ' ', ...], ...]`
2. Each coordinate tuple `(x, y, char)` maps to `grid[y][x] = char`
3. This approach handles sparse ASCII art efficiently

### Error Handling

- `response.raise_for_status()`: Raises an exception if the HTTP request fails
- `try/except` block: Catches invalid data (non-integer coordinates or missing values)
- Empty data check: Warns if no valid ASCII art data was found

### HTML Parsing Strategy

The HTMLParser processes the document sequentially:
- State tracking (`in_table`, `in_cell`) ensures we only capture data from tables
- Row buffering (`current_row`) collects cell data before adding complete rows
- This stateful approach handles nested HTML structures correctly

## Limitations

- Assumes the first table in the document contains the ASCII art
- Expects exactly 3 columns: x-coordinate, character, y-coordinate
- No support for multiple ASCII art blocks (displays the first one found)
- Requires the specific Google Docs published page format

## Possible Improvements

- Add command-line argument support for custom URLs
- Support multiple ASCII art blocks in one document
- Add color support for terminal output
- Export ASCII art to text files
- Better error messages for malformed data
