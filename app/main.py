import requests
from services import get_files_with_extensions, prepare_dataretrieval_request_data, append_loaded_file, poll_for_result, create_timestamp_for_folder, create_new_json_file_in_output_directory

# Replace with your API key
API_KEY = 'your-api-key-here'

files = get_files_with_extensions()

loaded_files = []
print('''
----------------------------------------------------------------
1) STARTING LOADING ALL FILES FROM INPUT DIRECTORY...
----------------------------------------------------------------
''')

# load the data to Granton AI ecosystem
for file in files:
    url, headers, data = prepare_dataretrieval_request_data(API_KEY, file)
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        new_object = append_loaded_file(file, response.json())
        loaded_files.append(new_object)
        print(f'File: [{file.name}] loaded. record_id: {new_object["record_id"]}')
    else:
        print(f'ERROR: {file.name} failed to load.')

print('\nAll files loaded to Granton AI ecosystem...')

print('''
----------------------------------------------------------------
2) STARTING GETTING THE DATA FROM GRANTON AI (can take a while, please be patient)
----------------------------------------------------------------
''')

# Get the data from Granton AI
directory_name = create_timestamp_for_folder()
for loaded_file in loaded_files:
    file_extracted_data = poll_for_result(API_KEY, loaded_file['record_id'])

    if file_extracted_data:
        json_file_path = create_new_json_file_in_output_directory(directory_name, loaded_file['file'], file_extracted_data)
        if json_file_path:
            print(f'FILE: [{loaded_file["file"]}] contents is now available in [{json_file_path}].')

print('''
----------------------------------------------------------------
3) ALL FILES PROCESSED 
----------------------------------------------------------------''')
