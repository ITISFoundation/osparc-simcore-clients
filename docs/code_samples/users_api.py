from __future__ import print_function
import time
import osparc
from osparc.rest import ApiException
from pprint import pprint
configuration = osparc.Configuration()
# Configure HTTP basic authorization: HTTPBasic
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# Defining host is optional and default to http://localhost
configuration.host = "http://localhost"
# Enter a context with an instance of the API client
with osparc.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = osparc.UsersApi(api_client)
    
    try:
        # Get My Profile
        api_response = api_instance.get_my_profile()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UsersApi->get_my_profile: %s\n" % e)