import pandas as pd
import matplotlib.pyplot as plt

# Load CSV files
df_dsa_rc = pd.read_csv('example_gini_figure_3.csv')
df_ys = pd.read_csv('example_gini_figure_3_ys.csv')

for weight in [0, 1, 2, 3, 4, 5]:
    data = [
        ["60", df_dsa_rc.loc[weight, "60"], df_ys.loc[weight, "60"]],
        ["65", df_dsa_rc.loc[weight, "65"], df_ys.loc[weight, "65"]],
        ["70", df_dsa_rc.loc[weight, "70"], df_ys.loc[weight, "70"]],
        ["75", df_dsa_rc.loc[weight, "75"], df_ys.loc[weight, "75"]],
        ["80", df_dsa_rc.loc[weight, "80"], df_ys.loc[weight, "80"]],
        ["85", df_dsa_rc.loc[weight, "85"], df_ys.loc[weight, "85"]],
        ["90", df_dsa_rc.loc[weight, "90"], df_ys.loc[weight, "90"]]
    ]

    # Form DataFrame from data
    df = pd.DataFrame(data, columns=["Course limit", "DSA_RC", "Yankee swap"])
 
    # Plot unstacked multiple columns such as population and year from DataFrame
    df.plot(x="Course limit", y=["DSA_RC", "Yankee swap"], kind="bar", figsize=(10, 10))
 
    # Display plot
    plt.title(f'Comparison of gini coefficient results for friendship weight set to {weight}')
    plt.xlabel('Course limit')
    plt.ylabel('Value')
    plt.legend()
    plt.show()
