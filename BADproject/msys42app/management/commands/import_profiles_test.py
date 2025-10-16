import re
import pandas as pd
from datetime import datetime
from django.core.management.base import BaseCommand
from msys42app.models import Child, ContactNumber

class Command(BaseCommand):
    help = "Import child profiles from Excel file (Child Name ignored — uses placeholder names)"

    def add_arguments(self, parser):
        parser.add_argument("excel_file", type=str, help="Path to Excel file")

    def handle(self, *args, **kwargs):
        excel_file = kwargs["excel_file"]

        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading file: {e}"))
            return

        # Locate required columns (case-insensitive, tolerant of spaces and parentheses)
        def find_col(df_cols, *needles):
            needles_l = [n.lower() for n in needles]
            for c in df_cols:
                cl = str(c).strip().lower()
                if any(n in cl for n in needles_l):
                    return c
            return None

        id_col = find_col(df.columns, "child id", "id")
        gender_col = find_col(df.columns, "gender (m/f)", "gender", "sex")
        dob_col = find_col(df.columns, "dob", "date of birth", "birth", "date")

        if not all([id_col, gender_col, dob_col]):
            self.stdout.write(self.style.ERROR("Missing one or more required columns (Child ID, Gender (M/F), DoB)."))
            return

        count_created = 0

        # Pre-parse DoB column with pandas for robust date handling
        parsed_dates = pd.to_datetime(df[dob_col], errors='coerce', infer_datetime_format=True)

        for idx, row in df.iterrows():
            try:
                # Handle Child ID -> normalize to allowed SPC pattern ([A-Z]{3,4}\d{4})
                raw_id = str(row[id_col]).strip() if pd.notna(row[id_col]) else ""
                if not raw_id:
                    self.stdout.write(self.style.WARNING("Skipping row with empty Child ID"))
                    continue

                def to_spc(code_raw: str) -> str:
                    code_raw = (code_raw or "").strip().upper()
                    if re.fullmatch(r"[A-Z]{3,4}\d{4}", code_raw):
                        return code_raw
                    # If purely numeric -> ZZZ + zero-padded last 4 digits
                    if code_raw.isdigit():
                        return f"ZZZ{int(code_raw) % 10000:04d}"
                    # Mixed content: extract letters and digits
                    letters = "".join(ch for ch in code_raw if ch.isalpha())[:4] or "ZZZ"
                    digits = "".join(ch for ch in code_raw if ch.isdigit())[-4:]
                    if not digits:
                        digits = "0000"
                    if len(letters) < 3:
                        letters = (letters + "ZZZ")[:3]
                    # Ensure 3 or 4 letters max
                    letters = letters[:4]
                    return f"{letters}{int(digits):04d}"

                spc_code = to_spc(raw_id)

                # Handle Gender
                gender_raw = str(row[gender_col]).strip().upper() if pd.notna(row[gender_col]) else ""
                if gender_raw.startswith("M"):
                    sex = "Male"
                elif gender_raw.startswith("F"):
                    sex = "Female"
                else:
                    sex = "Male"  # default

                # Handle Date of Birth
                ts = parsed_dates.iloc[idx]
                if pd.isna(ts):
                    dob = datetime(2025, 1, 1).date()
                else:
                    dob = ts.date()

                # Create the Child entry with placeholders for names
                child, created = Child.objects.get_or_create(
                    spc_code=spc_code,
                    defaults=dict(
                        first_name="NA",
                        middle_name="",
                        last_name="NA",
                        sex=sex,
                        dob=dob,
                        blood_grp=None,
                        comm_address="NA",
                        fam_philhealth=None,
                        fam_4ps=None,
                        guardian_lastname="NA",
                        guardian_firstname="NA",
                        guardian_middlename="",
                        guardian_relationship="NA",
                        guardian_sex="Female",
                        age=(datetime.now().year - dob.year),
                    )
                )

                # If already exists, update sex/dob if different
                if not created:
                    updates = {}
                    if child.sex != sex:
                        updates["sex"] = sex
                    if child.dob != dob:
                        updates["dob"] = dob
                        updates["age"] = datetime.now().year - dob.year
                    if updates:
                        Child.objects.filter(pk=child.pk).update(**updates)
                        for k, v in updates.items():
                            if k != "age":
                                setattr(child, k, v)

                # Add default contact if new
                if created:
                    ContactNumber.objects.create(child=child, number="09123456789")
                    count_created += 1
                    self.stdout.write(self.style.SUCCESS(f"Created: {child.spc_code} ({child.sex}, {child.dob})"))
                else:
                    self.stdout.write(self.style.WARNING(f"Updated/kept: {child.spc_code} ({child.sex}, {child.dob})"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing row: {e}"))

        self.stdout.write(self.style.SUCCESS(f"\nImport complete! {count_created} new Child profiles created."))
