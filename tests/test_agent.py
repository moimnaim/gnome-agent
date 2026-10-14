# This file is part of Prometheus
# https://inl.gov/super-intelligence/prometheus/
#
# Copyright 2026 Battelle Energy Alliance, LLC
# All rights reserved, see NOTICE.txt for full restrictions
# https://github.com/idaholab/prometheus_core/blob/main/NOTICE.txt
#
# Licensed under the MIT License, please see LICENSE for details
# https://github.com/idaholab/prometheus_core/blob/main/LICENSE
#
# SPDX-License-Identifier: MIT

"""Tests for the Gnome Agent agent's `_execute` logic.

Extend these as you implement your agent: every input-validation branch and
every distinct result shape deserves a test. Run with `uv run pytest`.
"""
import pandas as pd

from agent import GnomeAgentAgent


def _make_agent() -> GnomeAgentAgent:
    # agent_card.json is loaded lazily by run()/build_app(), not by the
    # constructor, so unit tests can instantiate the agent directly.
    return GnomeAgentAgent(agent_name="Gnome Agent Agent")

'''
# This input is no longer valid, need to fix
async def test_execute_returns_success_for_valid_input(context, event_queue):
    agent = _make_agent()

    result = await agent._execute({"input_data": "hello"}, context, event_queue)

    assert result["status"] == "success"
    assert result["input_received"] == "hello"
    # The progress update was emitted through the event queue.
    assert event_queue.enqueue_event.await_count >= 1
'''

async def test_execute_rejects_missing_input(context, event_queue):
    agent = _make_agent()

    result = await agent._execute({}, context, event_queue)

    assert result["status"] == "error"
    assert "input_data" in result["error"]

async def test_markdown_to_csv(context, event_queue):
    # Load the test document
    # Specify the path to your markdown file
    file_path = "tests/data/hollowmere_almanac.md"

    # Open the file and read its contents into a string
    with open(file_path, "r", encoding="utf-8") as file:
        markdown_string = file.read()

    agent = _make_agent()
    result = agent.markdown_to_csv(markdown_string)

#    print(result)

    # Check that the number of tables is correct
    assert len(result) == 3

    assert result[0][0] == "**Table 1. Registered population of the three gnome villages of Hollowmere Valley, as counted at the midsummer census each year from 2010 to 2024.** The total column includes itinerant tinkers who happened to be in the valley on census night."
    assert result[1][0] == "**Table 2. Monthly rainfall and wild mushroom harvest in the Whispering Wood for the year 2023, with the average market price fetched at the Mossbury Saturday market.** Yields are the combined baskets of all licensed foragers; unlicensed foraging is, as ever, assumed to be considerable."
    assert result[2][0] == "**Table 3. Vital statistics of the dragons resident in the Hollowmere caves, taken from the Spring 2024 Draconic Register, including each dragon's age, wingspan, measured top speed, and declared favourite snack.** Speeds were measured by stopwatch over the Long Meadow and should be treated as approximate."

    assert list(result[0][1].columns) == ['Year', 'Thistledown', 'Mossbury', 'Pebblewick', 'Total']
    assert result[0][1].values.tolist() == [[2010, 416, 382, 172, 974], [2011, 412, 389, 180, 995], [2012, 424, 380, 201, 1014], [2013, 419, 372, 219, 1026], [2014, 415, 369, 226,1026], [2015, 410, 377, 234, 1031], [2016, 424, 387, 257, 1072], [2017, 436, 395, 274, 1109], [2018, 437, 386, 296, 1126], [2019, 440, 389, 305, 1140], [2020, 452, 388, 327, 1175], [2021, 449, 396, 350, 1204], [2022, 454, 389, 372, 1220], [2023, 466, 380, 396, 1251], [2024, 475, 391, 418, 1300]]
    assert list(result[1][1].columns) == ['Month', 'Rainfall (mm)', 'Chanterelle yield (kg)', 'Porcini yield (kg)', 'Average price (copper per kg)']
    assert result[1][1].values.tolist() == [['January', 89.4, 9.7, 7.5, 34.6], ['February', 96.0, 6.8, 6.7, 35.2], ['March', 81.8, 10.0, 4.1, 36.0], ['April', 56.7, 5.7, 5.1, 36.6], ['May', 37.5, 59.3, 4.5, 26.9], ['June', 48.2, 145.6, 6.7, 21.2], ['July', 82.4, 188.5, 35.0, 19.4], ['August', 93.1, 140.9, 93.6, 19.0], ['September', 78.0, 57.3, 123.9, 19.7], ['October', 57.9, 9.5, 96.3, 23.4], ['November', 37.6, 14.4, 34.1, 27.9], ['December', 54.9, 7.2, 3.7, 38.3]]     
    assert list(result[2][1].columns) == ['Dragon', 'Age (years)', 'Wingspan (m)', 'Top speed (km/h)', 'Favourite snack']
    assert result[2][1].values.tolist() == [['Ember', 14, 3.9, 92, 'toasted marshmallows'], ['Grumblewick', 87, 10.7, 163, 'pickled herring'], ['Saffron', 31, 5.7, 108, 'honey cakes'], ['Old Tallow', 212, 17.4, 125, 'roast chestnuts'], ['Nib', 6, 3.2, 74, 'blackberries'], ['Marigold', 45, 7.5, 133, 'smoked eel'], ['Vesper', 63, 8.6, 146, 'gingerbread'], ['Pudding', 19, 4.2, 88, 'pudding']]


