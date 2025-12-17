# Read the file
with open('templates/gamedaylive.html', 'r') as f:
    content = f.read()

# Replace the corrupted section
old_js = "window.handleTeamClick = handleTeamClick;\\n            \\n            // Loading Animation Control\\n            const loadingOverlay = document.getElementById('loadingOverlay');\\n            const mainContent = document.getElementById('mainContent');\\n            \\n            // Show loading for 3 seconds (simulating data loading)\\n            setTimeout(() => {\\n                loadingOverlay.classList.add('hidden');\\n                setTimeout(() => {\\n                    mainContent.classList.add('visible');\\n                }, 500);\\n            }, 3000);"

new_js = """window.handleTeamClick = handleTeamClick;
            
            // Loading Animation Control
            const loadingOverlay = document.getElementById('loadingOverlay');
            const mainContent = document.getElementById('mainContent');
            
            // Show loading for 3 seconds (simulating data loading)
            setTimeout(() => {
                loadingOverlay.classList.add('hidden');
                setTimeout(() => {
                    mainContent.classList.add('visible');
                }, 500);
            }, 3000);"""

content = content.replace(old_js, new_js)

# Add closing main-content div
content = content.replace('    </script>\n</body>\n</html>', '''    </script>
    
    </div> <!-- End main-content -->
</body>
</html>''')

# Write back
with open('templates/gamedaylive.html', 'w') as f:
    f.write(content)
    
print("Fixed gamedaylive.html")
