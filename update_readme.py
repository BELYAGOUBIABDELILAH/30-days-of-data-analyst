#!/usr/bin/env python3
"""
Update README.md to show only released days
"""
import json
import re
import sys

def main():
    # Read progress
    with open('progress.json', 'r') as f:
        progress = json.load(f)
    
    released_days = sorted(progress['released_days'])
    
    # Read README
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the project catalog table
    table_start = content.find('| Day | Project | Domain | Stack | Link |')
    table_header_end = content.find('|', table_start + 1)
    table_header_end = content.find('\n', table_header_end)
    
    # Find the end of the table (next --- or ##)
    table_end = content.find('\n---', table_header_end)
    if table_end == -1:
        table_end = content.find('\n##', table_header_end)
    
    # Extract all rows
    table_section = content[table_header_end+1:table_end]
    all_rows = [line.strip() for line in table_section.split('\n') if line.strip().startswith('|')]
    
    # Filter rows to only include released days
    filtered_rows = []
    for row in all_rows:
        # Extract day number from row
        match = re.search(r'\|\s*\*\*(\d+)\*\*', row)
        if match:
            day_num = int(match.group(1))
            if day_num in released_days:
                filtered_rows.append(row)
    
    # Rebuild the table
    new_table = content[:table_header_end+1] + '\n' + '\n'.join(filtered_rows) + '\n'
    new_content = new_table + content[table_end:]
    
    # Write back
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ README updated - showing {len(released_days)} released days")

if __name__ == '__main__':
    main()
