import requests  # This handles API requests
import json  # working with json data from API's


# this function returns the current city using IP address and router locations
def get_location():
    # using api get request to track ip address location
    url = "http://ipinfo.io/json"
    # get request to the API
    response = requests.get(url)
    # load data into dictionary
    data = json.loads(response.text)
    # return city
    return data['city']
