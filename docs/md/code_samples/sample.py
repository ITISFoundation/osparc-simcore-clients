from __future__ import print_function
import time
import osparc
from osparc.rest import ApiException
from osparc.configuration import Configuration
from pprint import pprint
from osparc.models import Meta

cfg = Configuration(host="https://api.osparc.io")

# Enter a context with an instance of the API client
with osparc.ApiClient(cfg) as api_client:
    # Create an instance of the API class
    meta_api = osparc.MetaApi(api_client)

    try:
        # Get Service Metadata
        #meta: Meta = meta_api.get_service_metadata()
        meta, status_code, headers = meta_api.get_service_metadata_with_http_info()
        pprint(meta)
    except ApiException as e:
        print("Exception when calling MetaApi->get_service_metadata: %s\n" % e)
        import pdb; pdb.set_trace()
    import pdb; pdb.set_trace()