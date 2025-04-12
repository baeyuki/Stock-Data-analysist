import numpy as np
import matplotlib.pyplot as plt

def plot_histogram(data_list, in_sample_data=None, bin_width=1000 , criteria=None,number_of_bins=30):
    """
    Visualize a histogram of total profits, group similar values, and compare with in-sample profit.
    
    Parameters:
    - data_list: List or array of total profits (e.g., 100 values).
    - in_sample_profit: The in-sample total profit to compare (optional).
    - bin_width: Width of each bin for grouping similar profits (default: 0.01).
    """
    criteria = ''
    if number_of_bins is not None:
        number_of_bins = number_of_bins
    if(criteria is None):
        criteria = 'total_profit'
    else:
        criteria = criteria

    # Determine the bins for grouping
    min_val = 0
    max_val = 0
    min_data = min(data_list)
    max_data = max(data_list)
    min_val = min_data - bin_width
    max_val = max_data + bin_width
    bins = np.arange(min_val,max_val, (max_val - min_val) / number_of_bins)  # Create bins from min to max with specified width
    
    # Create the histogram
    plt.figure(figsize=(10, 6))
    counts, bins, _ = plt.hist(data_list, bins=bins, density=True, alpha=0.7, color='gray', edgecolor='black')
    
    # Customize the plot
    plt.xlabel(f'{criteria} (Ω)')
    plt.ylabel('Probability')
    plt.title(f'Histogram of {criteria}')
    
    # If in-sample data is provided, mark it and calculate p-value
    if in_sample_data is not None:
        # Mark the in-sample data on the histogram
        in_sample_data = float(in_sample_data)  # Ensure it's a float for comparison
        plt.axvline(in_sample_data, color='red', linestyle='--', label=f'In-sample TT: {in_sample_data:.3f}')
        
        # Calculate the p-value (sum of probabilities for data > in_sample_data)
        bin_centers = (bins[:-1] + bins[1:]) / 2
        probabilities = counts / sum(counts)
        p_value = sum(probabilities[bin_centers > in_sample_data])
        
        # Add p-value to the plot
        plt.text(in_sample_data + 0.01, max(counts) * 0.9, f'p-value = {p_value:.3f}', color='blue')
        
        # Determine the position (left tail, center, right tail)
        if in_sample_data < bins[len(bins)//3]:
            position = "left tail"
        elif in_sample_data > bins[2*len(bins)//3]:
            position = "right tail"
        else:
            position = "center"
        print(f"In-sample profit {in_sample_data:.3f} lies in the {position} of the distribution.")
        print(f"p-value: {p_value:.3f}")
        if p_value < 0.1:
            print("Since p-value < 0.1, we reject H0. The strategy likely outperformed that monkey.")
        else:
            print("Since p-value >= 0.1, we fail to reject H0. We can't beat that monkey.")
    
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()