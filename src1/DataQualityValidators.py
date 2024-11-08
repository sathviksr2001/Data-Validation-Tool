from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
from datetime import datetime
import os
import time

class DataQualityValidator:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.validation_results = {}

    def check_missing_values(self, threshold: float = 0.1) -> Dict[str, float]:
        """
        Check for columns with missing values above specified threshold

        Args:
            threshold: Maximum acceptable percentage of missing values (0-1)
        Returns:
            Dictionary of columns and their missing value percentages
        """
        missing_pct = (self.df.isnull().sum() / len(self.df))
        problematic_cols = missing_pct[missing_pct > threshold]

        self.validation_results['missing_values'] = {
            'status': len(problematic_cols) == 0,
            'details': problematic_cols.to_dict()
        }
        return problematic_cols.to_dict()

    def check_duplicates(self, subset: Optional[List[str]] = None) -> int:
        """
        Check for duplicate rows in the dataset

        Args:
            subset: List of columns to check for duplicates
        Returns:
            Number of duplicate rows found
        """
        duplicate_count = len(self.df[self.df.duplicated(subset=subset)])

        self.validation_results['duplicates'] = {
            'status': duplicate_count == 0,
            'details': {'duplicate_count': duplicate_count}
        }
        return duplicate_count

    def check_outliers(self, columns: List[str], n_std: float = 3) -> Dict[str, List]:
        """
        Detect outliers using standard deviation method

        Args:
            columns: Numerical columns to check for outliers
            n_std: Number of standard deviations to use as threshold
        Returns:
            Dictionary with outlier indices for each column
        """
        outliers = {}

        for col in columns:
            if pd.api.types.is_numeric_dtype(self.df[col]):
                mean = self.df[col].mean()
                std = self.df[col].std()
                outlier_idx = self.df[
                    (self.df[col] < mean - n_std * std) |
                    (self.df[col] > mean + n_std * std)
                ].index.tolist()
                outliers[col] = outlier_idx

        self.validation_results['outliers'] = {
            'status': all(len(idx) == 0 for idx in outliers.values()),
            'details': outliers
        }
        return outliers

    def validate_schema(self, expected_schema: Dict[str, str]) -> List[str]:
        """
        Validate that DataFrame columns match expected data types

        Args:
            expected_schema: Dictionary of column names and expected data types
        Returns:
            List of columns with mismatched data types
        """
        mismatched_cols = []

        for col, expected_type in expected_schema.items():
            if col in self.df.columns:
                actual_type = str(self.df[col].dtype)
                if actual_type != expected_type:
                    mismatched_cols.append(col)
            else:
                mismatched_cols.append(col)

        self.validation_results['schema'] = {
            'status': len(mismatched_cols) == 0,
            'details': {'mismatched_columns': mismatched_cols}
        }
        return mismatched_cols

    def get_validation_summary(self) -> Dict[str, Any]:
        """Return complete validation results"""
        return {
            'timestamp': datetime.now().isoformat(),
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'checks': self.validation_results,
            'overall_status': all(check['status'] for check in self.validation_results.values())
        }

