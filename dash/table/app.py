# -*- coding: utf-8 -*-
from datetime import datetime

import dash
import dash_table
from dash_table.Format import Format, Group, Padding
from dash.dependencies import Input, Output
import pandas as pd

YEAR = "2021"
MONTH = "02"
WEEKDAYS = ["月", "火", "水", "木", "金", "土", "日"]
ACTIVE_CELL = {"row": 0, "column": 2, "column_id": "Begin"}
day1 = {"Date": f"{YEAR}/{MONTH}/01", "Begin": "09:10", "End": "16:00"}
day2 = {"Date": f"{YEAR}/{MONTH}/02", "Begin": "09:20", "End": "17:00"}
day3 = {"Date": f"{YEAR}/{MONTH}/03", "Begin": "10:30", "End": "18:00"}
day4 = {"Date": f"{YEAR}/{MONTH}/04", "Begin": "09:30", "End": "18:00"}
day5 = {"Date": f"{YEAR}/{MONTH}/05", "Begin": "09:30", "End": "18:00"}
day6 = {"Date": f"{YEAR}/{MONTH}/06", "Begin": "18:30", "End": "18:00"}
day7 = {"Date": f"{YEAR}/{MONTH}/07", "Begin": "09:30", "End": "18:00"}

days = [day1, day2, day3, day4, day5, day6, day7]
df = pd.DataFrame(days)

# parse data as datatime objefct and convert them into string object
df["Begin"] = pd.to_datetime(df["Begin"], format="%H:%M").dt.strftime("%H:%M")
df["End"] = pd.to_datetime(df["End"], format="%H:%M").dt.strftime("%H:%M")
df["Date"] = pd.to_datetime(df["Date"], format="%Y/%m/%d").dt.strftime("%Y/%m/%d")

day_of_the_weeks = pd.to_datetime(df["Date"], format="%Y/%m/%d").map(
    lambda d: WEEKDAYS[datetime.weekday(d)]
)
# insert `day_of_the_weeks` next to "Date"
loc = list(df.columns).index("Date") + 1
df.insert(loc, "DoW", day_of_the_weeks)

data = list(df.to_dict("index").values())

app = dash.Dash(__name__)

columns = []
for col in df.columns:
    if col in ["Date", "DoW"]:
        columns.append(
            {
                "name": col,
                "id": col,
                "type": "text",
                "editable": False,
            }
        )
    elif col in ["Begin", "End"]:
        columns.append(
            {
                "name": col,
                "id": col,
                "type": "numeric",
                "format": Format(
                    group_delimiter=":",
                    padding=Padding.yes,
                    padding_width=4 + 1,
                    group=Group.yes,
                    groups=[2],
                ),
            }
        )


app.layout = dash_table.DataTable(
    id="time-table",
    editable=True,
    columns=columns,
    data=data,
    active_cell=ACTIVE_CELL,
    style_data_conditional=[
        {
            "if": {
                "column_id": df.columns,
                "filter_query": "{Begin} > {End}",
            },
            "backgroundColor": "tomato",
        },
        {
            "if": {
                "column_id": ["Date", "DoW"],
                "filter_query": "{DoW} eq '土'",
            },
            "color": "blue",
        },
        {
            "if": {
                "column_id": ["Date", "DoW"],
                "filter_query": "{DoW} eq '日'",
            },
            "color": "red",
        },
    ],
)

cnt = 0
active_cell_previous = ACTIVE_CELL


@app.callback(
    Output("time-table", "data"),
    Input("time-table", "active_cell"),
    Input("time-table", "data_previous"),
    Input("time-table", "data"),
)
def goma(active_cell, data_previous, data):
    global cnt
    global active_cell_previous
    if active_cell_previous["column_id"] in ["Data", "DoW"]:
        # nothing to do
        active_cell_previous = active_cell
        return data
    else:
        row = active_cell_previous["row"]
        column_id = active_cell_previous["column_id"]
        value = data[row][column_id]
        print(f"type of {value}, {type(value)}")
        if isinstance(value, int):
            # e.g.
            # 145 -> 145
            # 12345 -> 2345
            # 99999 -> 9999
            value %= 10000
            # zero padding
            # 145 -> 0145
            # 2345 -> 2345
            # 9999 -> 9999
            str_value = str(value).zfill(4)
            # format with HH:MM
            # 0145 -> 01:45
            # 2345 -> 23:45
            # 9999 -> 99:99
            print(str_value)
            try:
                str_value = datetime.strptime(str_value, "%H:%M").strftime("%H:%M")
                data[row][column_id] = str_value
            except ValueError:
                # revert data with `previous_data`
                data[row][column_id] = data_previous[row][column_id]
                pass
        active_cell_previous = active_cell
        print(data[0])
    return data


if __name__ == "__main__":
    app.run_server(debug=True)
