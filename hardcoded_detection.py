#!/usr/bin/env python3
"""
Hardcoded Data Detection Script - Scan for static/hardcoded values that should be dynamic
"""

import os
import re
from pathlib import Path

def scan_for_hardcoded_data():
    """Scan Python files for common hardcoded patterns"""
    
    base_path = Path("/Users/davlenswain/Desktop/Gameday_Graphql_Model")
    
    # Patterns that indicate hardcoded data
    hardcoded_patterns = {
        'team_names': [
            r'\b(USC|Notre Dame|Lincoln Riley|Marcus Freeman)\b',
            r'\b(Trojans|Fighting Irish)\b',
            r'\b(Southern California|University of Notre Dame)\b'
        ],
        'coach_names': [
            r'\b(Lincoln Riley|Marcus Freeman|Brian Kelly)\b',
            r'\bCoach:\s*[A-Z][a-z]+\s+[A-Z][a-z]+\b'
        ],
        'static_scores': [
            r'\b(24-17|31-14|42-21)\b',  # Common static scores
            r'Score:\s*\d+-\d+',
            r'Final:\s*\d+-\d+'
        ],
        'static_stats': [
            r'\b\d+\.\d+\s*(yards|touchdowns|completions)\b',
            r'Passing:\s*\d+/\d+',
            r'Rushing:\s*\d+\s*yards'
        ],
        'hardcoded_predictions': [
            r'Win Probability:\s*\d+\.\d+%',
            r'Spread:\s*[+-]?\d+\.\d+',
            r'Total:\s*\d+\.\d+'
        ]
    }
    
    # Files to scan
    python_files = []
    for ext in ['*.py']:
        python_files.extend(base_path.glob(f'**/{ext}'))
    
    print("🔍 HARDCODED DATA DETECTION SCAN")
    print("=" * 80)
    print(f"📁 Scanning {len(python_files)} Python files...")
    
    findings = {}
    total_issues = 0
    
    for file_path in python_files:
        # Skip certain directories and files
        skip_patterns = [
            '__pycache__', 
            '.git', 
            'node_modules',
            'test_',  # Test files might have legitimate hardcoded data
            'component_mapping_analysis.py',  # Our own analysis scripts
            'hardcoded_detection.py'  # This script itself
        ]
        
        if any(skip in str(file_path) for skip in skip_patterns):
            continue
            
        try:
            content = file_path.read_text(encoding='utf-8')
            file_issues = []
            
            for category, patterns in hardcoded_patterns.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        # Get line number
                        line_num = content[:match.start()].count('\n') + 1
                        line_content = content.split('\n')[line_num - 1].strip()
                        
                        file_issues.append({
                            'category': category,
                            'pattern': pattern,
                            'match': match.group(),
                            'line': line_num,
                            'line_content': line_content
                        })
            
            if file_issues:
                findings[str(file_path)] = file_issues
                total_issues += len(file_issues)
                
        except Exception as e:
            print(f"⚠️  Error reading {file_path}: {e}")
    
    # Report findings
    if findings:
        print(f"\n🚨 FOUND {total_issues} POTENTIAL HARDCODED ISSUES")
        print("=" * 80)
        
        for file_path, issues in findings.items():
            rel_path = Path(file_path).relative_to(base_path)
            print(f"\n📄 {rel_path} ({len(issues)} issues)")
            print("-" * 60)
            
            by_category = {}
            for issue in issues:
                cat = issue['category']
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(issue)
            
            for category, cat_issues in by_category.items():
                print(f"\n🎯 {category.upper().replace('_', ' ')} ({len(cat_issues)} found):")
                for issue in cat_issues[:5]:  # Show first 5 of each category
                    print(f"   Line {issue['line']:3d}: {issue['match']}")
                    print(f"            {issue['line_content'][:80]}{'...' if len(issue['line_content']) > 80 else ''}")
                
                if len(cat_issues) > 5:
                    print(f"   ... and {len(cat_issues) - 5} more")
    
    else:
        print("\n✅ NO HARDCODED DATA PATTERNS FOUND!")
        print("All files appear to use dynamic data sources.")
    
    return findings

