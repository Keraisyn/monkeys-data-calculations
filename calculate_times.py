import pandas as pd
import argparse

OBSERVATION_ID_COL_NAME = "Observation id"
BEHAVIOUR_COL_NAME      = "Behavior"
DURATION_COL_NAME       = "Duration (s)"
START_COL_NAME          = "Start (s)"
STOP_COL_NAME           = "Stop (s)"
DEMO_BEHAVIOUR_NAME     = "Demo"
LOOK_BEHAVIOUR_NAME     = "Look"


### DURATIONS CALCULATIONS ###

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


### INDIVIDUAL DEMOS CALCULATIONS ###

def calculate_individual_looks_and_demos(filepath: str) -> pd.DataFrame:
    df = pd.read_excel(filepath)
    demo_intervals = df[df[BEHAVIOUR_COL_NAME] == DEMO_BEHAVIOUR_NAME].reset_index(drop=True)
    look_intervals = df[df[BEHAVIOUR_COL_NAME] == LOOK_BEHAVIOUR_NAME].reset_index(drop=True)
    
    demo_intervals["Demo Number"] = demo_intervals.groupby(OBSERVATION_ID_COL_NAME).cumcount() + 1

    results = []
    for i, demo in demo_intervals.iterrows():
        id = demo[OBSERVATION_ID_COL_NAME]
        index = demo["Demo Number"]
        start = demo[START_COL_NAME]
        stop = demo[STOP_COL_NAME]
        duration = stop - start

        overlapping_looks = look_intervals[
            (look_intervals[OBSERVATION_ID_COL_NAME] == id) &
            (look_intervals[START_COL_NAME] < stop) &
            (look_intervals[STOP_COL_NAME] > start)
        ]

        total_look_time = 0
        for i, look in overlapping_looks.iterrows():
            s = max(start, look[START_COL_NAME])
            e = min(stop, look[STOP_COL_NAME])
            total_look_time += e - s
        percent = total_look_time / duration * 100

        results.append({
            OBSERVATION_ID_COL_NAME: id,
            "Demo Number": index,
            "Look/Demo %": percent,
            "Total Look Time": total_look_time,
            "Total Demo Time": duration,
        })

    return pd.DataFrame(results)


def calculate_individual_looks_and_demos_multiple(filepaths: list[str]) -> pd.DataFrame:
    file_results = []
    for filepath in filepaths:
        file_results.append(calculate_individual_looks_and_demos(filepath))
        print("Finished processing file", filepath)

    result_df = pd.concat(file_results)

    return result_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate times for monkey data.")
    parser.add_argument("files", nargs="*", help="File path(s) to excel sheet (aggregated format).")
    parser.add_argument("--output", default="output.xlsx", help="Output file path (default: output.xlsx)")
    args = parser.parse_args()
        
    df = calculate_individual_looks_and_demos_multiple(args.files)
    df.to_excel(args.output, index=False)
    print("Exported results to", args.output)
