import requests
import pandas as pd
import matplotlib.pyplot as plt

# Fetch data from Eurostat API
url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10_lp_ulc"
params = {
    "format": "JSON",
    "na_item": "D1_SAL_HW",  # Compensation per hour worked
    "unit": "EUR",
    "time": "2022"
}

print("Fetching data from Eurostat...")
response = requests.get(url, params=params)
data = response.json()

# Parse JSON-stat format
records = []
if "dimension" in data and "value" in data:
    geo = data["dimension"]["geo"]["category"]
    countries = geo["label"]
    indices = geo["index"]
    values = data["value"]

    for country_code, idx in indices.items():
        if str(idx) in values and values[str(idx)] is not None:
            country_name = countries.get(country_code, country_code)
            hourly_wage = float(values[str(idx)])
            annual_salary = hourly_wage * 1800  # Convert to annual (1800 hours/year)
            records.append([country_name, annual_salary])

# Create DataFrame and process
df = pd.DataFrame(records, columns=["Country", "Salary_EUR"])
df = df.sort_values("Salary_EUR", ascending=False).head(15)

# Display results
print(f"\nTop 15 European Countries by Average Annual Salary (2022)")
print(f"Min salary: €{df['Salary_EUR'].mean():,.0f}")
print(f"\nTop 5 countries:")
for i, row in df.head(5).iterrows():
    print(f"  {row['Country']}: €{row['Salary_EUR']:,.0f}")

# Create visualization
plt.figure(figsize=(10, 6))
plt.barh(df['Country'], df['Salary_EUR'], color='steelblue')
plt.xlabel('Average Annual Salary (EUR)')
plt.title('European Salaries 2022 - Top 15 Countries')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('eu_salaries.png')
plt.show()

print(f"\n✓ Chart saved as 'eu_salaries.png'")
print(f"✓ Total countries analyzed: {len(df)}")