class DataQualityUI:
    def __init__(self):
        self.validator = None
        self.df = None

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        print("\n" + "="*50)
        print("       Data Quality Validation Tool")
        print("="*50 + "\n")

    def load_data(self):
        while True:
            self.clear_screen()
            self.print_header()
            print("Load Data Options:")
            print("1. Load CSV file")
            print("2. Load Excel file")
            print("3. Exit")

            choice = input("\nEnter your choice (1-3): ")

            if choice == '1':
                file_path = input("\nEnter CSV file path: ")
                try:
                    self.df = pd.read_csv(file_path)
                    print("\nData loaded successfully!")
                    self.validator = DataQualityValidator(self.df)
                    time.sleep(2)
                    return True
                except Exception as e:
                    print(f"\nError loading file: {str(e)}")
                    input("\nPress Enter to continue...")

            elif choice == '2':
                file_path = input("\nEnter Excel file path: ")
                try:
                    self.df = pd.read_excel(file_path)
                    print("\nData loaded successfully!")
                    self.validator = DataQualityValidator(self.df)
                    time.sleep(2)
                    return True
                except Exception as e:
                    print(f"\nError loading file: {str(e)}")
                    input("\nPress Enter to continue...")

            elif choice == '3':
                return False

    def display_data_preview(self):
        self.clear_screen()
        self.print_header()
        print("Data Preview:")
        print("\nFirst 5 rows:")
        print(self.df.head())
        print("\nDataset Info:")
        print(f"Total Rows: {len(self.df)}")
        print(f"Total Columns: {len(self.df.columns)}")
        print("\nColumns:", ", ".join(self.df.columns))
        input("\nPress Enter to continue...")

    def run_validations(self):
        while True:
            self.clear_screen()
            self.print_header()
            print("Validation Options:")
            print("1. Check Missing Values")
            print("2. Check Duplicates")
            print("3. Check Outliers")
            print("4. Validate Schema")
            print("5. Run All Checks")
            print("6. View Validation Summary")
            print("7. Return to Main Menu")

            choice = input("\nEnter your choice (1-7): ")

            if choice == '1':
                threshold = float(input("\nEnter missing values threshold (0-1): "))
                results = self.validator.check_missing_values(threshold)
                print("\nMissing Values Check Results:")
                print(results)
                input("\nPress Enter to continue...")

            elif choice == '2':
                columns = input("\nEnter column names to check for duplicates (comma-separated) or press Enter for all: ")
                subset = [col.strip() for col in columns.split(',')] if columns else None
                results = self.validator.check_duplicates(subset)
                print(f"\nFound {results} duplicate rows")
                input("\nPress Enter to continue...")

            elif choice == '3':
                columns = input("\nEnter numerical column names to check for outliers (comma-separated): ")
                n_std = float(input("Enter number of standard deviations (default=3): ") or 3)
                cols = [col.strip() for col in columns.split(',')]
                results = self.validator.check_outliers(cols, n_std)
                print("\nOutlier Detection Results:")
                print(results)
                input("\nPress Enter to continue...")

            elif choice == '4':
                print("\nCurrent column types:")
                for col in self.df.columns:
                    print(f"{col}: {self.df[col].dtype}")
                print("\nEnter expected schema (example: column_name:dtype, ...)")
                schema_input = input("Schema: ")
                schema = {}
                for item in schema_input.split(','):
                    if ':' in item:
                        col, dtype = item.split(':')
                        schema[col.strip()] = dtype.strip()
                results = self.validator.validate_schema(schema)
                print("\nSchema Validation Results:")
                print(results)
                input("\nPress Enter to continue...")

            elif choice == '5':
                print("\nRunning all checks...")
                self.validator.check_missing_values()
                self.validator.check_duplicates()
                self.validator.check_outliers(
                    self.df.select_dtypes(include=[np.number]).columns.tolist()
                )
                print("\nAll checks completed!")
                input("\nPress Enter to continue...")

            elif choice == '6':
                summary = self.validator.get_validation_summary()
                print("\nValidation Summary:")
                print(summary)
                input("\nPress Enter to continue...")

            elif choice == '7':
                break

    def main_menu(self):
        while True:
            self.clear_screen()
            self.print_header()
            print("Main Menu:")
            print("1. Load Data")
            print("2. Preview Data")
            print("3. Run Validations")
            print("4. Exit")

            choice = input("\nEnter your choice (1-4): ")

            if choice == '1':
                if not self.load_data():
                    break

            elif choice == '2':
                if self.df is not None:
                    self.display_data_preview()
                else:
                    print("\nPlease load data first!")
                    time.sleep(2)

            elif choice == '3':
                if self.df is not None:
                    self.run_validations()
                else:
                    print("\nPlease load data first!")
                    time.sleep(2)

            elif choice == '4':
                print("\nThank you for using the Data Quality Validation Tool!")
                break

if __name__ == "__main__":
    ui = DataQualityUI()
    ui.main_menu()
