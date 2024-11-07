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
    return jiwer.cer(hypotheses, references)

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