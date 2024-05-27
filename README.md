Touch Report Processor
Overview
This Python script is designed to process touch reports, generating daily, weekly, and monthly reports in both CSV and Excel formats. It monitors specified file paths for input files, processes them, and saves the generated reports to designated output directories.

Features
Automatic File Detection: Continuously checks specified file paths for the presence of input files.
Encoding Flexibility: Supports multiple encodings for reading input files.
Dynamic Date Range: Generates reports based on dynamic date ranges such as daily, weekly, and monthly.
File Format Handling: Handles different file formats and converts them into appropriate types.
Output Versatility: Saves reports in both CSV and Excel formats.
Logging: Maintains a log file recording the start and end times of each processing cycle.
Getting Started
Prerequisites
Python 3.x
pandas library
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/touch-report-processor.git
Navigate to the project directory:

bash
Copy code
cd touch-report-processor
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Usage
Modify the file_paths.txt file to specify the input and output file paths for your touch reports.

Run the script:

bash
Copy code
python touch_report_processor.py
The script will continuously monitor the specified input file paths. When it finds a new input file, it will process it and generate the required reports.

Configuration
Adjust the file_paths.txt file to specify input and output file paths.
Modify the encodings list in the script to include additional encodings if necessary.
Customize the logic for date ranges and data filtering based on your requirements.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Hat tip to anyone whose code was used
Inspiration
etc.
