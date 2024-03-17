import sys
import requests

def main(file_path):

    # Set the URL you want to send the POST request to
    url = 'http://localhost:5000/rates'



    # Set the file path as a regular form field
    data = {'file': file_path}

    # Make the POST request
    response = requests.post(url, data=data)

    # Check the response
    print(response.text)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    main(file_path)