from pathlib import Path
from typing import List
import base64
import json
import requests
import time
from datetime import datetime

# CONFIG
OUTPUT_DIRECTORY = 'output_directory'
INPUT_DIRECTORY = 'input_directory'
dataretrieval_url = 'https://apim-clients-common-northeurope-prod.azure-api.net/cv-demo/upload'
dataretrieval_request_data = {
    "binaryFile": "{base64_encoded_binary_file}",
    "filename": "test document 2 .pdf",
    "userCustomFields": {
        "documentId": "123",
        "candidateName": "Tester Testerovy",
        "requestorEmail": "tester@testerovy.cz"
    }
}
dataretrieval_request_headers = {
    'Content-Type': 'application/json',
    'apikey': '{API_KEY}'
}
datatransfer_url = 'https://apim-clients-common-northeurope-prod.azure-api.net/cv-demo/graphql'
datatransfer_query = """
query GetSingleRecord($id: ID!) {
  get_record(record_id: $id) {
    cv_language
    person {
      personal_information {
        names
        surnames
        date_of_birth
        age
      }
      contact_information {
        phone
        email
        address {
          street
          city
          house_number
          zip_code
        }
      }
      work_experience {
        company_name
        position
        start_date
        end_date
        achievements
      }
      education {
        school_name
        degree
        start_date
        end_date
        achievements
      }
      skills {
        language_skills {
          language
          level
        }
        hard_skills {
          skill_name
        }
        soft_skills {
          skill_name
          proficiency
        }
        driving_license {
          license_type
        }
      }
    }
  }
}
"""
datatransfer_headers = {
    'Content-Type': 'application/json',
    'apikey': '{API_KEY}'
}


def poll_for_result(api_key: str, record_id: str, interval: int = 3, timeout: int = 180):
    """
    Poll a REST API endpoint at regular intervals until a successful response is received or a timeout is reached.

    Args:
        api_key (str): API key for authentication.
        record_id (str): Record ID of the file to get.
        interval (int): The interval (in seconds) between each poll. Default is 5 seconds.
        timeout (int): The maximum time (in seconds) to keep polling. Default is 60 seconds.

    Returns:
        dict: The JSON response from the API if successful, otherwise None.
    """
    start_time = time.time()
    url, headers, payload = prepare_datatransfer_request_data(api_key, record_id)
    while True:
        try:

            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 200:
                response_data = response.json()
                get_record = response_data.get("get_record", {})
                if get_record.get("cv_language") is not None or get_record.get("person") is not None:
                    return response_data
            elif response.status_code == 400:
                error_response = response.json()
                if error_response.get("errorCode") == 1002:
                    print("Error: The record does not exist.")
                    return None
                else:
                    print(f"Error: Received 400 status code with response: {error_response}")
                    return None
            else:
                print(f"Received unexpected status code {response.status_code}: {response.text}")
        except requests.RequestException as e:
            print(f"An error occurred: {e}")

        if time.time() - start_time > timeout:
            print(f"Timeout for file with {record_id} reached. Stopping polling.")
            return None
        time.sleep(interval)


def prepare_datatransfer_request_data(api_key: str, record_id: str):
    datatransfer_headers['apikey'] = api_key
    datatransfer_variables = {
        "id": record_id,
    }
    datatransfer_payload = {
        'query': datatransfer_query,
        'variables': datatransfer_variables
    }
    return datatransfer_url, datatransfer_headers, json.dumps(datatransfer_payload)


def encode_file_to_base64(file_path: str) -> str:
    """
    Encode the content of a file to a Base64 string using UTF-8 encoding.

    Args:
        file_path (str): Path to the file to be encoded.

    Returns:
        str: Base64 encoded string of the file content.
    """
    try:
        path = Path(file_path)

        # Check if the file exists and is readable
        if not path.is_file():
            print(f"Error: The file {file_path} does not exist or is not a file.")
            exit(1)
        if not path.exists():
            print(f"Error: The file {file_path} cannot be read due to permissions.")
            exit(1)

        with path.open('rb') as file:
            file_content = file.read()
        base64_encoded = base64.b64encode(file_content).decode('utf-8')
        return base64_encoded

    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)


