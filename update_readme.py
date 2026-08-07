#!/usr/bin/env python3
"""
Script to automatically update README.md with project catalog and themes
based on existing Day folders in the repository.
"""

import os
import re
import json
from urllib.parse import quote

# Project metadata mapping
PROJECT_METADATA = {
    1: {"name": "Tesla Stock Analysis", "domain": "Time Series", "stack": "Pandas, Matplotlib, Seaborn"},
    2: {"name": "Zomato Restaurant Analysis", "domain": "Food Industry", "stack": "Pandas, NumPy, Seaborn"},
    3: {"name": "Amazon Electronics Analysis", "domain": "E-commerce", "stack": "Pandas, Power BI"},
    4: {"name": "Global GDP Analysis", "domain": "Macroeconomics", "stack": "Pandas, SciPy, Scikit-learn"},
    5: {"name": "Spotify Music Analysis", "domain": "Clustering", "stack": "Scikit-learn, Power BI"},
    6: {"name": "Sales Dashboard", "domain": "Business Intelligence", "stack": "Power BI, Excel"},
    7: {"name": "Insurance Analysis", "domain": "Regression", "stack": "Scikit-learn, XGBoost"},
    8: {"name": "Twitter Stock Analysis", "domain": "Time Series", "stack": "Pandas, Matplotlib"},
    9: {"name": "Economy Indicators", "domain": "Macroeconomics", "stack": "Pandas, Seaborn"},
    10: {"name": "Bank Bankruptcy Analysis", "domain": "Classification", "stack": "Scikit-learn, Logistic Regression"},
    11: {"name": "Internet Usage Clustering", "domain": "Clustering", "stack": "Scikit-learn, Pandas"},
    12: {"name": "Sales Performance Analysis", "domain": "Sales Analytics", "stack": "Pandas, Matplotlib"},
    13: {"name": "Sales Team Performance", "domain": "Sales Analytics", "stack": "Pandas, Seaborn"},
    14: {"name": "Supermarket Analysis", "domain": "Retail", "stack": "Pandas, NumPy"},
    15: {"name": "Romanian Energy Prices", "domain": "Energy", "stack": "Pandas, Matplotlib"},
    16: {"name": "Credit Card Analysis", "domain": "Finance", "stack": "Pandas, Seaborn"},
    17: {"name": "Cricket Rankings Analysis", "domain": "Sports", "stack": "Pandas, NumPy"},
    18: {"name": "Delhi Air Quality", "domain": "Environment", "stack": "Pandas, Matplotlib"},
    19: {"name": "YouTube Channels Analysis", "domain": "Media", "stack": "Pandas, Seaborn"},
    20: {"name": "Movie Analysis", "domain": "Entertainment", "stack": "Pandas, Matplotlib"},
    21: {"name": "Cisco Stock Analysis", "domain": "Time Series", "stack": "Pandas, Matplotlib, Seaborn"},
    22: {"name": "Emergency Calls Analysis", "domain": "Public Safety", "stack": "Pandas, Seaborn"},
    23: {"name": "Global Terrorism Analysis", "domain": "Security", "stack": "Pandas, Openpyxl"},
    24: {"name": "Global Terrorism Dashboard", "domain": "Visualization", "stack": "Power BI"},
    25: {"name": "Horror Movies Analysis", "domain": "Entertainment", "stack": "Pandas, Seaborn"},
    26: {"name": "Billionaire Wealth Analysis", "domain": "Finance", "stack": "Pandas, NumPy"},
    27: {"name": "COVID-19 Analysis", "domain": "Public Health", "stack": "SQL, Excel"},
    28: {"name": "Medical Conditions Analysis", "domain": "Healthcare", "stack": "Scikit-learn, Random Forest"},
    29: {"name": "Retail Customer Analytics", "domain": "Segmentation", "stack": "Pandas, NumPy"},
    30: {"name": "Used Car Price Analysis", "domain": "Regression", "stack": "Scikit-learn, XGBoost"},
}

# Theme mapping for each project
DOMAIN_TO_THEME = {
    "Time Series": "Financial Analysis",
    "Food Industry": "Business Analytics",
    "E-commerce": "Business Analytics",
    "Macroeconomics": "Economic Analysis",
    "Clustering": "Machine Learning",
    "Business Intelligence": "Data Visualization",
    "Regression": "Machine Learning",
    "Classification": "Banking & Finance",
    "Sales Analytics": "Business Analytics",
    "Retail": "Business Analytics",
    "Energy": "Energy & Environment",
    "Finance": "Banking & Finance",
    "Sports": "Entertainment & Media",
    "Environment": "Energy & Environment",
    "Media": "Entertainment & Media",
    "Entertainment": "Entertainment & Media",
    "Public Safety": "Public Safety",
    "Security": "Public Safety",
    "Visualization": "Data Visualization",
    "Public Health": "Healthcare Analytics",
    "Healthcare": "Healthcare Analytics",
    "Segmentation": "Machine Learning",
}

