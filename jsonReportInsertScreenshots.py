import base64
from glob import glob
import re
import json
import argparse
from screenshotFileName import get_screenshot_new_file_name


def update_step_with_screenshot(step, file_name):

    screenshot = open(file_name, "rb")

    if 'embeddings' not in step.keys():
        step['embeddings'] = []
    step['embeddings'].append(
            {
                'mime_type': "image/png",
                'data': base64.b64encode(screenshot.read()).decode('utf-8')
            }
        )


def update_feature(feature, directory):

    for scenario in feature['elements']:

        for step in filter(lambda lstep: lstep['result']['status'] == 'failed',  scenario['steps']):

            next_file_name = get_screenshot_new_file_name(
                scenario['name'],
                step['keyword'] + ' ' + step['name'],
                directory
            )

            base_name = re.search(r'(.+)_([\d]+).png', next_file_name).group(1)
            for screenshot_file in glob(f'{base_name}_*.png'):
                update_step_with_screenshot(step, screenshot_file)


def main():

    parser = argparse.ArgumentParser(description='Insert png screenshots data into Behave Json Report')
    parser.add_argument('-r', '--report', required=True, type=open,
                        help='JSON Behave report file (with its relative path')
    parser.add_argument('-d', '--screenshots_directory', required=True,
                        help='Directory where the screenshots are')

    args = parser.parse_args()

    # load json report as python dict
    report_dict = json.load(args.report)

    for feature in filter(lambda lfeature: lfeature['status'] != 'skipped',  report_dict):
        update_feature(feature, args.screenshots_directory)

    print(report_dict)


if __name__ == "__main__":
    main()