def get_filename(file_path: str) -> str:
    """
    Get the filename from a given file path.

    Args:
        file_path (str): The full path to the file.

    Returns:
        str: The filename extracted from the file path.
    """
    path = Path(file_path)
    return path.name


def prepare_dataretrieval_request_data(api_key: str, filepath: Path) -> (str, str, str):
    """
    Prepare request data for data retrieval API.

    Args:
        api_key (str): API key for the data retrieval API.
        filepath (Path): Absolute Path to the input file.

    Returns:
        tuple: Request data with API key included.
    """
    base64_encoded_binary_file = encode_file_to_base64(str(filepath.resolve()))
    dataretrieval_request_data['binaryFile'] = base64_encoded_binary_file
    dataretrieval_request_headers['apikey'] = api_key
    dataretrieval_request_data['filename'] = get_filename(filepath.name)
    dataretrieval_request_data['userCustomFields']['apiKey'] = api_key
    return dataretrieval_url, dataretrieval_request_headers, json.dumps(dataretrieval_request_data)


def get_files_with_extensions(directory: str = INPUT_DIRECTORY) -> List[Path]:
    """
    Get all file names from the given directory that have allowed extensions.

    Args:
        directory (str): Path to the directory to search.

    Returns:
        List[Path]: List of file names with allowed extensions.
    """
    allowed_extensions = ['.txt', '.jpg', '.png', '.pdf', '.docx', '.doc', '.jpg', '.odt', '.jpeg', '.rtf', '.png', '.html', '.bmp', '.htm']
    try:
        directory_path = Path(directory)
    except:
        print("""ERROR: Please provide a valid directory path.""")
        exit(1)
    files_with_allowed_extensions = []

    # Ensure extensions are in the correct format
    allowed_extensions = [ext.lower() if ext.startswith('.') else f'.{ext.lower()}' for ext in allowed_extensions]

    # Traverse the directory
    for file in directory_path.rglob('*'):
        if file.is_file() and any(file.suffix.lower() == ext for ext in allowed_extensions):
            files_with_allowed_extensions.append(file)

    if len(files_with_allowed_extensions) == 0:
        print("""ERROR: Please provide at least one allowed extension.""")
        exit(1)

    return files_with_allowed_extensions


def append_loaded_file(file: Path, dtret_response: dict) -> dict:
    new_object = {
        'file': file.name,
        'record_id': dtret_response['recordID'],
    }
    return new_object


def create_timestamp_for_folder() -> str:
    """
    Create a date-time timestamp string for folder names that is compliant across all operating systems.

    Returns:
        str: A timestamp string formatted as 'YYYY-MM-DD_HH-MM-SS'.
    """
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d_%H-%M-%S')
    return timestamp


def remove_extension(filename: str) -> str:
    """
    Remove the extension from a given filename.

    Args:
        filename (str): The filename from which to remove the extension.

    Returns:
        str: The filename without its extension.
    """
    return Path(filename).stem


def create_new_json_file_in_output_directory(directory_name: str, filename: str, file_extracted_data: dict, main_output_directory: str = OUTPUT_DIRECTORY):
    """
    Create a JSON file from given data and save it in the specified directory.

    Args:
        directory_name (str): The directory where the JSON file should be saved.
        filename (str): The name of the JSON file to be created.
        file_extracted_data (dict): The data to be saved in the JSON file.
        main_output_directory (str, optional): The main output directory. Defaults to OUTPUT_DIRECTORY.

    Returns:
        str: The path to the created JSON file.
    """
    # Ensure the directory exists
    main_output_directory = Path(main_output_directory)
    json_output_directory = main_output_directory / directory_name

    json_output_directory.mkdir(parents=True, exist_ok=True)

    # Define the full path for the JSON file
    json_file_path = json_output_directory / f'{remove_extension(filename)}.json'

    # Write the data to the JSON file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(file_extracted_data, json_file, ensure_ascii=False, indent=4)

    return str(json_file_path)
