#!/usr/bin/env python3
"""Modernize all charts in ComprehensiveRatingsComparison.tsx to match Season Summary style"""

import re

file_path = "/Users/davlenswain/Desktop/Gameday_Graphql_Model/frontend/src/components/figma/ComprehensiveRatingsComparison.tsx"

print("🔧 Modernizing ComprehensiveRatingsComparison.tsx charts...")

with open(file_path, 'r') as f:
    content = f.read()

# Remove backdrop-blur
content = re.sub(r'\s*backdrop-blur-sm\s*', ' ', content)

# Increase opacity
content = content.replace('bg-gray-800/40', 'bg-slate-900/40')
content = content.replace('bg-gray-800/60', 'bg-slate-900/60')

# Clean up double spaces
content = re.sub(r'  +', ' ', content)

with open(file_path, 'w') as f:
    f.write(content)

print("   ✅ Removed backdrop-blur")
print("   ✅ Updated background opacity")
print("   ✅ Modernization complete!\n")
