#!/usr/bin/env python3

import requests
from html.parser import HTMLParser


class GoogleDocsASCIIParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_cell = False
        self.current_row = []
        self.table_data = []
        self.cell_content = ""

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.in_table = True
        elif tag == "td" and self.in_table:
            self.in_cell = True
            self.cell_content = ""

    def handle_endtag(self, tag):
        if tag == "table":
            self.in_table = False
            if self.current_row:
                self.table_data.append(self.current_row)
                self.current_row = []
        elif tag == "td" and self.in_cell:
            self.in_cell = False
            self.current_row.append(self.cell_content.strip())
        elif tag == "tr" and self.in_table:
            if self.current_row:
                self.table_data.append(self.current_row)
                self.current_row = []

    def handle_data(self, data):
        if self.in_cell:
            self.cell_content += data


def fetch_and_display_ascii_art(url):
    print(f"Fetching document from: {url}\n")

    resp = requests.get(url)
    resp.raise_for_status()
    html = resp.text

    parser = GoogleDocsASCIIParser()
    parser.feed(html)

    points = []

    for row in parser.table_data:
        if len(row) >= 3:
            try:
                x = int(row[0])
                ch = row[1]
                y = int(row[2])
                points.append((x, y, ch))
            except:
                continue

    if not points:
        print("No ASCII art data found in the document.")
        return

    max_x = max(p[0] for p in points)
    max_y = max(p[1] for p in points)

    grid = []
    for i in range(max_y + 1):
        grid.append([' '] * (max_x + 1))

    for x, y, ch in points:
        grid[max_y - y][x] = ch

    print("ASCII Art:")
    print("=" * (max_x + 1))
    for row in grid:
        print(''.join(row))
    print("=" * (max_x + 1))
    print()


def main():
    test_url = "https://docs.google.com/document/d/e/2PACX-1vSmVmKxyqWZ-piMuUS251weVuIABoqm7tSyFP-GqpM9atKcV2ShZMmt5mA2-uDg_9kVFS7Q1jeB84m0/pub"

    final_url = "https://docs.google.com/document/d/e/2PACX-1vS6_z9WRAQj3MfAjR2_G0V72OQREUCN8CKGmHWsVBv4LG3N-VVOh4uIjgGNJ8ZwHxslmGp7F8_bhTuF/pub"

    print("Testing with test URL (should show 'F'):")
    print("-" * 50)
    fetch_and_display_ascii_art(test_url)

    print("\n" + "=" * 50)
    print("Fetching final ASCII art:")
    print("=" * 50)
    fetch_and_display_ascii_art(final_url)


if __name__ == "__main__":
    main()
    
