import csv


class Patient:

    all_patients = [] # List to store all Patient objects.

    # The __init__ method initializes a Patient object with the provided attributes and appends it to the all_patients list.
    def __init__(self, donor_id: str, age_at_death: float, sex: str, apoe_genotype: str, cognitive_status: str, abeta40: float, abeta42: float, ttau: float, ptau: float):
        self.donor_id = donor_id
        self.age_at_death = age_at_death
        self.sex = sex
        self.apoe_genotype = apoe_genotype
        self.cognitive_status = cognitive_status
        self.abeta40 = abeta40
        self.abeta42 = abeta42
        self.ttau = ttau
        self.ptau = ptau

        Patient.all_patients.append(self)

    def __repr__(self): # Returns a string representation of the Patient object, including donor ID, sex, age at death, cognitive status, APOE genotype, and ABeta42 level.
        return (f"{self.donor_id}: ({self.sex} | {self.age_at_death} years | " f"{self.cognitive_status} | APOE {self.apoe_genotype} | " f"ABeta42 = {self.abeta42} pg/ug)")

    def get_age_at_death(self): # Returns the patient's age at death for sorting.
        return self.age_at_death

    @classmethod # Creates one Patient object from each row of the CSV file.
    def instantiate_from_csv(cls, filename: str):
        Patient.all_patients.clear()

        with open(filename, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            for row in reader:
                Patient(donor_id=row["Donor ID"], age_at_death=float(row["Age at Death"]), sex=row["Sex"], apoe_genotype=row["APOE Genotype"], cognitive_status=row["Cognitive Status"], abeta40=float(row["ABeta40 pg/ug"]), abeta42=float(row["ABeta42 pg/ug"]), ttau=float(row["tTAU pg/ug"]), ptau=float(row["pTAU pg/ug"]))

    @classmethod # Filters patients by sex and/or cognitive status.
    def filter(cls, patient_list, sex="any", cognitive_status="any"):
        filtered_patients = []

        for patient in patient_list: # Check if the patient's sex and cognitive status match the specified criteria. If either criterion is set to "any", it will match all patients for that attribute.
            sex_matches = sex == "any" or patient.sex == sex
            status_matches = (cognitive_status == "any" or
                              patient.cognitive_status == cognitive_status)

            if sex_matches and status_matches:
                filtered_patients.append(patient)

        return filtered_patients
