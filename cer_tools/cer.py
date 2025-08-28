from typing import List
import jiwer
import pandas as pd

def cer(hypotheses: List[str], references: List[str]) -> float:
    """
    Compute Character Error Rate (CER) between hypotheses and references
    Args:
        hypotheses: list of strings
        references: list of strings
    Returns:
        cer: float
    """
    # Filter out pairs where reference is empty string
    filtered_hypotheses = []
    filtered_references = []
    
    for hyp, ref in zip(hypotheses, references):
        if ref.strip():  # Only include if reference is not empty or just whitespace
            filtered_hypotheses.append(hyp)
            filtered_references.append(ref)
    
    # If no valid pairs remain, return 1.0 (100% error rate)
    if not filtered_references:
        return 1.0
    
    # If all references are empty but we have hypotheses, calculate based on hypothesis length
    if len(filtered_references) == 0 and any(hyp.strip() for hyp in hypotheses):
        return 1.0
    
    return jiwer.cer(filtered_hypotheses, filtered_references)

def read_file(file_path: str) -> pd.DataFrame:
    """
    Read CSV or XLSX file and return the dataframe

    Args:
        file_path (str): path to the file
    Returns:
        dataframe (pandas.DataFrame): dataframe containing the data
    """
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Only CSV and XLSX files are supported")
    
def get_column_to_list(dataframe: pd.DataFrame, column_name: str) -> List[str]:
    """
    Get the values of a column from a dataframe and return as a list

    Args:
        dataframe (pandas.DataFrame): dataframe containing the data
        column_name (str): column name
    Returns:
        values (list): list of values in the column
    """
    return dataframe[column_name].values.tolist()

def process_text(text: any) -> str:
    """
    Process the text by converting to lowercase and removing leading and trailing whitespaces
    Args:
        text: any
    Returns:
        processed_text: string
    """
    # Convert to string
    text = str(text)
    return text.lower().strip()

def get_matched_columns(hypotheses_dataframe: pd.DataFrame, references_dataframe: pd.DataFrame) -> List[str]:
    """
    Get the matched columns' names from the two dataframes excluding the index column (the first column)
    Args:
        hypotheses_dataframe: pandas.DataFrame
        references_dataframe: pandas.DataFrame
    Returns:
        matched_columns: list of strings
    """
    hypotheses_columns = hypotheses_dataframe.columns[1:]
    references_columns = references_dataframe.columns[1:]
    return list(set(hypotheses_columns).intersection(references_columns))

def concatenate_columns(dataframe: pd.DataFrame, columns: List[str]) -> List[str]:
    """
    Concatenate the values of the columns in the dataframe and return as a list of string.
    Args:
        dataframe: pandas.DataFrame
        columns: list of strings
    Returns:
        concatenated_values: list of strings
    """
    list_of_str_in_columns = []
    for column in columns:
        list_of_str_in_column = get_column_to_list(dataframe, column)
        list_of_str_in_columns += list_of_str_in_column
    return list_of_str_in_columns



    