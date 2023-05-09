import numpy as np
import math
import pandas as pd
from scipy.stats import chi2

# Read the Excel file
df = pd.read_excel('file.xlsx')

# Get the values from the desired column of the Excel file
data = df['data'].values.tolist()


def benflaw(data):
    # Get the first digit of each number in the dataset
    first_digits = [int(str(abs(num))[0]) for num in data if num != 0]

    # Calculate the observed frequency of each digit
    digit_count = pd.Series(list(data)).value_counts(sort=False)
    observed_freq = np.array(digit_count.values)

    # Calculate the expected frequency of each digit based on Benford's Law
    expected_counts = [round(len(first_digits) * math.log10(1 + 1 / d)) for d in range(1, 10)]

    # Define the expected frequencies for each digit based on Benford's law
    expected_freq = np.array([np.log10(1 + 1 / d) for d in range(1, 10)])
    expected_freq = expected_freq * len(data)

    # Compute the chi-squared test statistic and p-value
    chi_squared_stat = np.sum((observed_freq - expected_freq) ** 2 / expected_freq)
    degrees_of_freedom = len(observed_freq) - 1
    p_value = 1 - chi2.cdf(chi_squared_stat, degrees_of_freedom)

    alpha = 0.05
    if p_value < alpha:
        return 'fake'
    else:
        return 'real'


print(benflaw(data))