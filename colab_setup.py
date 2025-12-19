# 🚀 NUCLEAR CFP PREDICTOR - COLAB SETUP
# ======================================
# Copy this entire cell to your Google Colab notebook

# Step 1: Install required packages (if needed)
!pip install scikit-learn pandas numpy matplotlib seaborn

# Step 2: Mount Google Drive (adjust paths as needed)
from google.colab import drive
drive.mount('/content/drive')

# Step 3: Copy the nuclear_cfp_dynamic.py file to Colab
# (Upload nuclear_cfp_dynamic.py to your Colab files or Google Drive)

# Step 4: Import the nuclear predictor
exec(open('nuclear_cfp_dynamic.py').read())

# Step 5: Connect to your databases (adjust paths to your actual database locations)
DB_PATHS = {
    'playoff': '/content/drive/MyDrive/Databases/playoff_team_analysis.db',
    'coaches': '/content/drive/MyDrive/Databases/coaches_master.db', 
    'predictions': '/content/drive/MyDrive/Databases/predictions.db'
}

print("🔗 Connecting to databases...")
setup_nuclear_predictor(DB_PATHS['playoff'], DB_PATHS['coaches'], DB_PATHS['predictions'])

# Step 6: Load your trained model (if you saved it)
print("⚡ Loading nuclear model...")
if load_nuclear_model('nuclear_cfp_model.pkl'):
    print("✅ Nuclear model loaded successfully!")
else:
    print("❌ No saved model found. Train your model first!")

# Step 7: Check status
nuclear_status()

# ============================================================================
# 🎯 NOW YOU CAN USE THESE FUNCTIONS INSTANTLY:
# ============================================================================

print("\n🚀 NUCLEAR CFP PREDICTOR IS READY!")
print("\n📋 AVAILABLE FUNCTIONS:")
print("• predict_matchup('Oregon', 'Georgia') - Predict any matchup")
print("• quick_predict('Texas', 'Penn State') - Quick prediction")  
print("• predict_bracket([teams...]) - Analyze full bracket")
print("• team_strength('Indiana') - Get team rating (0-100)")
print("• nuclear_status() - Check predictor status")
print("• demo_predictions() - Run demo with sample matchups")

print("\n🎯 EXAMPLE USAGE:")
print("# Predict Oregon vs Georgia")
print("result = predict_matchup('Oregon', 'Georgia')")
print("print(f\"Winner: {result['winner']} ({result['confidence']:.1f}%)\")")

print("\n# Quick bracket analysis")
print("cfp_bracket = ['Indiana', 'Oregon', 'Georgia', 'Penn State', 'Notre Dame', 'Ohio State', 'Texas', 'Tennessee', 'SMU', 'Clemson', 'Alabama', 'Arizona State']")
print("bracket_results = predict_bracket(cfp_bracket)")
print("print(f\"Predicted Champion: {bracket_results['champion']}\")")

print("\n⚡ Your 4,758,555 datapoint model is ready to predict ANY matchup!")