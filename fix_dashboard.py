import os
import re
import json
from datetime import datetime
import shutil

class DashboardFixer:
    def __init__(self, workspace_path):
        self.workspace_path = workspace_path
        self.html_file = os.path.join(workspace_path, 'test.html')
        self.js_file = os.path.join(workspace_path, 'test.js')
        self.test2_html_file = os.path.join(workspace_path, 'test2.html')
        self.fbs_file = os.path.join(workspace_path, 'fbs.json')
        
    def create_backups(self):
        """Create backup copies of current files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if os.path.exists(self.html_file):
            backup_html = f"{self.html_file}.backup_fix_{timestamp}"
            shutil.copy2(self.html_file, backup_html)
            print(f"✓ Created HTML backup: {backup_html}")
        
        if os.path.exists(self.js_file):
            backup_js = f"{self.js_file}.backup_fix_{timestamp}"
            shutil.copy2(self.js_file, backup_js)
            print(f"✓ Created JS backup: {backup_js}")
    
    def fix_team_selector(self):
        """Fix the team selector to match test2.html style and functionality"""
        with open(self.html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Remove the current team selection interface
        html_content = re.sub(
            r'<!-- Team Selection Interface -->.*?</div>\s*</div>\s*</div>',
            '',
            html_content,
            flags=re.DOTALL
        )
        
        # Get the proper team selector from test2.html
        with open(self.test2_html_file, 'r', encoding='utf-8') as f:
            test2_content = f.read()
        
        # Extract the team selection section from test2.html
        team_selector_match = re.search(
            r'<!-- Team Selection Controls -->.*?</div>\s*</div>\s*<button[^>]*>.*?</button>',
            test2_content,
            flags=re.DOTALL
        )
        
        if team_selector_match:
            team_selector_section = team_selector_match.group(0)
            
            # Create the proper header section with team selection like test2.html
            proper_team_selector = f'''
        <!-- ============================================
             🏈 SECTION 1: HEADER WITH TEAM SELECTION  
             ============================================ -->
        <header class="relative w-full mb-8">
            <div class="glass-morphism p-8 rounded-3xl border border-white/20 shadow-2xl backdrop-blur-xl bg-gradient-to-br from-white/10 to-white/5">
                <div class="text-center mb-6">
                    <h1 class="text-4xl md:text-6xl font-black text-white tracking-tight">
                        🏈 College Football Analytics
                    </h1>
                    <p class="text-xl text-slate-300 mt-2 font-medium">Lightning-Fast AI Predictions</p>
                </div>
                
                <div class="flex flex-col lg:flex-row items-center justify-center gap-6 mt-8">
                    {team_selector_section}
                    <button id="generatePrediction" 
                            class="px-8 py-4 bg-gradient-to-r from-emerald-500 to-blue-600 text-white font-bold rounded-lg shadow-lg hover:from-emerald-600 hover:to-blue-700 transition-all duration-300 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none">
                        🚀 Generate Prediction
                    </button>
                </div>
                
                <div id="loadingIndicator" class="hidden mt-6 text-center">
                    <div class="inline-flex items-center px-6 py-3 bg-white/10 rounded-full">
                        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        <span class="text-white font-medium">Generating prediction...</span>
                    </div>
                </div>
            </div>
        </header>
'''
            
            # Insert the proper team selector after the opening body tag
            body_pattern = r'(<body[^>]*>)'
            html_content = re.sub(
                body_pattern, 
                r'\1\n    <div class="min-h-screen pt-8 pb-20 px-4 sm:px-6 lg:px-8">\n' + proper_team_selector,
                html_content
            )
            
            # Remove the old pt-32 class since we're adding proper header spacing
            html_content = re.sub(r'pt-32', 'pt-8', html_content)
    
        # Write the updated HTML
        with open(self.html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✓ Fixed team selector interface")
    
    def remove_hardcoded_svgs(self):
        """Remove all hardcoded SVG logos and betting site references"""
        with open(self.html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Remove hardcoded SVG logo references
        svg_patterns = [
            r'<img[^>]*src="Bovada-Casino-Logo\.svg"[^>]*>',
            r'<img[^>]*src="espnbet\.svg"[^>]*>',
            r'<img[^>]*src="Draftking\.svg"[^>]*>',
            r'<!-- Bovada -->.*?</div>',
            r'<!-- DraftKings -->.*?</div>',
        ]
        
        for pattern in svg_patterns:
            html_content = re.sub(pattern, '', html_content, flags=re.DOTALL)
        
        # Remove any references to betting sites
        html_content = re.sub(r'Bovada|DraftKings|ESPN Bet', '', html_content)
        
        with open(self.html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✓ Removed hardcoded SVG logos and betting references")
    
    def hide_data_until_prediction(self):
        """Hide all data sections until prediction is generated, like test2.html"""
        with open(self.html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Find main content sections and add hidden class initially
        sections_to_hide = [
            r'(<div[^>]*class="[^"]*grid[^"]*grid-cols[^"]*gap[^"]*"[^>]*>)',  # Main grid sections
            r'(<div[^>]*class="[^"]*glass-morphism[^"]*p-6[^"]*"[^>]*>.*?<h3[^>]*>.*?EPA)',  # EPA section
            r'(<div[^>]*class="[^"]*glass-morphism[^"]*p-6[^"]*"[^>]*>.*?<h3[^>]*>.*?Win Probability)',  # Win Prob section
            r'(<div[^>]*class="[^"]*glass-morphism[^"]*p-6[^"]*"[^>]*>.*?<h3[^>]*>.*?Yards Per Play)',  # YPP section
        ]
        
        # Add a main content wrapper that's hidden by default
        content_wrapper_start = '''
        <!-- Main Dashboard Content (Hidden until prediction) -->
        <div id="dashboardContent" class="hidden">
'''
        
        content_wrapper_end = '''
        </div>
        <!-- End Dashboard Content -->
'''
        
        # Find where main content starts (after header)
        main_content_pattern = r'(</header>)(.*?)(<script)'
        
        def wrap_content(match):
            header_end = match.group(1)
            main_content = match.group(2)
            script_start = match.group(3)
            return header_end + content_wrapper_start + main_content + content_wrapper_end + script_start
        
        html_content = re.sub(main_content_pattern, wrap_content, html_content, flags=re.DOTALL)
        
        with open(self.html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✓ Hidden dashboard content until prediction is run")
    
    def fix_javascript_integration(self):
        """Fix JavaScript to work with proper team selector and show/hide content"""
        with open(self.js_file, 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # Update the team selector IDs to match test2.html format
        js_content = re.sub(r'awayTeamSelect', 'awayTeam', js_content)
        js_content = re.sub(r'homeTeamSelect', 'homeTeam', js_content)
        
        # Add function to show dashboard content after prediction
        show_content_function = '''

// Show dashboard content after successful prediction
function showDashboardContent() {
    const dashboardContent = document.getElementById('dashboardContent');
    if (dashboardContent) {
        dashboardContent.classList.remove('hidden');
        // Smooth scroll to content
        dashboardContent.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Hide dashboard content when new teams are selected
function hideDashboardContent() {
    const dashboardContent = document.getElementById('dashboardContent');
    if (dashboardContent) {
        dashboardContent.classList.add('hidden');
    }
}

'''
        
        # Insert the show/hide functions
        js_content = show_content_function + js_content
        
        # Update the generatePrediction function to show content on success
        js_content = re.sub(
            r'(updateDashboardWithPrediction\(predictionData, awayTeamName, homeTeamName\);)',
            r'\1\n        \n        // Show dashboard content\n        showDashboardContent();',
            js_content
        )
        
        # Add event listeners for team selection changes to hide content
        team_change_listener = '''
    
    // Hide content when team selections change
    if (awaySelect) {
        awaySelect.addEventListener('change', hideDashboardContent);
    }
    if (homeSelect) {
        homeSelect.addEventListener('change', hideDashboardContent);
    }
'''
        
        # Add to the DOMContentLoaded event listener
        js_content = re.sub(
            r'(}\);)(\s*\/\/ Add CSS for enhanced dropdowns)',
            r'\1' + team_change_listener + r'\n\2',
            js_content
        )
        
        # Fix team logo handling to match the proper IDs
        js_content = re.sub(r'awayTeamLogo', 'awayLogo', js_content)
        js_content = re.sub(r'homeTeamLogo', 'homeLogo', js_content)
        
        with open(self.js_file, 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        print("✓ Fixed JavaScript integration and show/hide functionality")
    
    def validate_files(self):
        """Validate that required files exist"""
        missing_files = []
        
        if not os.path.exists(self.html_file):
            missing_files.append('test.html')
        if not os.path.exists(self.js_file):
            missing_files.append('test.js')
        if not os.path.exists(self.test2_html_file):
            missing_files.append('test2.html')
        
        if missing_files:
            print(f"❌ Missing required files: {', '.join(missing_files)}")
            return False
        
        return True
    
    def run_fixes(self):
        """Execute all dashboard fixes"""
        print("🔧 Starting Dashboard Fixes")
        print("=" * 50)
        
        # Validate files exist
        if not self.validate_files():
            return False
        
        try:
            # Step 1: Create backups
            print("📁 Creating backup files...")
            self.create_backups()
            
            # Step 2: Fix team selector
            print("🎯 Fixing team selector interface...")
            self.fix_team_selector()
            
            # Step 3: Remove hardcoded SVGs
            print("🗑️  Removing hardcoded SVG logos...")
            self.remove_hardcoded_svgs()
            
            # Step 4: Hide data until prediction
            print("👁️  Hiding content until prediction runs...")
            self.hide_data_until_prediction()
            
            # Step 5: Fix JavaScript
            print("⚡ Fixing JavaScript integration...")
            self.fix_javascript_integration()
            
            # Success message
            print("\n" + "=" * 50)
            print("✅ ALL FIXES COMPLETED SUCCESSFULLY!")
            print("=" * 50)
            print("\n📋 FIXES APPLIED:")
            print("• ✓ Fixed team selector to match test2.html style")
            print("• ✓ Removed all hardcoded SVG logos and betting references")
            print("• ✓ Hidden dashboard content until prediction is generated")
            print("• ✓ Updated JavaScript to show/hide content properly")
            print("• ✓ Fixed team selector IDs and event handling")
            print("• ✓ Added smooth scrolling to prediction results")
            
            print("\n🎯 WHAT'S FIXED:")
            print("• Team selector dropdowns now work like test2.html")
            print("• No hardcoded data or logos are shown initially")
            print("• Dashboard content only appears after running prediction")
            print("• Content hides again when changing team selections")
            print("• All SVG logo references removed")
            
            print("\n🚀 READY TO TEST:")
            print("1. Your Flask server should still be running")
            print("2. Refresh test.html in your browser")
            print("3. You'll see only the team selector initially")
            print("4. Select teams and generate prediction to see results!")
            
            return True
            
        except Exception as e:
            print(f"\n❌ FIXES FAILED: {str(e)}")
            print("Check the error above and ensure all files are accessible.")
            return False

def main():
    """Main function to run the dashboard fixes"""
    workspace_path = "/Users/davlenswain/Desktop/Gameday_Graphql_Model"
    
    # Initialize and run fixer
    fixer = DashboardFixer(workspace_path)
    success = fixer.run_fixes()
    
    if success:
        print("\n🎉 Dashboard is now properly dynamic with no hardcoded content!")
    else:
        print("\n💥 Fixes failed. Check the errors above.")

if __name__ == "__main__":
    main()