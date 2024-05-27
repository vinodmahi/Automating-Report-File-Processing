# Touch Report Processor

# Overview


This Python script is designed to process touch reports, generating daily, weekly, and monthly reports in both CSV and Excel formats. It monitors specified file paths for input files, processes them, and saves the generated reports to designated output directories.

# Features
Automatic File Detection: Continuously checks specified file paths for the presence of input files.

Encoding Flexibility: Supports multiple encodings for reading input files.

Dynamic Date Range: Generates reports based on dynamic date ranges such as daily, weekly, and monthly.

File Format Handling: Handles different file formats and converts them into appropriate types.

Output Versatility: Saves reports in both CSV and Excel formats.

Logging: Maintains a log file recording the start and end times of each processing cycle.

# Getting Started
1. Prerequisites
2. Python 3.x
3. pandas library
4. Installation

# Configuration

Adjust the file_paths.txt file to specify input and output file paths.
Modify the encodings list in the script to include additional encodings if necessary.
Customize the logic for date ranges and data filtering based on your requirements.
