import os
import re

# Define replacement patterns
replacements = [
    # bg-gray-800 variations
    (r'bg-gray-800/70', 'backdrop-blur-sm'),
    (r'bg-gray-800/60', 'bg-white/5'),
    (r'bg-gray-800/50', 'backdrop-blur-sm'),
    (r'bg-gray-800/40', 'backdrop-blur-sm'),
    (r'bg-gray-800/30', 'backdrop-blur-sm'),
    (r'bg-gray-800/20', 'bg-white/5'),
    (r'hover:bg-gray-800/50', 'hover:bg-white/5'),
    (r'hover:bg-gray-800/60', 'hover:bg-white/5'),
    (r'hover:bg-gray-800/20', 'hover:bg-white/5'),
    (r'hover:bg-gray-800', 'hover:bg-white/10'),
    
    # bg-slate-800 variations
    (r'bg-slate-800/60', 'backdrop-blur-sm'),
    (r'bg-slate-800/50', 'backdrop-blur-sm'),
    (r'bg-slate-800/40', 'backdrop-blur-sm'),
    (r'bg-slate-800/20', 'bg-white/5'),
    (r'hover:bg-slate-800/20', 'hover:bg-white/5'),
    (r'hover:bg-slate-800/80', 'hover:bg-white/10'),
    
    # bg-gray-700 variations
    (r'hover:bg-gray-700/60', 'hover:bg-white/10'),
]

# Directories to process
directories = [
    '/Users/davlenswain/Desktop/Gameday_Graphql_Model/frontend/src/components/figma',
]

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply replacements
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated: {os.path.basename(filepath)}")
            return True
        return False
    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")
        return False

# Process all files
total_updated = 0
for directory in directories:
    if os.path.exists(directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(('.tsx', '.jsx')):
                    filepath = os.path.join(root, file)
                    if process_file(filepath):
                        total_updated += 1

print(f"\n🎯 Total files updated: {total_updated}")
