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
        count = event['ResourceProperties']['TerraformVariables']['count']
        
        LOGGER.info("Requested Hostname is : " + instancename)
        LOGGER.info("Requested subnet is : " + subnet)
        LOGGER.info("Requested vmtype is : " + instancetype)
        LOGGER.info("Requested keyname is : " + keyname)
        LOGGER.info("Number of VMs is : " + count)
        
        # ------- Added by si --------------
        url = "https://gitlabv2.chrisley.fr/api/v4/projects/4/trigger/pipeline"
        payload = {'token': '8b7e8be6b87a41672bf133a561cac3','ref': 'master', 'variables[TF_VAR_instance_name]': instancename, 'variables[TF_VAR_instance_type]': instancetype, 'variables[TF_VAR_key_pair]': keyname, 'variables[TF_VAR_number_vm]': count, 'variables[TF_VAR_subnet_id]': subnet}
        response = requests.request("POST", url, data = payload)
        # ---------------------------------------------------------------------------
        
        ## Example for adding a host in AWX inventory
        #url = 'http://15.236.21.16/api/v2/inventories/34/hosts/'
        
        #my_headers = {"Content-Type": "application/json", "Authorization" : "Basic YWRtaW46b29DaGlldG9qNA=="}
        
        data = {
            "Task": "Created by gitops pipeline"
        }
        
        #response = requests.post(url, headers=my_headers, json=data)
        
    except BaseException as ex:
        LOGGER.exception(ex)

    finally:
        cfnresponse.send(event=event, context=context, responseStatus=status, responseData=data)

def _update_instance(event, context):
    return _create_instance(event, context)

def _delete_instance(event, context):
    instancename = event['ResourceProperties']['GlobalVariables']['instancename']
    subnet = event['ResourceProperties']['TerraformVariables']['subnet']
    instancetype = event['ResourceProperties']['TerraformVariables']['instancetype']
    keyname = event['ResourceProperties']['TerraformVariables']['keyname']
    status = cfnresponse.SUCCESS

    try:
        # Retrieve data from event
        LOGGER.info("Delete ec2 instance event" )
        url = "https://gitlabv2.chrisley.fr/api/v4/projects/3/trigger/pipeline"
        payload = {'token': 'pwsjNZSPXuA4f1GpcFhM','ref': 'master', 'variables[TF_VAR_instance_type]': instancetype}
        response = requests.request("POST", url, data = payload)
        data = {
            "Task": "Terminated by gitops pipeline"
        }
    except BaseException as ex:
        LOGGER.exception(ex)

    finally:
        cfnresponse.send(event=event, context=context, responseStatus=status, responseData=data)
