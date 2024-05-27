import pandas as pd
from datetime import datetime, timedelta
import os
import time
import json


def process_touch_reports():
    found_files = []  # Define found_files here

    with open(r"C:\Users\vinod\Desktop", "r") as file:  # input file path
        file_paths = json.load(file)

    with open(r"C:\Users\vinod\Desktop",'a') as f:  # creating a log file and appending all the data in log.txt file
        for file_name, paths in file_paths.items():
            start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write("start_time : {0}\n".format(start_time))
            file_path = paths['input']
            output_path = paths['output']
            encodings = ['utf-8', 'latin-1', 'iso-8859-1']


            file_found_time = None
            not_found_times = []

            while True:  # writing a loop to check the file is found or not
                if os.path.exists(file_path):
                    if file_found_time is None:
                        file_found_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print("File {0} found at: {1}".format(file_name, file_found_time))
                        f.write("File {0} found at: {1}\n".format(file_name, file_found_time))
                        found_files.append(file_name)
                    break
                else:
                    if file_found_time is not None:
                        file_found_time = None
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    not_found_times.append(current_time)
                    print("file {0} not found at {1}. Waiting for 10 sec... ".format(file_name, current_time))
                    f.write("File {0} not found at {1}. Waiting for 10 sec...\n".format(file_name, current_time))
                    time.sleep(10)

            if file_name not in found_files:  # if the first file is not found go to 2nd file and execute
                continue

            for encoding in encodings:  # specifying the file format type
                try:
                    data = pd.read_csv(file_path, encoding=encoding, low_memory=False)
                    break
                except UnicodeDecodeError:
                    continue

            start_process = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(start_process)
            if file_name in ['BAE', 'IBS', 'OTM']:
                data.drop('DISPLAY LABEL', axis=1, inplace=True)  # Remove DISPLAY LABEL column for BAE, IBS, and OTM

            # Convert columns to appropriate types
            data['ACCOUNT NUMBER'] = data['ACCOUNT NUMBER'].str.replace('=', '').str.replace('"', '')
            data['ORDER NUM'] = data['ORDER NUM'].str.replace('=', '').str.replace('"', '')
            data['PHONE NUMBER 1'] = data['PHONE NUMBER 1'].str.replace('=', '').str.replace('"', '')
            data['TASK CREATION DATE'] = data['TASK CREATION DATE'].str.replace('/', '-')
            data['TASK CREATION DATE'] = pd.to_datetime(data['TASK CREATION DATE'], format="%m-%d-%y")

            # filtering data

            today = datetime.today()
            yesterday = today - timedelta(days=1)
            weekly = today - timedelta(days=3)
            #is_leap_year = (today.year % 4 == 0 and (today.year % 100 != 0 or today.year % 400 == 0))

            if today.month == 1:
                end_date = datetime(today.year - 1, 12, 29)  # Handle January case
            else:
                if today.month == 3 and today.day < 29:
                    end_date = datetime(today.year, today.month - 1, 28)
                else:
                    end_date = datetime(today.year, today.month - 1, 29)

            # daily report
            daily_report = data[(data['TASK CREATION DATE'] >= end_date) & (data['TASK CREATION DATE'] <= yesterday)]
            #daily_dummy = daily_report.head(10)
            yesterday_str = yesterday.strftime('%m%d%Y')

            weekly_report = None
            if today.weekday() == 0:  # Check if today is Monday
                weekly_report = data[(data['TASK CREATION DATE'] >= end_date) & (data['TASK CREATION DATE'] <= weekly)]
                #weekly_dummy = weekly_report.head(10)

            end_datestr = end_date.strftime('%m%d%Y')
            week_day = weekly.strftime('%m%d%Y')

            montly_report = None
            if today.day == 29:
                montly_report = data[(data['TASK CREATION DATE'] >= end_date) & (data['TASK CREATION DATE'] <= yesterday)]
            else:
                if today.month == 3 and today.day == 1:
                    not_leap_year = datetime(today.year, today.month - 2, 29)
                    montly_report = data[(data['TASK CREATION DATE'] >= not_leap_year) & (data['TASK CREATION DATE'] <= yesterday)]
           # fiscial_dummy = montly_report.head(10)
            fiscial_date = yesterday.strftime('%m%d%Y')

            reports = {
                file_name + '_O2_Touch_Report': daily_report
            }

            if weekly_report is not None:
                reports[file_name + '_O2_Touch_Report'] = weekly_report

            if montly_report is not None:
                reports[file_name + '_O2_Touch_report'] = montly_report

            # generating the output file as excel and csv
            for report_name, report_data in reports.items():
                csv_file_path = os.path.join(output_path, "{0}-{1}.csv".format(report_name, yesterday_str))
                excel_file_path = os.path.join(output_path, "{0}-{1}.xlsx".format(report_name, yesterday_str))
                if csv_file_path and excel_file_path:
                    report_data.to_csv(csv_file_path, index=False)
                    report_data.to_excel(excel_file_path, index=False)
                    if today.weekday() == 0 and weekly_report is not None:
                        csv_weekly_path = os.path.join(output_path, "{0}-{1}-{2}.csv".format(report_name, end_datestr, week_day))
                        excel_weekly_path = os.path.join(output_path, "{0}-{1}-{2}.xlsx".format(report_name, end_datestr, week_day))
                        weekly_report.to_csv(csv_weekly_path, index=False)
                        weekly_report.to_excel(excel_weekly_path, index=False)
                        if today.day == 29 or montly_report is not None:
                            csv_fiscial_path = os.path.join(output_path, "{0}-{1}-{2}.csv".format(report_name, end_datestr, fiscial_date))
                            excel_fiscial_path = os.path.join(output_path, "{0}-{1}-{2}.xlsx".format(report_name, end_datestr, fiscial_date))
                            montly_report.to_csv(csv_fiscial_path, index=False)
                            montly_report.to_excel(excel_fiscial_path, index=False)
                    end_timing = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            f.write("start process : {0}\n".format(start_process))
            f.write("Ending process: {0}\n".format(end_timing))
            f.write("\n")


# Usage
process_touch_reports()