async def test_plot_table_index(context, event_queue):
    # Load the csv data based on column indices
    # Specify the path to your csv file
    file_path = "tests/data/test.csv"
    output_file = "plot_table.png"

    agent = _make_agent()
    result = agent.plot_csv_xy(file_path=file_path, png_file=output_file)

    print(result)

async def test_plot_table_exact_name(context, event_queue):
    # Load the csv data based on column indices
    # Specify the path to your csv file
    file_path = "tests/data/test.csv"
    output_file = "plot_table_2.png"

    agent = _make_agent()
    result = agent.plot_csv_xy(file_path=file_path, x_col="time", y_col="flow", png_file=output_file)

    print(result)


async def test_markdown_to_csv_no_bold(context, event_queue):
    # Load the test document
    # Specify the path to your markdown file
    file_path = "tests/data/hollowmere_almanac_no_bold.md"

    # Open the file and read its contents into a string
    with open(file_path, "r", encoding="utf-8") as file:
        markdown_string = file.read()

    agent = _make_agent()
    result = agent.markdown_to_csv(markdown_string)

    # Check that the number of tables is correct
    assert len(result) == 3

    assert result[0][0] == "Table 1. Registered population of the three gnome villages of Hollowmere Valley, as counted at the midsummer census each year from 2010 to 2024. The total column includes itinerant tinkers who happened to be in the valley on census night."
    assert result[1][0] == "Table 2. Monthly rainfall and wild mushroom harvest in the Whispering Wood for the year 2023, with the average market price fetched at the Mossbury Saturday market. Yields are the combined baskets of all licensed foragers; unlicensed foraging is, as ever, assumed to be considerable."
    assert result[2][0] == "Table 3. Vital statistics of the dragons resident in the Hollowmere caves, taken from the Spring 2024 Draconic Register, including each dragon's age, wingspan, measured top speed, and declared favourite snack. Speeds were measured by stopwatch over the Long Meadow and should be treated as approximate."
  
    assert list(result[0][1].columns) == ['Year', 'Thistledown', 'Mossbury', 'Pebblewick', 'Total']
    assert result[0][1].values.tolist() == [[2010, 416, 382, 172, 974], [2011, 412, 389, 180, 995], [2012, 424, 380, 201, 1014], [2013, 419, 372, 219, 1026], [2014, 415, 369, 226,1026], [2015, 410, 377, 234, 1031], [2016, 424, 387, 257, 1072], [2017, 436, 395, 274, 1109], [2018, 437, 386, 296, 1126], [2019, 440, 389, 305, 1140], [2020, 452, 388, 327, 1175], [2021, 449, 396, 350, 1204], [2022, 454, 389, 372, 1220], [2023, 466, 380, 396, 1251], [2024, 475, 391, 418, 1300]]
    assert list(result[1][1].columns) == ['Month', 'Rainfall (mm)', 'Chanterelle yield (kg)', 'Porcini yield (kg)', 'Average price (copper per kg)']
    assert result[1][1].values.tolist() == [['January', 89.4, 9.7, 7.5, 34.6], ['February', 96.0, 6.8, 6.7, 35.2], ['March', 81.8, 10.0, 4.1, 36.0], ['April', 56.7, 5.7, 5.1, 36.6], ['May', 37.5, 59.3, 4.5, 26.9], ['June', 48.2, 145.6, 6.7, 21.2], ['July', 82.4, 188.5, 35.0, 19.4], ['August', 93.1, 140.9, 93.6, 19.0], ['September', 78.0, 57.3, 123.9, 19.7], ['October', 57.9, 9.5, 96.3, 23.4], ['November', 37.6, 14.4, 34.1, 27.9], ['December', 54.9, 7.2, 3.7, 38.3]]
    assert list(result[2][1].columns) == ['Dragon', 'Age (years)', 'Wingspan (m)', 'Top speed (km/h)', 'Favourite snack']
    assert result[2][1].values.tolist() == [['Ember', 14, 3.9, 92, 'toasted marshmallows'], ['Grumblewick', 87, 10.7, 163, 'pickled herring'], ['Saffron', 31, 5.7, 108, 'honey cakes'], ['Old Tallow', 212, 17.4, 125, 'roast chestnuts'], ['Nib', 6, 3.2, 74, 'blackberries'], ['Marigold', 45, 7.5, 133, 'smoked eel'], ['Vesper', 63, 8.6, 146, 'gingerbread'], ['Pudding', 19, 4.2, 88, 'pudding']]

