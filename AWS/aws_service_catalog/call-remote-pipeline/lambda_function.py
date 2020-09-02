# Any code, applications, scripts, templates, proofs of concept, documentation
# and other items provided by AWS under this SOW are "AWS Content,"" as defined
# in the Agreement, and are provided for illustration purposes only. All such
# AWS Content is provided solely at the option of AWS, and is subject to the
# terms of the Addendum and the Agreement. Customer is solely responsible for
# using, deploying, testing, and supporting any code and applications provided
# by AWS under this SOW.
#
# (c) 2019 Amazon Web Services

import os
import logging
import json
import cfnresponse
import urllib3
from botocore.exceptions import ClientError
from botocore.vendored import requests


# Configure logging
LOGGER = logging.getLogger(__name__)
DEBUG_MODE = os.getenv('DEBUG_MODE', 'true')
if DEBUG_MODE == 'true':
    LOGGER.setLevel(logging.DEBUG)
else:
    LOGGER.setLevel(logging.INFO)


def lambda_handler(event, context):
    """ Lambda Function for command execution """
    LOGGER.info("Received event: " + json.dumps(event, indent=2))

    request_type = event['RequestType']
    if request_type == 'Create':
        _create_instance(event, context)
    elif request_type == 'Delete':
        _delete_instance(event, context)
    elif request_type == 'Update':
        _update_instance(event, context)


def _create_instance(event, context):
    status = cfnresponse.SUCCESS

    try:
        # Retrieve data from event
        
        instancename = event['ResourceProperties']['GlobalVariables']['instancename']
        subnet = event['ResourceProperties']['TerraformVariables']['subnet']
        instancetype = event['ResourceProperties']['TerraformVariables']['instancetype']
        keyname = event['ResourceProperties']['TerraformVariables']['keyname']
        
        LOGGER.info("Requested Hostname is : " + instancename)
        LOGGER.info("Requested subnet is : " + subnet)
        LOGGER.info("Requested vmtype is : " + instancetype)
        LOGGER.info("Requested keyname is : " + keyname)
        
        ## Example for adding a host in AWX inventory
        url = 'http://15.236.21.16/api/v2/inventories/34/hosts/'
        my_headers = {"Content-Type": "application/json", "Authorization" : "Basic YWRtaW46b29DaGlldG9qNA=="}
        
        data = {
            "name": instancename
        }
        
        response = requests.post(url, headers=my_headers, json=data)
        
    except BaseException as ex:
        LOGGER.exception(ex)

    finally:
        cfnresponse.send(event=event, context=context, responseStatus=status, responseData=data)

def _update_instance(event, context):
    return _create_instance(event, context)

def _delete_instance(event, context):

    status = cfnresponse.SUCCESS
    data = {""}

    try:
        # Retrieve data from event
        LOGGER.info("Delete event" )

    except BaseException as ex:
        LOGGER.exception(ex)

    finally:
        cfnresponse.send(event=event, context=context, responseStatus=status, responseData=data)