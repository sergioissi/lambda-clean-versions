"""
Removes old versions of Lambda functions.
"""
import logging
import sys
from pathlib import Path
file = Path(__file__).resolve()
sys.path.append(str(file.parent))
import logger
import boto3


# Initialize log
logger.logger_init()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
logger.propagate = False


try:
    CLIENT = boto3.client('lambda', region_name='eu-west-1')
except Exception as exception:
    logger.error(str(exception), exc_info=True)

# Number of versions to keep
KEEP_LAST = 10

def clean_lambda_versions(event, context):
    """
    List all Lambda functions and call the delete_version function.
    Check if the paginator token exist that's included if more results are available.
    """
    next_marker = None
    try:
        response = CLIENT.list_functions()
    except UnboundLocalError as error:
        logger.error(str(error), exc_info=True)
    except Exception as exception:
        logger.error(str(exception), exc_info=True)
    while next_marker != '':
        next_marker = ''
        for functions in response['Functions']:
            func_arn = functions['FunctionArn']
            # Only production functions (production is part of the name of the lambda)
            if "production" in func_arn:
                delete_version(func_arn)
        # Verify if there is next marker
        if 'NextMarker' in response:
            next_marker = response['NextMarker']
            response = CLIENT.list_functions(
                Marker=next_marker
            )

def delete_version(func_arn):
    """
    Delete a specific function version using Qualifier parameter and keeping the last KEEP_LAST versions.
    Check if the paginator token exist that's included if more results are available.
    """
    next_marker = None
    try:
        response = CLIENT.list_versions_by_function(
            FunctionName=func_arn
        )
    except UnboundLocalError as error:
        logger.error(str(error), exc_info=True)
    except Exception as exception:
        logger.error(str(exception), exc_info=True)
    while next_marker != '':
        next_marker = ''
        function_versions = response['Versions']
        for function_version in function_versions[:-KEEP_LAST]:
            if function_version['Version'] != '$LATEST':
                try:
                    logger.info("Deleting function version: %s:%s ",
                                function_version['FunctionName'], function_version['Version'])
                    CLIENT.delete_function(
                        FunctionName=function_version['FunctionName'],
                        Qualifier=function_version['Version'],
                    )
                    logger.info("Successfully deleted function version: %s:%s",
                                function_version['FunctionName'], function_version['Version'])
                except Exception as exception:
                    logger.error(str(exception), exc_info=True)
        # Verify if there is next marker
        if 'NextMarker' in response:
            next_marker = response['NextMarker']
            response = CLIENT.list_versions_by_function(
                FunctionName=func_arn,
                Marker=next_marker
            )

if __name__ == '__main__':
    clean_lambda_versions([], None)