# Theme categories and descriptions
THEME_DESCRIPTIONS = {
    "Financial Analysis": "Stock price trends and volatility",
    "Business Analytics": "Restaurant ratings, electronics sales, and sales team performance",
    "Entertainment & Media": "Audio clustering, YouTube metrics, movie rating patterns",
    "Healthcare Analytics": "Insurance claims modeling and chronic condition classification",
    "Banking & Finance": "Bankruptcy prediction and credit card transaction analysis",
    "Energy & Environment": "Delhi AQI tracking and Romanian fuel price trends",
    "Data Visualization": "Power BI dashboards for business intelligence",
    "Public Safety": "Emergency call patterns and global terrorism indicators",
    "Machine Learning": "RFM segmentation, K-Means clustering, and price regression",
    "Economic Analysis": "Macroeconomic indicators and COVID-19 time series",
}


def get_existing_days():
    """Scan directory for existing Day folders."""
    days = []
    for item in os.listdir('.'):
        match = re.match(r'Day (\d+) -', item)
        if match and os.path.isdir(item):
            day_num = int(match.group(1))
            days.append((day_num, item))
    return sorted(days)


def find_notebook_or_file(folder):
    """Find the main notebook or file in a day folder."""
    day_num = int(re.search(r'Day (\d+)', folder).group(1))
    
    # Check for common patterns
    patterns = [
        f"Day-{day_num}.ipynb",
        f"Day {day_num}.ipynb",
        f"day-{day_num}.ipynb",
        "*.pbix",  # Power BI files
        "*.sql",   # SQL files
        "*.py",    # Python scripts
    ]
    
    for pattern in patterns:
        if '*' in pattern:
            import glob
            files = glob.glob(os.path.join(folder, pattern))
            if files:
                return os.path.relpath(files[0], folder)
        else:
            path = os.path.join(folder, pattern)
            if os.path.exists(path):
                return pattern
    
    # Fallback: find any notebook
    for file in os.listdir(folder):
        if file.endswith('.ipynb'):
            return file
    
    return None


def generate_catalog_table(existing_days):
    """Generate the markdown table for project catalog."""
    lines = ["| Day | Project | Domain | Stack | Link |"]
    lines.append("| :---: | :--- | :--- | :--- | :---: |")
    
    for day_num, folder in existing_days:
        if day_num not in PROJECT_METADATA:
            continue
            
        meta = PROJECT_METADATA[day_num]
        notebook = find_notebook_or_file(folder)
        
        folder_url = quote(folder)
        project_link = f"[{meta['name']}](./{folder_url})"
        
        if notebook:
            file_url = quote(f"{folder}/{notebook}")
            if notebook.endswith('.ipynb'):
                link_text = "Notebook"
            elif notebook.endswith('.pbix'):
                link_text = "Dashboard"
            elif notebook.endswith('.sql'):
                link_text = "SQL"
            else:
                link_text = "Code"
            file_link = f"[{link_text}](./{file_url})"
        else:
            file_link = "[View](./{})".format(folder_url)
        
        lines.append(f"| **{day_num:02d}** | {project_link} | {meta['domain']} | {meta['stack']} | {file_link} |")
    
    return '\n'.join(lines)


def generate_themes(existing_days):
    """Generate project themes based on available projects."""
    if not existing_days:
        return "*Themes will appear as projects are released*"
    
    # Collect themes from released projects
    active_themes = set()
    for day_num, _ in existing_days:
        if day_num in PROJECT_METADATA:
            domain = PROJECT_METADATA[day_num]['domain']
            if domain in DOMAIN_TO_THEME:
                active_themes.add(DOMAIN_TO_THEME[domain])
    
    # Generate theme list in order
    lines = []
    for theme in THEME_DESCRIPTIONS.keys():
        if theme in active_themes:
            lines.append(f"- **{theme}** — {THEME_DESCRIPTIONS[theme]}")
    
    return '\n'.join(lines) if lines else "*Themes will appear as projects are released*"


def update_readme():
    """Update README.md with current project status."""
    readme_path = 'README.md'
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get existing days
    existing_days = get_existing_days()
    
    # Generate new content
    catalog_table = generate_catalog_table(existing_days)
    themes_content = generate_themes(existing_days)
    
    # Replace catalog section
    catalog_pattern = r'(<!-- AUTO-GENERATED-CATALOG-START -->).*?(<!-- AUTO-GENERATED-CATALOG-END -->)'
    new_catalog = f'\\1\n{catalog_table}\n\\2'
    content = re.sub(catalog_pattern, new_catalog, content, flags=re.DOTALL)
    
    # Replace themes section
    themes_pattern = r'(<!-- AUTO-GENERATED-THEMES-START -->).*?(<!-- AUTO-GENERATED-THEMES-END -->)'
    new_themes = f'\\1\n{themes_content}\n\\2'
    content = re.sub(themes_pattern, new_themes, content, flags=re.DOTALL)
    
    # Write back
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Updated README with {len(existing_days)} projects")


if __name__ == '__main__':
    update_readme()
