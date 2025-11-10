ASCII Art Viewer

This script grabs ASCII art from published Google Docs pages and displays it in the terminal. The Google Docs store the art data in HTML tables with x,y coordinates for each character.

How it works:

Google Docs published pages have this weird format where ASCII art is stored in tables. Each row has an x-coordinate, the character, and a y-coordinate. Something like this:

| x-coordinate | character | y-coordinate |
|--------------|-----------|--------------|
| 0            | █         | 0            |
| 1            | █         | 0            |

So the script just:
1. Downloads the HTML from the Google Docs URL
2. Parses the HTML and pulls out the table data
3. Converts those coordinates into a 2D grid
4. Prints out the grid as ASCII art

Code breakdown:

GoogleDocsASCIIParser Class

Extends Python's HTMLParser to pull data from HTML tables.

Attributes:
- in_table: tracks if we're inside a table element
- in_cell: tracks if we're inside a table cell (td)
- current_row: stores the current row's cell contents
- table_data: all the extracted table rows
- cell_content: accumulates content of current cell

Methods:

handle_starttag(tag, attrs) - called when parser hits an opening HTML tag
- Sets in_table = True when it sees <table>
- Sets in_cell = True when it sees <td> inside a table
- Resets cell_content for new cells

handle_endtag(tag) - called when parser hits a closing HTML tag
- When </table> is found, adds remaining row to table_data
- When </td> is found, adds cell content to current_row
- When </tr> is found, saves complete row to table_data

handle_data(data) - called when parser encounters text
- Accumulates text into cell_content when inside a cell

fetch_and_display_ascii_art(url)

Main function that does everything.

Steps:

1. Download - Uses requests.get() to fetch HTML from the Google Docs URL
2. Parse - Creates parser instance and feeds it the HTML
3. Extract - Loops through parsed table data and grabs coordinates and characters
   - Each row needs at least 3 elements: x, character, y
   - Converts x and y to integers
   - Stores as tuples: (x, y, character)
4. Build Grid:
   - Finds max x and y coordinates to figure out grid size
   - Creates 2D list (grid) filled with spaces
   - Places each character at its (x, y) position
5. Display - Prints the grid row by row

main()

Entry point. Runs the script with two URLs - test URL displays 'F', final URL shows the challenge answer.

Requirements:

import requests
from html.parser import HTMLParser

Install requests:
pip install requests

Usage:

Run directly:
python3 ascii_art_viewer.py

Or import it:
from ascii_art_viewer import fetch_and_display_ascii_art
url = "your-google-docs-url"
fetch_and_display_ascii_art(url)

Example output:

ASCII Art:
====
█
█▀▀
█▀▀▀
====

Technical stuff:

The coordinate approach works better than reading line by line. Creates empty 2D grid like [[' ', ' ', ...], [' ', ' ', ...], ...] and each tuple (x, y, char) maps to grid[y][x] = char. Pretty efficient for sparse ASCII art.

Error handling catches HTTP failures with response.raise_for_status(), invalid data with try/except, and warns if no data found.

The HTMLParser goes through the document sequentially. State tracking (in_table, in_cell) makes sure we only grab data from tables. Row buffering (current_row) collects cell data before adding complete rows.

Limitations:

- Only grabs first table in the document
- Expects exactly 3 columns: x-coordinate, character, y-coordinate
- Doesn't handle multiple ASCII art blocks
- Needs specific Google Docs published format

Could be improved:

- Command-line arguments for custom URLs
- Multiple ASCII art blocks support
- Color output
- Export to text files
- Better error messages
