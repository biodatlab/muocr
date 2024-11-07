####################################################################################################
# Description: This script calculates the Character Error Rate (CER) of the predicted text against
# the ground truth text. The script reads the predictions and groundtruth from separate CSV or XLSX files.
# The columns containing the predictions and groundtruth are specified in the arguments.
# The script uses the function in `cer` module  to calculate the CER.
# Usage: python cer_calculation.py --predictions predictions.csv --groundtruth groundtruth.csv --prediction_column pred --groundtruth_column gt
####################################################################################################

import argparse
from typing import List
import cer

def main(predictions_file: str, groundtruth_file: str, prediction_column: str, groundtruth_column: str) -> float:
    """
    Calculate the Character Error Rate (CER) between predictions and groundtruth
    Args:
        predictions_file: path to the predictions file
        groundtruth_file: path to the groundtruth file
        prediction_column: column name in the predictions file
        groundtruth_column: column name in the groundtruth file
    Returns:
        cer: float
    """
    predictions_df = cer.read_file(predictions_file)
    groundtruth_df = cer.read_file(groundtruth_file)
    predictions = cer.get_column_to_list(predictions_df, prediction_column)
    groundtruth = cer.get_column_to_list(groundtruth_df, groundtruth_column)
    # Process each element in predictions and groundtruth
    predictions = [cer.process_text(pred) for pred in predictions]
    groundtruth = [cer.process_text(gt) for gt in groundtruth]
    # Check if the number of predictions and groundtruth are the same
    assert len(predictions) == len(groundtruth), "Number of predictions and groundtruth should be the same"
    # Check if any of elements in predictions and groundtruth are float
    if any([isinstance(pred, float) for pred in predictions]):
        raise ValueError("Some predictions are float")
    if any([isinstance(gt, float) for gt in groundtruth]):
        raise ValueError("Some groundtruth are float")
    # Check if any of elements in predictions and groundtruth are empty
    if any([not pred.strip() for pred in predictions]):
        raise ValueError("Some predictions are empty")
    if any([not gt.strip() for gt in groundtruth]):
        raise ValueError("Some groundtruth are empty")
    return cer.cer(predictions, groundtruth)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate Character Error Rate (CER) between predictions and groundtruth')
    parser.add_argument('--predictions', type=str, help='Path to the predictions file')
    parser.add_argument('--groundtruth', type=str, help='Path to the groundtruth file')
    parser.add_argument('--prediction_column', type=str, help='Column name in the predictions file')
    parser.add_argument('--groundtruth_column', type=str, help='Column name in the groundtruth file')
    args = parser.parse_args()
    
    cer = main(args.predictions, args.groundtruth, args.prediction_column, args.groundtruth_column)
    print(f'CER: {cer}')