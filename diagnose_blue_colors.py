#!/usr/bin/env python3
"""
Comprehensive Blue Color Diagnostic Tool
Scans all files in the project for blue color references that might be causing unwanted styling.
"""

import os
import re
from pathlib import Path
from collections import defaultdict
import json

class BlueColorScanner:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.results = defaultdict(list)
        self.exclude_dirs = {
            'node_modules', '.git', '__pycache__', '.venv', 'venv', 
            'dist', 'build', '.next', 'coverage', '.pytest_cache'
        }
        self.file_extensions = {
            '.html', '.css', '.js', '.jsx', '.ts', '.tsx', 
            '.py', '.json', '.scss', '.sass', '.less'
        }
        
        # Comprehensive blue color patterns
        self.patterns = {
            # Hex colors
            'hex_blue': re.compile(r'#[0-9a-fA-F]{3,8}(?=\s|;|,|\)|\'|"|})', re.IGNORECASE),
            # RGB/RGBA
            'rgb_blue': re.compile(r'rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*(?:,\s*[\d.]+)?\s*\)', re.IGNORECASE),
            # HSL/HSLA
            'hsl_blue': re.compile(r'hsla?\(\s*\d+\s*,\s*[\d.]+%?\s*,\s*[\d.]+%?\s*(?:,\s*[\d.]+)?\s*\)', re.IGNORECASE),
            # Named colors
            'named_blue': re.compile(r'\b(blue|navy|azure|cyan|aqua|skyblue|steelblue|dodgerblue|cornflowerblue|deepskyblue|lightblue|midnightblue|royalblue|slateblue|mediumblue|darkblue|cadetblue|powderblue|lightcyan|turquoise|darkturquoise|mediumturquoise|paleturquoise|aquamarine|mediumaquamarine|lightseagreen|darkcyan|teal)\b', re.IGNORECASE),
            # Tailwind CSS classes with blue
            'tailwind_blue': re.compile(r'\b(?:bg|text|border|ring|divide|from|via|to|decoration|accent|caret|fill|stroke|outline)-(?:blue|cyan|sky|indigo|slate)-\d+\b', re.IGNORECASE),
            # CSS property with blue in class names
            'class_blue': re.compile(r'\b(?:class|className)=["\']([^"\']*(?:blue|cyan|sky|indigo|slate)[^"\']*)["\']', re.IGNORECASE),
        }
        
    def is_blue_color(self, color_str):
        """Check if a hex/rgb color is predominantly blue."""
        color_str = color_str.strip()
        
        # Check hex colors
        hex_match = re.match(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})', color_str)
        if hex_match:
            hex_value = hex_match.group(1)
            if len(hex_value) == 3:
                hex_value = ''.join([c*2 for c in hex_value])
            
            r = int(hex_value[0:2], 16)
            g = int(hex_value[2:4], 16)
            b = int(hex_value[4:6], 16)
            
            # Blue is dominant if B > R and B > G, and B is significant
            return b > r and b > g and b > 100
        
        # Check RGB values
        rgb_match = re.match(r'rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', color_str)
        if rgb_match:
            r, g, b = map(int, rgb_match.groups())
            return b > r and b > g and b > 100
        
        return False
    
    def scan_file(self, file_path):
        """Scan a single file for blue color references."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            findings = []
            
            for pattern_name, pattern in self.patterns.items():
                matches = pattern.finditer(content)
                for match in matches:
                    matched_text = match.group(0)
                    
                    # For hex and rgb, check if it's actually blue
                    if pattern_name in ['hex_blue', 'rgb_blue']:
                        if not self.is_blue_color(matched_text):
                            continue
                    
                    # Get line number
                    line_num = content[:match.start()].count('\n') + 1
                    
                    # Get context (line containing the match)
                    lines = content.split('\n')
                    context_line = lines[line_num - 1].strip() if line_num <= len(lines) else ""
                    
                    findings.append({
                        'pattern_type': pattern_name,
                        'match': matched_text,
                        'line': line_num,
                        'context': context_line[:150]  # First 150 chars
                    })
            
            return findings
            
        except Exception as e:
            return [{'error': str(e), 'line': 0, 'context': ''}]
    
    def scan_directory(self):
        """Recursively scan all relevant files in the project."""
        print(f"🔍 Scanning project: {self.project_root}\n")
        
        for root, dirs, files in os.walk(self.project_root):
            # Remove excluded directories from traversal
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs]
            
            for file in files:
                file_path = Path(root) / file
                
                # Check if file extension is relevant
                if file_path.suffix not in self.file_extensions:
                    continue
                
                # Skip files larger than 1MB
                if file_path.stat().st_size > 1_000_000:
                    continue
                
                findings = self.scan_file(file_path)
                
                if findings and not any('error' in f for f in findings):
                    relative_path = file_path.relative_to(self.project_root)
                    self.results[str(relative_path)] = findings
    
    def generate_report(self):
        """Generate a detailed report of findings."""
        if not self.results:
            print("✅ No blue color references found!")
            return
        
        print("=" * 80)
        print("🔵 BLUE COLOR DIAGNOSTIC REPORT")
        print("=" * 80)
        print(f"\nTotal files with blue references: {len(self.results)}\n")
        
        # Group by pattern type
        pattern_counts = defaultdict(int)
        for file_findings in self.results.values():
            for finding in file_findings:
                pattern_counts[finding['pattern_type']] += 1
        
        print("📊 Findings by Pattern Type:")
        print("-" * 80)
        for pattern_type, count in sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {pattern_type:20s}: {count:4d} occurrences")
        
        print("\n" + "=" * 80)
        print("📄 DETAILED FILE ANALYSIS")
        print("=" * 80 + "\n")
        
        # Sort files by number of findings
        sorted_files = sorted(self.results.items(), key=lambda x: len(x[1]), reverse=True)
        
        for file_path, findings in sorted_files:
            print(f"\n{'─' * 80}")
            print(f"📁 {file_path}")
            print(f"   Total occurrences: {len(findings)}")
            print(f"{'─' * 80}")
            
            # Group findings by pattern type
            by_type = defaultdict(list)
            for f in findings:
                by_type[f['pattern_type']].append(f)
            
            for pattern_type, items in by_type.items():
                print(f"\n  🔹 {pattern_type} ({len(items)} occurrences):")
                for item in items[:5]:  # Show first 5 of each type
                    print(f"     Line {item['line']:4d}: {item['match']}")
                    print(f"              Context: {item['context'][:100]}")
                
                if len(items) > 5:
                    print(f"     ... and {len(items) - 5} more")
        
        # Save detailed JSON report
        report_path = self.project_root / 'blue_color_report.json'
        with open(report_path, 'w') as f:
            json.dump(dict(self.results), f, indent=2)
        
        print(f"\n{'=' * 80}")
        print(f"💾 Detailed JSON report saved to: {report_path}")
        print(f"{'=' * 80}\n")
    
    def check_external_sources(self):
        """Check for external CSS sources that might inject blue styles."""
        print("\n" + "=" * 80)
        print("🌐 EXTERNAL SOURCE ANALYSIS")
        print("=" * 80 + "\n")
        
        # Find HTML files and check for CDN links
        html_files = list(self.project_root.rglob('*.html'))
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Look for CDN links
                cdn_pattern = re.compile(r'<(?:link|script)[^>]*(?:href|src)=["\']([^"\']*(?:cdn|googleapis|unpkg)[^"\']*)["\']', re.IGNORECASE)
                matches = cdn_pattern.findall(content)
                
                if matches:
                    rel_path = html_file.relative_to(self.project_root)
                    print(f"📄 {rel_path}")
                    print("   External resources:")
                    for match in matches:
                        print(f"     • {match}")
                    print()
                    
            except Exception as e:
                continue
        
        print("\n⚠️  POTENTIAL ISSUES:")
        print("-" * 80)
        print("1. Tailwind CSS CDN uses default blue colors in many utilities")
        print("   - Consider overriding in tailwind.config or using !important")
        print("2. Browser default table styles often include blue links")
        print("   - Add explicit CSS resets for <a> and <table> elements")
        print("3. Lucide icons don't inject styles, but check parent containers")
        print("4. Google Fonts only provide typography, not colors")
        print("-" * 80 + "\n")


def main():
    """Main execution function."""
    project_root = Path(__file__).parent
    
    print("\n" + "=" * 80)
    print("   🔵 BLUE COLOR DIAGNOSTIC TOOL")
    print("   Finding all blue color references in your project")
    print("=" * 80 + "\n")
    
    scanner = BlueColorScanner(project_root)
    scanner.scan_directory()
    scanner.generate_report()
    scanner.check_external_sources()
    
    print("\n" + "=" * 80)
    print("✨ DIAGNOSIS COMPLETE")
    print("=" * 80 + "\n")
    
    print("📋 NEXT STEPS:")
    print("-" * 80)
    print("1. Review blue_color_report.json for all occurrences")
    print("2. Check Tailwind CDN default colors in your HTML")
    print("3. Add explicit CSS overrides for table elements")
    print("4. Use browser DevTools to inspect computed styles")
    print("5. Look for JavaScript that might be injecting blue styles")
    print("-" * 80 + "\n")


if __name__ == "__main__":
    main()
