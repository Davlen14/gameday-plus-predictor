#!/usr/bin/env python3
"""
JavaScript Extractor Script
Extracts inline JavaScript from HTML file into a separate .js file
and updates the HTML to reference the external file.
"""

import re
from pathlib import Path


def extract_javascript(html_file: str, js_output_file: str = None):
    """
    Extract JavaScript from HTML file and create a separate JS file.
    
    Args:
        html_file: Path to the HTML file
        js_output_file: Optional output JS filename (defaults to replacing .html with .js)
    """
    html_path = Path(html_file)
    
    # Default JS filename if not provided
    if js_output_file is None:
        js_output_file = html_path.stem + ".js"
    
    js_path = Path(js_output_file)
    
    # Read the HTML file
    print(f"Reading {html_path}...")
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Find the inline script tag and extract JavaScript
    # Looking for <script> ... </script> (not script tags with src attribute)
    pattern = r'<script(?![^>]*src=)>(.*?)</script>'
    matches = list(re.finditer(pattern, html_content, re.DOTALL))
    
    if not matches:
        print("No inline JavaScript found in the HTML file.")
        return
    
    # Extract all inline JavaScript
    all_js = []
    for match in matches:
        js_code = match.group(1).strip()
        if js_code:  # Only add non-empty scripts
            all_js.append(js_code)
    
    if not all_js:
        print("No JavaScript code found to extract.")
        return
    
    # Combine all JavaScript
    combined_js = '\n\n'.join(all_js)
    
    # Write JavaScript to separate file
    print(f"Writing JavaScript to {js_path}...")
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(combined_js)
    
    print(f"✓ Extracted {len(combined_js)} characters of JavaScript")
    
    # Update HTML to reference external JS file
    # Replace inline scripts with external script reference
    new_html = html_content
    
    # Remove all inline script blocks
    for match in reversed(matches):  # Reverse to maintain correct positions
        new_html = new_html[:match.start()] + new_html[match.end():]
    
    # Add external script reference before closing body tag
    script_tag = f'\n    <script src="{js_path.name}"></script>'
    
    # Insert before </body>
    if '</body>' in new_html:
        new_html = new_html.replace('</body>', f'{script_tag}\n</body>')
    else:
        # If no </body>, add before </html>
        new_html = new_html.replace('</html>', f'{script_tag}\n</html>')
    
    # Create backup of original HTML
    backup_path = html_path.with_suffix('.html.backup_js')
    print(f"Creating backup at {backup_path}...")
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Write updated HTML
    print(f"Updating {html_path} with external script reference...")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print("\n✓ Extraction complete!")
    print(f"  - JavaScript file: {js_path}")
    print(f"  - Updated HTML: {html_path}")
    print(f"  - Backup: {backup_path}")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python extract_js.py <html_file> [output_js_file]")
        print("Example: python extract_js.py test.html")
        print("Example: python extract_js.py test.html dashboard.js")
        sys.exit(1)
    
    html_file = sys.argv[1]
    js_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    extract_javascript(html_file, js_file)
