# Time-History-Association
## Overview
This project analyzes experimental signal data and produces a result of which 2 reference signals it is the closest match to.  This uses a comparison with RSS for the error to evaluate the alignment.  This error is then computed into a normalized probability to find the top 2 matches.  The results are then output into a CSV file.

## Thought Process
Each reference had 100 data points, while the experiments had 50.  This means that to check alignment for the data we would need to use a sliding window to check every possible position.  I used RSS for the error metric, as it sharply penalizes large deviations from the data, and I have had experience with it previously in neural network problems.  To compute the probability, I used a calculation that inversed the error so that the lower errors would be higher numbers, then normalized the data to 1.  This gives me a clean probability for each sample.  I also used matplotlib to graph the best fits, and the results looked good to the eye.

## Findings
The best match reference aligned well with the shifted experimental signal when plotted.  The shifting windows worked to find the best match across the time sample.  Many of the experiments were very close to one of the reference signals, and the early probabilities reflected that.

## Recommendations
If I was to continue to work on this project, I would use command line flags for the data input/ouput instead of using global constants.  I would also add in unit testing to ensure that the methods will work as intended and that any change in the future would not break functionality.  I would also add in error handling for experiments that are larger than the references, as well as error handling for the file folders to ensure that the data is what is expected.
