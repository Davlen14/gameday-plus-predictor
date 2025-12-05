#!/usr/bin/env python3
"""
Compute statistical metrics for prediction model performance.
Calculates MAE, RMSE, mean error, median error, standard deviation, and correlation.
"""

import pandas as pd
import numpy as np
from scipy import stats

def compute_metrics(csv_file):
    """
    Compute comprehensive statistical metrics for prediction accuracy.
    
    Args:
        csv_file: Path to CSV file with columns 'Predicted Margin' and 'Actual Margin'
    
    Returns:
        Dictionary containing all computed metrics
    """
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Extract predicted and actual margins
    predicted = df['Predicted Margin'].values
    actual = df['Actual Margin'].values
    
    # Calculate errors (predicted - actual)
    errors = predicted - actual
    
    # Compute metrics
    metrics = {
        'MAE': np.mean(np.abs(errors)),
        'RMSE': np.sqrt(np.mean(errors**2)),
        'Mean Error': np.mean(errors),
        'Median Error': np.median(errors),
        'Std Dev of Errors': np.std(errors, ddof=1),
        'Correlation': stats.pearsonr(predicted, actual)[0],
        'R-squared': stats.pearsonr(predicted, actual)[0]**2,
        'Number of Games': len(predicted)
    }
    
    return metrics, errors, predicted, actual


def print_metrics(metrics):
    """Print metrics in a formatted table."""
    print("\n" + "="*60)
    print(" PREDICTION MODEL PERFORMANCE METRICS")
    print("="*60)
    print(f"\n📊 Sample Size: {metrics['Number of Games']} games\n")
    print("-"*60)
    print("\n🎯 Accuracy Metrics:")
    print(f"   MAE (Mean Absolute Error):        {metrics['MAE']:.2f} points")
    print(f"   RMSE (Root Mean Square Error):    {metrics['RMSE']:.2f} points")
    print("-"*60)
    print("\n📈 Error Distribution:")
    print(f"   Mean Error:                       {metrics['Mean Error']:+.2f} points")
    print(f"   Median Error:                     {metrics['Median Error']:+.2f} points")
    print(f"   Standard Deviation:               {metrics['Std Dev of Errors']:.2f} points")
    print("-"*60)
    print("\n🔗 Correlation Analysis:")
    print(f"   Correlation Coefficient:          {metrics['Correlation']:.4f}")
    print(f"   R-squared:                        {metrics['R-squared']:.4f}")
    print("-"*60)
    
    # Interpretation
    print("\n💡 Interpretation:")
    if abs(metrics['Mean Error']) < 2:
        print(f"   • Model is well-calibrated (mean error near zero)")
    else:
        bias_direction = "overestimates" if metrics['Mean Error'] > 0 else "underestimates"
        print(f"   • Model {bias_direction} margins by ~{abs(metrics['Mean Error']):.1f} points on average")
    
    if metrics['Correlation'] > 0.5:
        print(f"   • Strong positive correlation ({metrics['Correlation']:.3f})")
    elif metrics['Correlation'] > 0.3:
        print(f"   • Moderate positive correlation ({metrics['Correlation']:.3f})")
    else:
        print(f"   • Weak correlation ({metrics['Correlation']:.3f})")
    
    print("\n" + "="*60 + "\n")


def main():
    """Main execution function."""
    csv_file = '/Users/davlenswain/Desktop/Gameday_Graphql_Model/week14_results.csv'
    
    # Compute metrics
    metrics, errors, predicted, actual = compute_metrics(csv_file)
    
    # Print formatted results
    print_metrics(metrics)
    
    # Additional statistics
    print("📊 Additional Statistics:")
    print(f"   Errors within ±7 points:          {np.sum(np.abs(errors) <= 7)} ({100*np.sum(np.abs(errors) <= 7)/len(errors):.1f}%)")
    print(f"   Errors within ±14 points:         {np.sum(np.abs(errors) <= 14)} ({100*np.sum(np.abs(errors) <= 14)/len(errors):.1f}%)")
    print(f"   Errors within ±21 points:         {np.sum(np.abs(errors) <= 21)} ({100*np.sum(np.abs(errors) <= 21)/len(errors):.1f}%)")
    print(f"   Maximum error:                    {np.max(np.abs(errors)):.1f} points")
    print(f"   Minimum error:                    {np.min(np.abs(errors)):.1f} points")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
