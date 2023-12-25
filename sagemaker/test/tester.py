import json
import requests

Test_example = { "data": "52, 1, 1, 128, 205, 1, 1, 184, 0, 0, 2, 0, 2" }
Appended_url = f'https://https://lqmm19wey7.execute-api.us-west-2.amazonaws.com/Alpha/sagemaker_api_resource'

response = requests.post(Appended_url, json=Test_example).json()
print(json.dumps(response, indent=4))