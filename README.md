# Your Project Name

Brief description of your project.

## Formatter printer

These Python scripts read a TXT files containing the output of the [DSA_RC](https://github.com/Justrygh/Course-allocation-with-friends/tree/main) algorithm, generate accumulated data for utility and the Gini coefficient, and provide input for the [Paula](https://github.com/cheerstopaula/Allocation/tree/main) algorithm.

1. Run _create_duplicate_folder.py_

2. Run _formater_txt_csv.py_

3. Run _calculate_utility.py_

## Folder printer

These Python scripts read a CSV file containing utility or gini coefficient values corresponding to different weights (friendship parameter) and generate a line plot to visualize the data.

## Usage

### Prerequisites

- Python installed (version X.X.X)

### Running the Script

1. Open a terminal or command prompt.

2. Navigate to the project directory.

3. Run the following command:

```bash
   python main.py -s ./friendship.csv -c ./ratings.csv -d ./distributions.csv
```