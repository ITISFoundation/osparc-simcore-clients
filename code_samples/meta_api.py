from __future__ import print_function
import time
import osparc
from osparc.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with osparc.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = osparc.MetaApi(api_client)
    extended_info = False # bool |  (optional) (default to False)

    try:
        # Get Service Metadata
        api_response = api_instance.get_service_metadata(extended_info=extended_info)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling MetaApi->get_service_metadata: %s\n" % e)
        