def check_specific_files():
    """Check specific files known to have had issues"""
    
    problem_files = [
        'formatter.py',
        'app.py', 
        'run.py',
        'graphqlpredictor.py'
    ]
    
    base_path = Path("/Users/davlenswain/Desktop/Gameday_Graphql_Model")
    
    print(f"\n🎯 SPECIFIC FILE ANALYSIS")
    print("=" * 80)
    
    for filename in problem_files:
        file_path = base_path / filename
        
        if not file_path.exists():
            print(f"❌ {filename} - File not found")
            continue
            
        try:
            content = file_path.read_text()
            
            # Check for USC/Notre Dame references
            usc_nd_matches = re.findall(r'\b(USC|Notre Dame|Lincoln Riley|Marcus Freeman|Trojans|Fighting Irish)\b', content, re.IGNORECASE)
            
            # Check for hardcoded return statements
            hardcoded_returns = re.findall(r'return\s*{[^}]*["\']USC["\'][^}]*}', content, re.IGNORECASE | re.DOTALL)
            
            # Check for static team data
            static_data = re.findall(r'["\'][A-Z][a-z]+\s+[A-Z][a-z]+["\'].*:\s*["\'][A-Z]', content)
            
            print(f"\n📄 {filename}")
            print(f"   🏈 USC/Notre Dame references: {len(set(usc_nd_matches))}")
            print(f"   📊 Hardcoded returns: {len(hardcoded_returns)}")  
            print(f"   📋 Static data patterns: {len(static_data)}")
            
            if usc_nd_matches:
                print(f"   ⚠️  Found: {', '.join(set(usc_nd_matches))}")
                
            if hardcoded_returns:
                print(f"   🚨 Hardcoded return detected!")
                
        except Exception as e:
            print(f"❌ {filename} - Error reading file: {e}")

def check_import_usage():
    """Check what formatter is being imported/used"""
    
    base_path = Path("/Users/davlenswain/Desktop/Gameday_Graphql_Model")
    
    print(f"\n🔗 IMPORT ANALYSIS") 
    print("=" * 80)
    
    files_to_check = ['app.py', 'run.py', 'test_fix.py']
    
    for filename in files_to_check:
        file_path = base_path / filename
        
        if not file_path.exists():
            continue
            
        try:
            content = file_path.read_text()
            
            # Check formatter imports
            formatter_imports = re.findall(r'from\s+(\w+)\s+import.*format', content, re.IGNORECASE)
            run_imports = re.findall(r'from\s+run\s+import', content)
            formatter_direct = re.findall(r'import\s+formatter', content)
            
            print(f"\n📄 {filename}")
            if formatter_imports:
                print(f"   📦 Formatter imports from: {formatter_imports}")
            if run_imports:
                print(f"   ✅ Using run.py imports: {len(run_imports)}")
            if formatter_direct:
                print(f"   ⚠️  Direct formatter import: {len(formatter_direct)}")
            if not any([formatter_imports, run_imports, formatter_direct]):
                print(f"   📋 No formatter-related imports")
                
        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")

if __name__ == "__main__":
    print("🎯 GAMEDAY+ HARDCODED DATA DETECTION")
    print("=" * 80)
    
    # Scan for hardcoded patterns
    findings = scan_for_hardcoded_data()
    
    # Check specific problematic files
    check_specific_files()
    
    # Check import usage
    check_import_usage()
    
    print(f"\n🎯 SUMMARY")
    print("=" * 80)
    
    if findings:
        print(f"🚨 Found potential issues in {len(findings)} files")
        print("   Review the files above for hardcoded data that should be dynamic")
        print("   Focus on formatter.py and any files importing from it")
    else:
        print("✅ No obvious hardcoded patterns detected")
        
    print("\n💡 RECOMMENDATIONS:")
    print("   1. Ensure app.py imports from run.py (not formatter.py)")
    print("   2. Verify formatter.py is not used in production code") 
    print("   3. Check that all team data comes from API calls")
    print("   4. Test with multiple team combinations")