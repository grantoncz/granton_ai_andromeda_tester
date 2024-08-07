# Document Processing and Data Retrieval Script

This repository contains a simple Python script designed to upload documents to one API and then retrieve the processed data from another API. This guide will walk you through setting up and running the script from scratch.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [File Structure](#file-structure)
6. [Contributing](#contributing)
7. [License](#license)

## Prerequisites

Before running the script, ensure you have the following installed:
- Python 3.x
- `requests` library (installable via pip)
- An API key for accessing the APIs

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. **Install required Python packages:**
   ```bash
   pip install requests
   ```

## Configuration

1. **API Key:**
   Replace the placeholder `your-api-key-here` with your actual API key in the script.

   ```python
   API_KEY = 'your-api-key-here'
   ```

2. **Input Directory:**
   Ensure you have an input directory containing the documents you want to process. The script will automatically look for files with specific extensions in this directory.

## Usage

To run the script, use the following command:

```bash
python app/main.py
```

The script performs the following steps:

1. **Loading Files:**
   It retrieves all files from the input directory and uploads them to the Granton AI ecosystem. Each file's status is printed to the console.

2. **Retrieving Data:**
   After uploading, the script polls the API to retrieve the processed data. This step might take some time, so please be patient.

3. **Saving Results:**
   The retrieved data is saved as JSON files in an output directory, named with a timestamp to ensure uniqueness.

### Example Output

```
----------------------------------------------------------------
1) STARTING LOADING ALL FILES FROM INPUT DIRECTORY...
----------------------------------------------------------------
File: [example1.pdf] loaded. record_id: cd900703-34xf-4y45-82ba-0a42a6ce5f12
File: [example2.pdf] loaded. record_id: cd876703-34fe-4e45-836y-1b42a6ce5f00

All files loaded to Granton AI ecosystem...

----------------------------------------------------------------
2) STARTING GETTING THE DATA FROM GRANTON AI (can take a while, please be patient)
----------------------------------------------------------------
FILE: [example1.txt] contents is now available in [output_directory/2024-08-07_12-34-56/example1.json].
FILE: [example2.txt] contents is now available in [output_directory/2024-08-07_12-34-56/example2.json].

----------------------------------------------------------------
3) ALL FILES PROCESSED
----------------------------------------------------------------
```

## File Structure
```
repo/
|
├── README.md                   # This README file
├── app
│   ├── main.py                 # Main script file
│   ├── requirements.txt        # List of dependencies
│   └── services.py             # Auxiliary functions for the script
├── input_directory             # Directory containing input files
└── output_directory            # Directory for output JSON files
```
