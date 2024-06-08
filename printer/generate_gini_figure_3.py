import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV file
file_path = 'example_gini_figure_3.csv'
data = pd.read_csv(file_path)

# Set the 'weight' column as the index
data.set_index('weight', inplace=True)

# Transpose the dataframe to have weights as columns
data = data.transpose()

# Plot the data
data.plot(kind='line', marker='o')

# Adding labels and title
plt.xlabel('Course Limit')
plt.ylabel('Gini')
plt.title('Gini Coefficient Distribution by Weight')
plt.legend(title='Weights')

# Show the plot
plt.show()
