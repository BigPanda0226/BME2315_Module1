# AI Usage Statement: AI was used to assist in the development of this code by suggesting improvemnts and corrections to incorrect code. AI also helped find correlations between the data which helped when formatting the bar and scatter plots.

from patient_cherry import Patient # Import the Patient class from the patient_cherry.py file
import matplotlib.pyplot as plt
import numpy as np
import statistics
from scipy import stats
import pandas as pd
from sklearn.linear_model import LinearRegression


filename = "Metadata and Protein Data for Module 1.csv"

Patient.instantiate_from_csv(filename) # Create all patient objects from the CSV file.

Patient.all_patients.sort(key=Patient.get_age_at_death, reverse=False) # Sort and print all patients by age at death, youngest to oldest.

print("PATIENTS SORTED BY AGE AT DEATH")
for patient in Patient.all_patients: # Print all patients sorted by age at death.
    print(patient)

female_dementia_patients = Patient.filter(Patient.all_patients, sex="Female", cognitive_status="Dementia") # Filter using two attributes: sex and cognitive status.

print("\nFEMALE PATIENTS WITH DEMENTIA")
for patient in female_dementia_patients: # Print all female patients with dementia.
    print(patient)

print(f"Number of female patients with dementia: "
      f"{len(female_dementia_patients)}")

male_dementia_patients = Patient.filter(Patient.all_patients, sex="Male", cognitive_status="Dementia") # Filter male patients with dementia for the bar graph comparison.

female_abeta42 = [] # Store ABeta42 values for female and male patients with dementia.
male_abeta42 = []

for patient in female_dementia_patients: # Store ABeta42 values for female and male patients with dementia.
    female_abeta42.append(patient.abeta42)

for patient in male_dementia_patients:
    male_abeta42.append(patient.abeta42)

female_mean = statistics.mean(female_abeta42) # Calculate the means and standard deviations.
male_mean = statistics.mean(male_abeta42)
female_stdev = statistics.stdev(female_abeta42)
male_stdev = statistics.stdev(male_abeta42)

print(f"\nFemale mean ABeta42: {female_mean:.2f} pg/ug")
print(f"Female ABeta42 standard deviation: {female_stdev:.2f} pg/ug")
print(f"Male mean ABeta42: {male_mean:.2f} pg/ug")
print(f"Male ABeta42 standard deviation: {male_stdev:.2f} pg/ug")

sex_labels = ["Female", "Male"] # Bar graph: mean ABeta42 +/- standard deviation by sex among dementia patients.
abeta42_means = [female_mean, male_mean]
abeta42_stdevs = [female_stdev, male_stdev]
yerr = [np.zeros(len(abeta42_means)), abeta42_stdevs]

plt.figure(figsize=(7, 5)) # Create a new figure with the specified size, then plot a bar graph with error bars representing the standard deviation for each sex. The bars are colored purple for females and green for males. The graph is titled and labeled appropriately, and the layout is adjusted to fit everything neatly. Finally, the graph is saved as a PNG file and displayed.
plt.bar(
    sex_labels,
    abeta42_means,
    yerr=yerr,
    capsize=10,
    color=["purple", "green"]
)
plt.title("Mean ABeta42 Levels in Patients with Dementia")
plt.xlabel("Sex")
plt.ylabel("Mean ABeta42 (pg/ug)")
plt.tight_layout()
plt.savefig("Cherry_bar_graph.png", dpi=300)
plt.show()

ages_at_death = [] # Scatter plot: ABeta42 level versus age at death for all patients.
all_abeta42 = []

for patient in Patient.all_patients: # Store the age at death and ABeta42 values for all patients in separate lists to be used for plotting.
    ages_at_death.append(patient.age_at_death)
    all_abeta42.append(patient.abeta42)

t_stat, p_value = stats.ttest_ind(female_abeta42, male_abeta42)
print(f"t-statistic: {t_stat:.2f}")
print(f"p-value: {p_value:.4f}")
if p_value < 0.05:
    print("There is a statistically significant difference between female and male ABeta42 levels.")
else:
    print("There is no statistically significant difference between female and male ABeta42 levels.")

ages_at_death_array = np.array(ages_at_death).reshape(-1, 1)

model = LinearRegression()
model.fit(ages_at_death_array, all_abeta42)

predicted_abeta42 = model.predict(ages_at_death_array)

slope = model.coef_[0]
intercept = model.intercept_
r_squared = model.score(ages_at_death_array, all_abeta42)

print(f"\nRegression slope: {slope:.2f}")
print(f"Regression intercept: {intercept:.2f}")
print(f"R-squared value: {r_squared:.4f}")

plt.figure(figsize=(7, 5))

plt.scatter(
    ages_at_death,
    all_abeta42,
    color="blue",
    alpha=0.7,
    label="Patients"
)

plt.plot(
    ages_at_death,
    predicted_abeta42,
    color="red",
    linewidth=2,
    label="Linear Regression"
)

regression_text = (
    f"y = {slope:.2f}x + {intercept:.2f}\n"
    f"R² = {r_squared:.4f}"
)

plt.text(
    0.05,
    0.95,
    regression_text,
    transform=plt.gca().transAxes,
    fontsize=11,
    verticalalignment="top",
    bbox=dict(facecolor="white", edgecolor="black", alpha=0.8)
)

plt.title("ABeta42 Level vs. Age at Death")
plt.xlabel("Age at Death (years)")
plt.ylabel("ABeta42 (pg/ug)")
plt.legend()
plt.tight_layout()
plt.savefig("Cherry_scatter_plot.png", dpi=300)
plt.show()