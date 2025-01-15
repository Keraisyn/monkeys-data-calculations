import pandas as pd
import argparse
import pathlib

OBSERVATION_ID_COL_NAME = "Observation id"
BEHAVIOUR_COL_NAME      = "Behavior"
DURATION_COL_NAME       = "Duration (s)"
DEMO_BEHAVIOUR_NAME     = "Demo"
LOOK_BEHAVIOUR_NAME     = "Look"

def calculate_looks_and_demos(filepath: str) -> pd.DataFrame:
    df = pd.read_excel(filepath)
    df = df.groupby(
        [OBSERVATION_ID_COL_NAME, BEHAVIOUR_COL_NAME]
    )[DURATION_COL_NAME].sum().reset_index()
    df = df.pivot(
        index=OBSERVATION_ID_COL_NAME, 
        columns=BEHAVIOUR_COL_NAME, 
        values=DURATION_COL_NAME
    ).fillna(0).reset_index().rename_axis(None, axis=1)
    df["look_to_demo"] = df["Look"] / df["Demo"]
    
    return df


def calculate_looks_and_demos_multiple(filepaths: list[str]) -> pd.DataFrame:
    file_results = []
    for filepath in filepaths:
        file_results.append(calculate_looks_and_demos(filepath))

    result_df = pd.concat(file_results)

    return result_df


def report_looks_and_demos_multiple(filepaths: list[str]) -> None:
    result_df = calculate_looks_and_demos_multiple(filepaths)
    demo_sum = result_df[DEMO_BEHAVIOUR_NAME].sum()
    look_sum = result_df[LOOK_BEHAVIOUR_NAME].sum()

    for i, row in result_df.iterrows():
        demo = row[DEMO_BEHAVIOUR_NAME]
        look = row[LOOK_BEHAVIOUR_NAME]
        print("------------------------------")
        print("Observation ID:\t", row[OBSERVATION_ID_COL_NAME], sep="")
        print("Demo time:\t", f"{demo:.2f}", sep="")
        print("Look time:\t", f"{look:.2f}", sep="")
        print("Ratio:\t\t", f"{look/demo*100:.2f}", "%", sep="")

    
    print("------------------------------")
    print("TOTAL")
    print("Demo time:\t", f"{demo_sum:.2f}", sep="")
    print("Look time:\t", f"{look_sum:.2f}", sep="")
    print("Ratio:\t\t", f"{look_sum/demo_sum*100:.2f}", "%", sep="")
    print("------------------------------")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate times for monkey data.")
    parser.add_argument('files', nargs="*", help="File path(s) to excel sheet (aggregated format).")
    args = parser.parse_args()
        
    report_looks_and_demos_multiple(args.files)
