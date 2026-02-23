import pandas as pd
import matplotlib.pyplot as plt
import os

REFERENCE_FOLDER = './signal_data/reference'
EXPERIMENTAL_FOLDER = './signal_data/experimental'
OUTPUT_FILE = './result.csv'

def load_refs():
    references = {}
    with os.scandir(REFERENCE_FOLDER) as refs:
        for ref in refs:
            reference_data = pd.read_csv(os.path.join(REFERENCE_FOLDER, ref.name))
            references[ref.name] = reference_data
    return references

def load_expiremental(filename):
    return pd.read_csv(filename)

def best_associations(experimental, references):
    # find the delta between every point within the expirement
    experimental_length = len(experimental)

    best_fits = {}

    for reference in references:
        reference_length = len(references[reference])
        best_difference = float('inf')
        best_start = 0

        for start in range(reference_length - experimental_length):

            difference = 0
            for index in range(experimental_length):
                difference += abs(references[reference]['Intensity'][start + index] - experimental['Intensity'][index])

            if(difference < best_difference):
                best_difference = difference
                best_start = start

        best_fits[reference] = {
            'best_difference': best_difference,
            'best_start': best_start
        }
    
    return best_fits

def plot_best_fit(experimental, references, best_fits):    
    for fit in best_fits:
        reference = references[fit]
        offset = best_fits[fit]["best_start"]

        plt.plot(reference["Time"], reference["Intensity"], label='reference')
        plt.plot(experimental["Time"] + offset, experimental["Intensity"], label='experiment')

        plt.show()

def compute_prob(best_fits):
    differences = []
    total_difference = 0
    for fit in best_fits:
        total_difference += best_fits[fit]["best_difference"]
        differences.append((fit, best_fits[fit]["best_difference"]))
    
    probs = [ (fit, d / total_difference) for fit, d in differences]

    probs_sorted = sorted(probs, key=lambda x: x[1])

    best_fit, best_prob = probs_sorted[0]
    second_fit, second_prob = probs_sorted[1]

    best_prob = 1 - best_prob
    second_prob = 1 - second_prob
    

    return best_fit, best_prob, second_fit, second_prob

def write_to_csv(name, best_fit, best_prob, second_fit, second_prob):
    df = pd.DataFrame({
        'Signal': [name],
        'Best signal fit': [best_fit],
        'Best probability': [best_prob],
        'Second best fit': [second_fit],
        'Second best probability': [second_prob]
    })

    file_exists = os.path.isfile(OUTPUT_FILE)
    df.to_csv(OUTPUT_FILE, index=False, mode='a', header=not file_exists)

def initialize_csv():
    df = pd.DataFrame(columns=[ 'Signal', 'Best signal fit', 'Best probability', 'Second best fit', 'Second best probability' ]) 

    df.to_csv(OUTPUT_FILE, index=False)

def main():
    references = load_refs()
    initialize_csv()

    with os.scandir(EXPERIMENTAL_FOLDER) as experiments:
        for experiment in experiments:
            full_path = os.path.join(EXPERIMENTAL_FOLDER, experiment.name)
            
            experimental_data = load_expiremental(full_path)
            best_fits = best_associations(experimental_data, references)
            # plot_best_fit(experimental_data, references, best_fits)
            best_fit, best_prob, second_fit, second_prob = compute_prob(best_fits)
            # print(experiment.name, best_fit, best_prob, second_fit, second_prob)
            write_to_csv(experiment.name, best_fit, best_prob, second_fit, second_prob)


if __name__ == "__main__":
    main()