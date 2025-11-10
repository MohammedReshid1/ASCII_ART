ASCII Art Viewer

Script that fetches ASCII art from published Google Docs and displays it in terminal.

The way it works is pretty straightforward - Google Docs stores the art in HTML tables with x,y coordinates for each character.

How I built this:

So Google Docs has this format where ASCII art gets stored in tables. Each row has the x coord, character, and y coord:

| x-coordinate | character | y-coordinate |
|--------------|-----------|--------------|
| 0            | █         | 0            |
| 1            | █         | 0            |

The script:
1. Downloads HTML from Google Docs URL
2. Parses HTML to extract table data
3. Converts coordinates to 2D grid
4. Renders the grid

Main components:

GoogleDocsASCIIParser - extends HTMLParser to extract data from tables

Key attributes:
- in_table: bool tracking if we're inside table element
- in_cell: bool for table cell tracking
- current_row: stores current row cells
- table_data: all extracted rows
- cell_content: current cell text

Key methods:
- handle_starttag: fires on opening tags, sets flags for tables/cells
- handle_endtag: fires on closing tags, saves rows/cells to storage
- handle_data: grabs text content from cells

fetch_and_display_ascii_art(url) - main function

Process:
1. Download HTML with requests.get()
2. Parse with HTMLParser
3. Extract coords and chars from table (needs 3 cols: x, char, y)
4. Build 2D grid from max x/y values
5. Place chars at coordinates
6. Print result

main() - entry point that runs test and final URLs

Setup:

pip install requests

Run it:

python3 ascii_art_viewer.py

Or import:
from ascii_art_viewer import fetch_and_display_ascii_art
fetch_and_display_ascii_art("your-url-here")

Output looks like:

ASCII Art:
====
█
█▀▀
█▀▀▀
====

Notes:

Uses coordinate mapping instead of line-by-line reading which works better for sparse ASCII art. Creates empty grid [[' ', ' ', ...]] and maps (x, y, char) to grid[y][x].

Error handling with try/except for bad data and raise_for_status() for HTTP errors.

Parser uses state tracking (in_table, in_cell) to only grab table data. Buffers rows before adding complete ones.

Known issues:
- Only works with first table in doc
- Expects 3 columns exactly
- Single ASCII art block only
- Specific to Google Docs format

Future improvements:
- CLI args for URLs
- Multiple art blocks
- Color support
- File export
- Better errors
