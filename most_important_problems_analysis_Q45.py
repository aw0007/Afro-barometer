import pandas as pd
import pyreadstat
import os
import matplotlib.pyplot as plt
import seaborn as sns

# File path to the dataset
file_path = r"C:\Users\massa\Desktop\MiniProjet\Afro barometre\Data\R9.Merge_39ctry.20Nov23.final.release_Updated.25Oct24 2 2.sav"

# Load the SPSS file
df, meta = pyreadstat.read_sav(file_path)

# Define the variables of interest (including location variables)
variables_of_interest = ['Q45PT1', 'Q45PT2', 'Q45PT3', 'COUNTRY', 'REGION', 'URBRUR']  # Add relevant location variables
variables_of_interest = [var.upper() for var in variables_of_interest if var.upper() in df.columns]

# Calculate the total number of individuals in the dataset
nb_indivi = len(df)

# Filter the dataset for the selected variables
filtered_df = df[variables_of_interest]

# Recode the COUNTRY variable based on the codebook
country_mapping = {
    2: "Angola", 3: "Benin", 4: "Botswana", 5: "Burkina Faso", 6: "Cabo Verde", 7: "Cameroon",
    8: "Congo-Brazzaville", 9: "Côte d'Ivoire", 10: "Eswatini", 11: "Ethiopia", 12: "Gabon",
    13: "Gambia", 14: "Ghana", 15: "Guinea", 16: "Kenya", 17: "Lesotho", 18: "Liberia",
    19: "Madagascar", 20: "Malawi", 21: "Mali", 22: "Mauritania", 23: "Mauritius",
    24: "Morocco", 25: "Mozambique", 26: "Namibia", 27: "Niger", 28: "Nigeria",
    29: "São Tomé and Príncipe", 30: "Senegal", 31: "Seychelles", 32: "Sierra Leone",
    33: "South Africa", 34: "Sudan", 35: "Tanzania", 36: "Togo", 37: "Tunisia",
    38: "Uganda", 39: "Zambia", 40: "Zimbabwe"
}

filtered_df['COUNTRY'] = filtered_df['COUNTRY'].map(country_mapping)

# Dictionary for value labels (adjust based on the dataset documentation)
q45_value_labels = {
    0: "Nothing/no problems",
    1: "Management of the economy",
    2: "Wages, incomes, and salaries",
    3: "Unemployment",
    4: "Poverty/Destitution",
    5: "Rates and taxes",
    6: "Loans/Credit",
    7: "Farming/Agriculture",
    8: "Food shortage/Famine",
    9: "Drought",
    10: "Land",
    11: "Transportation",
    12: "Communications",
    13: "Infrastructure/Roads",
    14: "Education",
    15: "Housing",
    16: "Electricity",
    17: "Water supply",
    18: "Orphans/Homeless children",
    19: "Services (other)",
    20: "Health",
    21: "AIDS",
    22: "Sickness/Disease",
    23: "Crime and security",
    24: "Corruption",
    25: "Political violence",
    26: "Political instability/Divisions",
    27: "Discrimination/Inequality",
    28: "Gender issues/Women's rights",
    29: "Democracy/Political rights",
    30: "War (international)",
    31: "Civil war",
    32: "Agricultural marketing",
    33: "Climate change",
    34: "COVID-19",
    180: "Internally displaced",
    1500: "Pollution",
    1680: "Drug abuse",
    9995: "Other",
    9998: "Refused",
    9999: "Don't know",
    -1: "Missing"
}

custom_palette = {
    "Nothing/no problems": "#1f77b4",
    "Management of the economy": "#ff7f0e",
    "Wages, incomes, and salaries": "#2ca02c",
    "Unemployment": "#d62728",
    "Poverty/Destitution": "#9467bd",
    "Rates and taxes": "#8c564b",
    "Loans/Credit": "#e377c2",
    "Farming/Agriculture": "#7f7f7f",
    "Food shortage/Famine": "#bcbd22",
    "Drought": "#17becf",
    "Land": "#1f77b4",
    "Transportation": "#ff7f0e",
    "Communications": "#2ca02c",
    "Infrastructure/Roads": "#d62728",
    "Education": "#9467bd",
    "Housing": "#8c564b",
    "Electricity": "#e377c2",
    "Water supply": "#1E90FF",  # Blue color assigned
    "Orphans/Homeless children": "#bcbd22",
    "Services (other)": "#17becf",
    "Health": "#1f77b4",
    "AIDS": "#ff7f0e",
    "Sickness/Disease": "#2ca02c",
    "Crime and security": "#d62728",
    "Corruption": "#9467bd",
    "Political violence": "#8c564b",
    "Political instability/Divisions": "#e377c2",
    "Discrimination/Inequality": "#7f7f7f",
    "Gender issues/Women's rights": "#bcbd22",
    "Democracy/Political rights": "#17becf",
    "War (international)": "#1f77b4",
    "Civil war": "#ff7f0e",
    "Agricultural marketing": "#2ca02c",
    "Climate change": "#d62728",
    "COVID-19": "#9467bd",
    "Internally displaced": "#8c564b",
    "Pollution": "#e377c2",
    "Drug abuse": "#7f7f7f",
    "Other": "#bcbd22",
    "Refused": "#17becf",
    "Don't know": "#1f77b4",
    "Missing": "#ff7f0e"
}


