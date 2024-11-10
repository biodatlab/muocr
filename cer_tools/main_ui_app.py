###############################################################################
# This file contains the main UI application for the CER tools.
# It uses the PyQt6 library for the GUI and the functions in the `cer` module for CER calculation.
# The application allows the user to upload the predictions and groundtruth files and specify the columns.
# The application also displays the top 5 rows of the predictions and groundtruth files.
# The application allows the user to sort the predictions and groundtruth files by the specified columns.
# The application calculates the CER between the predictions and groundtruth and displays the result when the user clicks the "Calculate CER" button.
###############################################################################

import sys
from typing import List
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem, QLineEdit, QComboBox
from PyQt6.QtCore import Qt
import pandas as pd
import cer

class CERApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CER Calculation App")
        self.setGeometry(100, 100, 800, 600)

        self.init_ui()

    def init_ui(self):
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        # File Selection Layout
        file_layout = QHBoxLayout()
        self.pred_file_label = QLabel("Predictions File:")
        self.pred_file_input = QLineEdit()
        self.pred_file_button = QPushButton("Browse")
        self.pred_file_button.clicked.connect(self.load_predictions)

        self.gt_file_label = QLabel("Groundtruth File:")
        self.gt_file_input = QLineEdit()
        self.gt_file_button = QPushButton("Browse")
        self.gt_file_button.clicked.connect(self.load_groundtruth)

        file_layout.addWidget(self.pred_file_label)
        file_layout.addWidget(self.pred_file_input)
        file_layout.addWidget(self.pred_file_button)
        file_layout.addWidget(self.gt_file_label)
        file_layout.addWidget(self.gt_file_input)
        file_layout.addWidget(self.gt_file_button)
        layout.addLayout(file_layout)

        # Select Sorting Column Inputs
        # User can specify the column to sort the data separately for predictions and groundtruth
        # Use combobox to select the column
        sorting_column_layout = QHBoxLayout()
        self.pred_sorting_column_label = QLabel("Prediction Column:")
        self.pred_sorting_column_dropdown = QComboBox()
        self.pred_sorting_column_dropdown.setEnabled(False)  # Disabled until file is loaded
        self.gt_sorting_column_label = QLabel("Groundtruth Column:")
        self.gt_sorting_column_dropdown = QComboBox()
        self.gt_sorting_column_dropdown.setEnabled(False)  # Disabled until file is loaded

        sorting_column_layout.addWidget(self.pred_sorting_column_label)
        sorting_column_layout.addWidget(self.pred_sorting_column_dropdown)
        sorting_column_layout.addWidget(self.gt_sorting_column_label)
        sorting_column_layout.addWidget(self.gt_sorting_column_dropdown)
        # layout.addLayout(sorting_column_layout)

        # Buttons for Sorting
        sorting_button_layout = QHBoxLayout()
        self.sort_button = QPushButton("Sort by Specified Columns")
        self.sort_button.clicked.connect(self.sort_data)
        sorting_button_layout.addWidget(self.sort_button)
        # layout.addLayout(sorting_button_layout)

        # Table Previews
        self.pred_table = QTableWidget()
        self.gt_table = QTableWidget()
        layout.addWidget(QLabel("Predictions Preview:"))
        layout.addWidget(self.pred_table)
        layout.addWidget(QLabel("Groundtruth Preview:"))
        layout.addWidget(self.gt_table)

        # Select Column Inputs for CER Calculation
        # User can specify the column to calculate CER separately for predictions and groundtruth
        # Use combobox to select the column
        calculation_column_layout = QHBoxLayout()
        self.pred_calculation_column_label = QLabel("Prediction Column for CER calculation:")
        self.pred_calculation_column_dropdown = QComboBox()
        self.pred_calculation_column_dropdown.setEnabled(False)  # Disabled until file is loaded
        self.gt_calculation_column_label = QLabel("Groundtruth Column for CER calculation:")
        self.gt_calculation_column_dropdown = QComboBox()
        self.gt_calculation_column_dropdown.setEnabled(False)  # Disabled until file is loaded

        calculation_column_layout.addWidget(self.pred_calculation_column_label)
        calculation_column_layout.addWidget(self.pred_calculation_column_dropdown)
        calculation_column_layout.addWidget(self.gt_calculation_column_label)
        calculation_column_layout.addWidget(self.gt_calculation_column_dropdown)
        # layout.addLayout(calculation_column_layout)

        # Buttons for Calculation
        button_layout = QHBoxLayout()
        self.calculate_button = QPushButton("Calculate CER")
        self.calculate_button.clicked.connect(self.calculate_cer)
        self.result_label = QLabel("CER Result: N/A")
        button_layout.addWidget(self.calculate_button)
        button_layout.addWidget(self.result_label)
        layout.addLayout(button_layout)

        self.central_widget.setLayout(layout)

    def load_predictions(self):
        # Load CSV or Excel file
        filepath, _ = QFileDialog.getOpenFileName(self, "Open Predictions File", "", "Spreadsheet Files (*.csv *.xlsx)")
        if filepath:
            self.pred_file_input.setText(filepath)
            with open(filepath, "rb") as f:
                if filepath.endswith('.xlsx'):
                    self.pred_data = pd.read_excel(f)
                else:
                    self.pred_data = pd.read_csv(f)
            # Automatically sort the data by the first column
            self.pred_data = self.pred_data.sort_values(by=self.pred_data.columns[0])
            # Load the columns into the comboboxes
            self.pred_sorting_column_dropdown.setEnabled(True)
            self.pred_sorting_column_dropdown.clear()
            self.pred_sorting_column_dropdown.addItems(self.pred_data.columns)
            self.pred_calculation_column_dropdown.setEnabled(True)
            self.pred_calculation_column_dropdown.clear()
            self.pred_calculation_column_dropdown.addItems(self.pred_data.columns)
            self.display_data(self.pred_data, self.pred_table)

    def load_groundtruth(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Open Groundtruth File", "", "Spreadsheet Files (*.csv *.xlsx)")
        if filepath:
            self.gt_file_input.setText(filepath)
            with open(filepath, "rb") as f:
                if filepath.endswith('.xlsx'):
                    self.gt_data = pd.read_excel(f)
                else:
                    self.gt_data = pd.read_csv(f)
            # Automatically sort the data by the first column
            self.gt_data = self.gt_data.sort_values(by=self.gt_data.columns[0])
            # Load the columns into the comboboxes
            self.gt_sorting_column_dropdown.setEnabled(True)
            self.gt_sorting_column_dropdown.clear()
            self.gt_sorting_column_dropdown.addItems(self.gt_data.columns)
            self.gt_calculation_column_dropdown.setEnabled(True)
            self.gt_calculation_column_dropdown.clear()
            self.gt_calculation_column_dropdown.addItems(self.gt_data.columns)
            self.display_data(self.gt_data, self.gt_table)

    def display_data(self, data, table_widget):
        """Display the top 5 rows of a DataFrame in a QTableWidget."""
        table_widget.clear()
        table_widget.setRowCount(5)
        table_widget.setColumnCount(len(data.columns))
        table_widget.setHorizontalHeaderLabels(data.columns)

        for i in range(min(5, len(data))):
            for j, column in enumerate(data.columns):
                table_widget.setItem(i, j, QTableWidgetItem(str(data.iloc[i, j])))

    def sort_data(self):
        """Sort both predictions and groundtruth data by the specified columns."""
        pred_sorting_column = self.pred_sorting_column_dropdown.currentText()
        gt_sorting_column = self.gt_sorting_column_dropdown.currentText()

        if hasattr(self, 'pred_data') and pred_sorting_column in self.pred_data.columns:
            self.pred_data = self.pred_data.sort_values(by=pred_sorting_column)
            self.display_data(self.pred_data, self.pred_table)

        if hasattr(self, 'gt_data') and gt_sorting_column in self.gt_data.columns:
            self.gt_data = self.gt_data.sort_values(by=gt_sorting_column)
            self.display_data(self.gt_data, self.gt_table)

    def calculate_cer(self):
        """Calculate the CER and display the result."""
        # pred_column = self.pred_calculation_column_dropdown.currentText()
        # gt_column = self.gt_calculation_column_dropdown.currentText()

        if not (hasattr(self, 'pred_data') and hasattr(self, 'gt_data')):
            self.result_label.setText("CER Result: Load both files first!")
            return

        matched_columns = cer.get_matched_columns(self.pred_data, self.gt_data)
        # Check if any matched_column neither in pred_data nor in gt_data

        # if pred_column not in self.pred_data.columns or gt_column not in self.gt_data.columns:
        #     self.result_label.setText("CER Result: Invalid column names!")
        #     return

        predictions = cer.concatenate_columns(self.pred_data, matched_columns)
        groundtruth = cer.concatenate_columns(self.gt_data, matched_columns)

        # predictions = cer.get_column_to_list(self.pred_data, pred_column)
        # groundtruth = cer.get_column_to_list(self.gt_data, gt_column)

        # Process each element in predictions and groundtruth
        predictions = [cer.process_text(pred) for pred in predictions]
        groundtruth = [cer.process_text(gt) for gt in groundtruth]

        # Ensure both lists have the same length
        if len(predictions) != len(groundtruth):
            self.result_label.setText("CER Result: Mismatched row counts!")
            return
        
        # Ensure that each element in predictions and groundtruth is a string
        if not all(isinstance(pred, str) for pred in predictions):
            self.result_label.setText("CER Result: All predictions should be strings!")
            return
        if not all(isinstance(gt, str) for gt in groundtruth):
            self.result_label.setText("CER Result: All groundtruth should be strings!")
            return

        # Calculate CER
        cer_result = cer.cer(predictions, groundtruth)
        self.result_label.setText(f"CER Result: {cer_result:.4f}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CERApp()
    window.show()
    sys.exit(app.exec())