import json
import time
import requests
import argparse

def get_all_queries(jwt, host, port):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer %s" % (jwt)
    }
    for x in range (3):
        try:
            response = requests.get(f'http://{host}:{port}/api/v2/saved-queries', headers=headers, verify=False)
            if response.status_code == 200:
                break
            else:
                print(f"Failed to get queries with error code {response.status_code}")
        except Exception as e:
            print(f"Error occurred while sending request: {str(e)}")
        time.sleep(1)
    return response.json()

def send_requests(id,jwt, host, port):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer %s" % (jwt)
    }
    for x in range (3):
        try:
            response = requests.delete(f'http://{host}:{port}/api/v2/saved-queries/{id}', headers=headers, verify=False)
            if response.status_code == 204:
                print(f"Successfully delete query: '{id}'")
                break
            else:
                print(f"Failed to delete query: '{id}' with error code {response.status_code}")
        except Exception as e:
            print(f"Error occurred while sending request for '{id}': {str(e)}")
        time.sleep(1)

def main():
    parser = argparse.ArgumentParser(description='Import custom queries into BloodHound CE from a legacy BloodHound JSON file.', usage='python import-custom-bloodhound-queries.py --jwt eyJhbGciOiJIUz... [--host localhost] [--port 8080] [--file ./customqueries.json]')
    parser.add_argument('--jwt', type=str, required=True, help='Required: The JWT used for authentication. Open the Network tab of your browser after authenticating to BloodHound.')
    parser.add_argument('--host', type=str, default='localhost', help='Optional: Bloodhound host. Default is localhost.')
    parser.add_argument('--port', type=str, default='8080', help='Optional: BloodHound port. Default is 8080.')
    args = parser.parse_args()

    parsed_queries = get_all_queries(args.jwt, args.host, args.port)

    for query in parsed_queries["data"]:
        send_requests(query['id'], args.jwt, args.host, args.port)


if __name__ == "__main__":
    main()
