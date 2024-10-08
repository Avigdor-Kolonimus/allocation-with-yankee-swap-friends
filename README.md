# FriendAllocate: Optimizing Course Allocation with Collaborative DSSA and Yankee Swap

This project implements a powerful combination of two algorithms: **Distributed Stochastic Search Algorithm** (DSSA) and **Yankee Swap**. _DSSA_ is a metaheuristic optimization technique known for its effectiveness in solving complex optimization problems, while _Yankee Swap_ is a popular algorithm used in gift exchange events. By integrating these two algorithms, this project offers a unique approach to problem-solving, leveraging the stochastic nature of _DSSA_ and the dynamic exchange mechanism of _Yankee Swap_. Additionally, friendship dynamics are incorporated into the utility calculation, enhancing the algorithm's ability to navigate complex problem spaces by considering social relationships. Whether you're tackling optimization challenges or exploring novel problem-solving strategies, this project provides a flexible and innovative framework for experimentation and implementation.

## Helpers folder

These Python scripts are necessary for converting the output of the _Yankee Swap_ algorithm (interpreted by [Paula](https://github.com/cheerstopaula/Allocation/tree/main)) into a format suitable for calculating utility and the Gini coefficient

1. Run _transposed_folder.py_

2. Run _transposed_folder_accumulate.py_


## Formatter folder

These Python scripts read a TXT files containing the output of the [DSA_RC](https://github.com/Justrygh/Course-allocation-with-friends/tree/main) algorithm, generate accumulated data for utility and the Gini coefficient, and provide input for the [Paula](https://github.com/cheerstopaula/Allocation/tree/main) algorithm.

1. Run _create_duplicate_folder.py_

2. Run _formater_txt_csv.py_

3. Run _calculate_utility.py_

4. Run _calculate_utility_paula_output.py_

## Printer folder

These Python scripts read a CSV file containing utility or gini coefficient values corresponding to different weights (friendship parameter) and generate a line plot to visualize the data.

## Original Input folder

This folder contains the original input files used for the experiments:

- `friendship.csv`: The friendship network CSV file.
- `courses.csv`: The CSV file containing students' preferences.
- `empty_input.zip`: Input folders for EYS-FI with the Empty Allocation experiment.
- `random_input.zip`: Input folders for EYS-FI with Random Allocation.
- `dsa_rc_input.zip`: Input folders for EYS-FI with DSA RC Allocation.

## Usage

### Prerequisites

- Python installed (version 3.11.X)

### Additional Parameters in main.py
- `directory`: Folder where input CSV files are located.
- `output_csv_folder`: Folder where the output CSV will be written.
- `original_capacity`: Course limit.
- `method`: Variation of the EYS-FI algorithm.
- `flag_friendship`: Indicates if there is a friendship header in the file.
- `flag_course`: Indicates if there is a course header in the file.
- `flag_distribution`: Indicates if there is an allocation header in the file (CSV files from the input folder).
- `flag_course_limit`: Indicates if there is a course limit column in the file.

### Running the Script

1. Open a terminal or command prompt.

2. Navigate to the project directory.

3. Run the following command:

```bash
   python main.py -s ./friendship.csv -c ./ratings.csv
```
