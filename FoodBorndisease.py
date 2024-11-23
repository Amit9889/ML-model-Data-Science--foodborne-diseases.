import pandas as pd
import numpy as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

def load_and_clean_data(filepath):
    """
    Load and perform initial data cleaning
    """
    # Read the dataset
    df = pd.read_csv(filepath)
    
    # Handle missing values
    df = df.fillna(0)  # or use more sophisticated imputation methods
    
    # Convert date columns to datetime if present
    # Adjust column name based on actual dataset
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    return df

def analyze_outbreak_trend(df):
    """
    Q1: Analyze if outbreaks are increasing or decreasing
    """
    # Group by year and count outbreaks
    yearly_outbreaks = df.groupby(df['date'].dt.year)['outbreak_id'].count()
    
    # Perform linear regression to determine trend
    X = yearly_outbreaks.index.values.reshape(-1, 1)
    y = yearly_outbreaks.values
    model = LinearRegression()
    model.fit(X, y)
    
    # Calculate statistical significance
    slope = model.coef_[0]
    r_squared = model.score(X, y)
    
    return yearly_outbreaks, slope, r_squared

def analyze_contaminants(df):
    """
    Q2: Analyze which contaminant caused most illnesses/hospitalizations/deaths
    """
    contaminant_summary = df.groupby('contaminant').agg({
        'illnesses': 'sum',
        'hospitalizations': 'sum',
        'deaths': 'sum'
    }).sort_values(by=['illnesses', 'hospitalizations', 'deaths'], 
                  ascending=False)
    
    return contaminant_summary

def analyze_locations(df):
    """
    Q3: Analyze which food preparation location poses greatest risk
    """
    # Group by location and calculate risk metrics
    location_risk = df.groupby('location').agg({
        'illnesses': ['count', 'sum', 'mean'],
        'hospitalizations': ['sum', 'mean'],
        'deaths': ['sum', 'mean']
    })
    
    # Calculate risk score (you might want to adjust this based on domain knowledge)
    location_risk['risk_score'] = (
        location_risk[('illnesses', 'mean')] * 1 +
        location_risk[('hospitalizations', 'mean')] * 5 +
        location_risk[('deaths', 'mean')] * 20
    )
    
    return location_risk.sort_values('risk_score', ascending=False)

def visualize_results(yearly_outbreaks, contaminant_summary, location_risk):
    """
    Create visualizations for the analysis
    """
    # Create figure with multiple subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15))
    
    # Plot 1: Outbreak Trend
    yearly_outbreaks.plot(kind='line', ax=ax1)
    ax1.set_title('Yearly Outbreak Trend')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Number of Outbreaks')
    
    # Plot 2: Top Contaminants
    top_contaminants = contaminant_summary.head(10)
    top_contaminants['illnesses'].plot(kind='bar', ax=ax2)
    ax2.set_title('Top 10 Contaminants by Illnesses')
    ax2.set_xlabel('Contaminant')
    ax2.set_ylabel('Number of Illnesses')
    
    # Plot 3: Location Risk
    location_risk['risk_score'].plot(kind='bar', ax=ax3)
    ax3.set_title('Location Risk Scores')
    ax3.set_xlabel('Location')
    ax3.set_ylabel('Risk Score')
    
    plt.tight_layout()
    return fig

def main(filepath):
    """
    Main analysis workflow
    """
    # Load and clean data
    df = load_and_clean_data(filepath)
    
    # Q1: Analyze outbreak trends
    yearly_outbreaks, slope, r_squared = analyze_outbreak_trend(df)
    
    # Q2: Analyze contaminants
    contaminant_summary = analyze_contaminants(df)
    
    # Q3: Analyze locations
    location_risk = analyze_locations(df)
    
    # Visualize results
    fig = visualize_results(yearly_outbreaks, contaminant_summary, location_risk)
    
    return {
        'yearly_outbreaks': yearly_outbreaks,
        'trend_slope': slope,
        'trend_r_squared': r_squared,
        'contaminant_summary': contaminant_summary,
        'location_risk': location_risk,
        'visualization': fig
    }

# When you have the dataset, run the analysis like this:
# results = main('path_to_your_dataset.csv')