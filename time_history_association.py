import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

REFERENCE_FOLDER = Path('./signal_data/reference')
EXPERIMENTAL_FOLDER = Path('./signal_data/experimental')
OUTPUT_FILE = Path('./result.csv')

def load_refs() -> dict[str, pd.DataFrame]:
    """Load the reference data from the reference folder into a dict of name, data"""
    references = {}
    for ref in REFERENCE_FOLDER.iterdir():
        reference_data = pd.read_csv(ref)
        references[ref.name] = reference_data
    return references

def load_experimental(filename: Path) -> pd.DataFrame:
    """Load the experimental data into a dataframe"""
    return pd.read_csv(filename)

def best_associations(experimental: pd.DataFrame, references: dict[str, pd.DataFrame]) -> dict[str, dict[str, float]]:
    """Returns the best alignments of experimental data to the references"""
    experimental_values = experimental["Intensity"].to_numpy()
    experimental_length = len(experimental_values)
    best_matches = {}
    
    for reference in references:
        best_error = float('inf')
        best_start = 0
        reference_values = references[reference]["Intensity"].to_numpy()

        for start in range(len(reference_values) - experimental_length + 1):
            
            # calculate difference using RSS
            reference_window = reference_values[start : start + experimental_length]
            error = np.sum(np.square(reference_window - experimental_values))

            if(error < best_error):
                best_error = error
                best_start = start

        best_matches[reference] = {
            'best_error': best_error,
            'best_start': best_start
        }
    return best_matches

def plot_best_fit(experimental: pd.DataFrame, references: dict[str, pd.DataFrame], best_matches: dict[str, dict[str, float]]):
    """Optional plotting to help visualize the best alignment between the experiment and the references"""    
    for fit in best_matches:
        reference = references[fit]
        offset = best_matches[fit]['best_start']

        plt.plot(reference['Time'], reference['Intensity'], label='reference')
        plt.plot(experimental['Time'] + offset, experimental['Intensity'], label='experiment')
        plt.title(fit)

        plt.show()

def compute_prob(best_matches: dict[str, dict[str, float]]) -> tuple[str, float, str, float]:
    """Computes the probability of each match"""

    # Inverse best_error so that lower error gives a higher number
    errors = {}
    for match in best_matches:
        errors[match] = 1 / best_matches[match]['best_error']
    
    # Normalize values to a probability
    total = sum(errors.values())
    probs = {}
    for error in errors:
        probs[error] = errors[error] / total
    
    # Sort by highest probability
    sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)
    best_fit, best_prob = sorted_probs[0]
    second_fit, second_prob = sorted_probs[1]
    
    # Return two best probabilities
    return best_fit, best_prob, second_fit, second_prob

def write_to_csv(name: str, best_fit: str, best_prob: float, second_fit: str, second_prob: float):
    """Append one resulting row to the output CSV"""
    df = pd.DataFrame({
        'Signal': [name],
        'Best signal fit': [best_fit],
        'Best probability': [best_prob],
        'Second best fit': [second_fit],
        'Second best probability': [second_prob]
    })

    df.to_csv(OUTPUT_FILE, index=False, mode='a', header=False)

def initialize_csv():
    """Initialize the output CSV with only the header"""
    df = pd.DataFrame(columns=[ 'Signal', 'Best signal fit', 'Best probability', 'Second best fit', 'Second best probability' ]) 

    df.to_csv(OUTPUT_FILE, index=False)

def main():
    """Runs the main loop over all experiments in the folder"""
    references = load_refs()
    initialize_csv()

    for experiment in EXPERIMENTAL_FOLDER.iterdir():         
        experimental_data = load_experimental(experiment)
        
        best_matches = best_associations(experimental_data, references)
        best_fit, best_prob, second_fit, second_prob = compute_prob(best_matches)

        write_to_csv(experiment.name, best_fit, best_prob, second_fit, second_prob)


if __name__ == '__main__':
    main()