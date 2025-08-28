# CER (Character Error Rate) Tool

A comprehensive evaluation tool for Optical Character Recognition (OCR) systems that calculates Character Error Rate (CER) between predicted and ground truth text data.

## What is Character Error Rate (CER)?

Character Error Rate (CER) is a metric used to evaluate the accuracy of OCR systems by measuring the percentage of characters that are incorrectly recognized. It quantifies the performance of text recognition systems at the character level.

### How CER is Calculated

CER is calculated using the following formula:

```
CER = (S + D + I) / N
```

Where:
- **S** = Number of character substitutions (incorrect characters)
- **D** = Number of character deletions (missing characters)
- **I** = Number of character insertions (extra characters)
- **N** = Total number of characters in the ground truth text

The result is a value between 0 and ∞, where:
- **0** means perfect recognition (no errors)
- **1** means 100% error rate (every character is wrong)
- Values > 1 are possible when there are more insertions than the original text length

### Example

**Ground Truth:** "hello world"
**Prediction:** "helo word"

- Substitutions: 0
- Deletions: 2 ('l' in "hello", 'l' in "world")
- Insertions: 0
- Total characters in ground truth: 11

CER = (0 + 2 + 0) / 11 = 0.182 = 18.2%

## Features

- **GUI Application**: Easy-to-use PyQt6 interface for loading and comparing files
- **Multiple File Formats**: Supports CSV and Excel (.xlsx) files
- **Column-wise Analysis**: Calculate CER for specific columns or all matched columns
- **Data Preprocessing**: Automatic text processing (lowercase conversion, whitespace trimming)
- **Empty String Handling**: Robust handling of empty or missing text entries
- **Batch Processing**: Process multiple text pairs simultaneously
- **Real-time Preview**: View top 5 rows of loaded data

## Installation

### Prerequisites

- Python 3.10 or higher
- Conda (recommended) or pip

### Option 1: Using Conda Environment

1. Clone the repository:
```bash
git clone <repository-url>
cd muocr-cer-tool
```

2. Create and activate the conda environment:
```bash
conda create -n cer-tool python=3.10
conda activate cer-tool
```

3. Install dependencies:
```bash
pip install -r cer_tools/requirements.txt
```

### Option 2: Using Poetry (if available)

```bash
cd cer_tools
poetry install
poetry shell
```

## Usage

### GUI Application

1. Activate your environment:
```bash
conda activate cer-tool  # or your preferred environment
```

2. Run the application:
```bash
python cer_tools/main_ui_app.py
```

3. Use the interface to:
   - Load prediction and ground truth files (CSV/Excel)
   - Preview your data
   - Select columns for CER calculation
   - Calculate and view CER results

### Programmatic Usage

```python
from cer_tools import cer

# Example: Calculate CER for text pairs
predictions = ["hello world", "good morning"]
groundtruth = ["hello word", "good morning"]

cer_score = cer.cer(predictions, groundtruth)
print(f"CER: {cer_score:.4f} ({cer_score*100:.2f}%)")
```

### File Format

Your CSV/Excel files should have columns containing the text data. Example:

```csv
id,predictions,groundtruth
1,"hello world","hello word"
2,"good morning","good morning"
3,"test text","test txet"
```

## Advanced Features

### Text Preprocessing

The tool automatically applies the following preprocessing:
- Converts text to lowercase
- Strips leading/trailing whitespace
- Handles empty strings gracefully

### Empty String Handling

The tool handles empty ground truth entries by:
- Filtering out pairs where ground truth is empty
- Returning 100% error rate if all ground truth entries are empty
- Continuing calculation with valid pairs only

### Column Matching

The application automatically identifies matching columns between prediction and ground truth files (excluding the first column, typically an ID column).

## Project Structure

```
cer_tools/
├── __init__.py
├── cer.py                 # Core CER calculation functions
├── main_ui_app.py        # PyQt6 GUI application
├── requirements.txt      # Python dependencies
├── pyproject.toml       # Poetry configuration
├── tests/
│   ├── __init__.py
│   ├── test_cer.py      # Unit tests
│   └── test_data.csv    # Test data
└── __pycache__/
```

## API Reference

### Core Functions

- `cer(hypotheses, references)`: Calculate CER between prediction and ground truth lists
- `process_text(text)`: Preprocess text (lowercase, strip whitespace)
- `get_matched_columns(df1, df2)`: Find matching columns between dataframes
- `concatenate_columns(df, columns)`: Combine multiple columns into a single list

## Testing

Run the test suite:

```bash
python -m unittest cer_tools.tests.test_cer -v
```

## Dependencies

- **jiwer**: For CER calculation implementation
- **pandas**: Data manipulation and file I/O
- **PyQt6**: GUI framework
- **numpy**: Numerical operations
- **openpyxl**: Excel file support

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

[Include your license information here]

## Troubleshooting

### Common Issues

1. **"one or more references are empty strings"**: This has been fixed in the current version. Update to the latest version.

2. **PyQt6 installation issues**: Try installing PyQt6 separately:
   ```bash
   pip install PyQt6
   ```

3. **File encoding issues**: Ensure your CSV files are UTF-8 encoded.

## Citation

If you use this tool in your research, please cite:

```
[Add citation information if applicable]
```
