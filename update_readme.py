#!/usr/bin/env python3
"""
Update README.md to show only released days.
Reads progress.json to determine which days are released,
then filters the project catalog table accordingly.
"""
import json
import re


def main():
    # Read progress
    with open('progress.json', 'r') as f:
        progress = json.load(f)

    released_days = sorted(progress['released_days'])

    # Read README
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the project catalog table header line
    header_line = '| Day | Project | Domain | Stack | Link |'
    table_start = content.find(header_line)
    if table_start == -1:
        print("[ERROR] Could not find project catalog table header.")
        return

    # Find end of the header line
    header_end = content.find('\n', table_start)

    # Find the separator line (e.g. | :--- | :--- | ... |)
    sep_end = content.find('\n', header_end + 1)

    # Find the end of the table (blank line or ---)
    table_end = content.find('\n---', sep_end)
    if table_end == -1:
        table_end = content.find('\n##', sep_end)
    if table_end == -1:
        table_end = len(content)

    # Extract all data rows (skip header and separator)
    table_section = content[sep_end + 1:table_end]
    all_rows = [line.strip() for line in table_section.split('\n') if line.strip().startswith('|')]

    # Filter rows to only include released days
    filtered_rows = []
    for row in all_rows:
        match = re.search(r'\|\s*\*\*(\d+)\*\*', row)
        if match:
            day_num = int(match.group(1))
            if day_num in released_days:
                filtered_rows.append(row)

    # Reconstruct: keep everything up to and including separator, then add filtered rows
    pre_table = content[:sep_end + 1]
    post_table = content[table_end:]

    new_content = pre_table + '\n'.join(filtered_rows) + '\n' + post_table

    # Write back
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[SUCCESS] README updated - showing {len(filtered_rows)} released day(s): {released_days}")


if __name__ == '__main__':
    main()
