import re
from os import listdir


def get_screenshot_new_file_name(scenario_name, step_name, directory='reports'):
    step_file_name = '-'.join(step_name.split(' '))
    if re.search(r'@([\d]+).([\d]+)', scenario_name):
        # scenario name = 'scenario name -- @1.1' ==> file_name = scenario name_0_step name_[1,2,3,...].png
        # scenario name = 'scenario name -- @1.2' ==> file_name = scenario name_1_step name_[1,2,3,...].png
        scenario_simple_name, scenario_outline_index_str = re.search(r'(.+) -- @([\d]+).([\d]+)', scenario_name)\
            .group(1, 3)
        scenario_outline_index = int(scenario_outline_index_str) - 1
        scenario_file_name = '-'.join(scenario_simple_name.split(' '))
        file_name_no_intra_step_counter = scenario_file_name + '_' + str(scenario_outline_index) + '_' + step_file_name
    else:
        # scenario name = 'scenario name' ==> file_name = scenario name_step name_[1,2,3,...].png
        file_name_no_intra_step_counter = '-'.join(scenario_name.split(' ')) + '_' + step_file_name

    reports = listdir(directory)
    intra_step_screenshots_list = list(filter(
        lambda screenshot: re.search(file_name_no_intra_step_counter + '_([\d]+).png', screenshot), reports
    ))

    if intra_step_screenshots_list:
        intra_step_counter_list = list(map(
            lambda screenshot: int(re.search(r'.+_([\d]+).png', screenshot).group(1)),
            intra_step_screenshots_list
        ))
    else:
        intra_step_counter_list = [0]

    return 'reports/' + file_name_no_intra_step_counter + '_' + str(max(intra_step_counter_list) + 1) + '.png'
