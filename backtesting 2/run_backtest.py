#!/usr/bin/env python3
"""
🚀 Quick Backtesting Runner
Simple script to run elite backtesting on your historical data
"""

import os
import sys

def main():
    print("🚀 ELITE ALGORITHM ENHANCEMENT")
    print("="*50)
    
    # Check if we're in the right directory
    if not os.path.exists("all_fbs_games_2024_ENHANCED_20251015_002119.json"):
        print("❌ Could not find 2024 data file")
        print("   Make sure you're running from the backtesting/ directory")
        return
    
    if not os.path.exists("all_fbs_games_2025_ENHANCED_20251015_083540.json"):
        print("❌ Could not find 2025 data file") 
        print("   Make sure you're running from the backtesting/ directory")
        return
    
    print("✅ Found historical data files")
    print("   2024: all_fbs_games_2024_ENHANCED_20251015_002119.json")
    print("   2025: all_fbs_games_2025_ENHANCED_20251015_083540.json")
    
    # Check if elite_backtester exists
    if not os.path.exists("elite_backtester.py"):
        print("❌ Could not find elite_backtester.py")
        return
    
    print("\n🎯 Ready to enhance your algorithm!")
    print("   This will:")
    print("   • Test your model on 1,300+ historical games")
    print("   • Calculate winner accuracy, spread errors, ATS performance")
    print("   • Generate comprehensive performance report")
    print("   • Identify strengths and improvement areas")
    
    print("\n⚡ Starting backtesting...")
    
    # Import and run the backtester
    try:
        import asyncio
        from elite_backtester import main as run_backtest
        
        # Run the backtesting
        asyncio.run(run_backtest())
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you're running from the correct directory")
        print("   Try: cd backtesting && python run_backtest.py")
    except Exception as e:
        print(f"❌ Error running backtest: {e}")

if __name__ == "__main__":
    main()