# Apply value labels to recode the variables of interest
for var in ['Q45PT1', 'Q45PT2', 'Q45PT3']:
    if var in filtered_df.columns:
        filtered_df[var] = filtered_df[var].map(q45_value_labels)

# Folder to save plots
results_folder = r"C:\Users\massa\Desktop\MiniProjet\Afro barometre\Results"
os.makedirs(results_folder, exist_ok=True)

# Titles for each variable
titles = {
    'Q45PT1': "First Most Important Problem",
    'Q45PT2': "Second Most Important Problem",
    'Q45PT3': "Third Most Important Problem"
}

for var in ['Q45PT1', 'Q45PT2', 'Q45PT3']:
    # Count the frequency of each response
    freq = filtered_df[var].value_counts().sort_values(ascending=False)

    # Calculate percentages
    percentages = (freq / nb_indivi) * 100

    # Map the modalities to their specific colors
    modality_colors = [custom_palette[label] for label in freq.index]

    # Create a bar plot
    plt.figure(figsize=(14, 8))
    sns.barplot(
        x=freq.index,
        y=percentages.values,
        palette=modality_colors
    )
    plt.title(f"{titles.get(var, var)} ", fontsize=18, fontweight='bold')
    plt.xlabel("", fontsize=14)
    plt.ylabel(" (%)", fontsize=14)
    plt.xticks(rotation=45, ha="right", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Save the graph
    graph_file_name = f"{var}_percentage_distribution.png"
    graph_file_path = os.path.join(results_folder, graph_file_name)
    plt.tight_layout()
    plt.savefig(graph_file_path)
    plt.close()

    print(f"Graph saved for {var} at: {graph_file_path}")


# Generate plots for each country
countries = filtered_df['COUNTRY'].unique()

for country in countries:
    country_data = filtered_df[filtered_df['COUNTRY'] == country]
    nb_indivi_country = len(country_data)

    for var in ['Q45PT1', 'Q45PT2', 'Q45PT3']:
        freq = country_data[var].value_counts().sort_values(ascending=False)
        percentages = (freq / nb_indivi_country) * 100
        modality_colors = [custom_palette.get(label, "#333333") for label in freq.index]

        plt.figure(figsize=(14, 8))
        sns.barplot(
            x=freq.index,
            y=percentages.values,
            palette=modality_colors
        )
        plt.title(f"{titles.get(var, var)} in {country} ", fontsize=18, fontweight='bold')
        plt.xlabel("", fontsize=14)
        plt.ylabel("Percentage (%)", fontsize=14)
        plt.xticks(rotation=45, ha="right", fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Save the graph
        country_results_folder = os.path.join(results_folder, country)
        os.makedirs(country_results_folder, exist_ok=True)
        graph_file_name = f"{var}_percentage_distribution_{country}.png"
        graph_file_path = os.path.join(country_results_folder, graph_file_name)
        plt.tight_layout()
        plt.savefig(graph_file_path)
        plt.close()

        print(f"Graph saved for {var} in {country} at: {graph_file_path}")


# Generate plots per country in resukts
countries = filtered_df['COUNTRY'].dropna().unique()

for country in countries:
    country_data = filtered_df[filtered_df['COUNTRY'] == country]
    nb_indivi_country = len(country_data)

    for var in ['Q45PT1', 'Q45PT2', 'Q45PT3']:
        freq = country_data[var].value_counts().sort_values(ascending=False)
        percentages = (freq / nb_indivi_country) * 100
        modality_colors = [custom_palette.get(label, "#333333") for label in freq.index]

        plt.figure(figsize=(14, 8))
        sns.barplot(x=freq.index, y=percentages.values, palette=modality_colors)
        plt.title(f"{titles.get(var, var)} in {country}", fontsize=18, fontweight='bold')
        plt.xlabel("", fontsize=14)
        plt.ylabel("Percentage (%)", fontsize=14)
        plt.xticks(rotation=45, ha="right", fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        graph_file_name = f"{var}_Percentage_{country}.png"
        plt.tight_layout()
        plt.savefig(os.path.join(results_folder, graph_file_name))
        plt.close()

        print(f"Graph saved for {var} in {country} at: {os.path.join(results_folder, graph_file_name)}")