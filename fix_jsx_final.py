import re

file_path = "frontend/src/components/figma/ComprehensiveRatingsComparison.tsx"

with open(file_path, 'r') as f:
    lines = f.readlines()

# Remove lines 566-577 (0-indexed: 565-576)
# These contain orphaned old bar code: metric.homeValue.toFixed(1) and old bar divs
lines_to_remove = list(range(565, 577))

new_lines = [line for i, line in enumerate(lines) if i not in lines_to_remove]

with open(file_path, 'w') as f:
    f.writelines(new_lines)

print("✅ Removed orphaned old bar code (lines 566-577)")
print(f"✅ File cleaned: {len(lines)} → {len(new_lines)} lines")
