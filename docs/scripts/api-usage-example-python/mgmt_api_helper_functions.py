# Copyright © Check Point Software Technologies Ltd.
# Management API Example Tool - 1.0.0
# Terms & Conditions: https://www.checkpoint.com/about-us/cloud-terms/
# This code example can be copied and reused


import uuid
from vars import *
from vars import *
import requests
from mgmt_api_helper_functions import *
import time
from urllib3.util.retry import Retry, MaxRetryError
from urllib3.response import HTTPResponse
from requests.adapters import HTTPAdapter
import requests
import vars
from json import dumps, loads


def generate_random_hex():
    return str(uuid.uuid4())[0:4]


def generate_full_random_hex():
    return str(uuid.uuid4())



# used only on REST API requests (in this test only authentication)
def create_request_url(path):
    return "{}{}".format(vars.CLOUD_INFRA_HOST, path)

# used only on REST API requests (in this test only authentication)
def parse_response(response_type, orig_response, description):
    try:
        if response_type == 'text':
            return orig_response.text
        else:
            return orig_response.json()
    except Exception as err:
        raise ApiTesterException("Failed to parse response - {} - err: {}".format(description,
                                                                                  repr(err)))


def publish_changes():
    """
    Executes a "publish changes" mutation with graphql-client
    """
    publish_res = perform_infinity_request(query_or_mutation=PUBLISH_MUTATION,
                                      version=1,
                                      description="Publish Changes")
    # check if publish was successful
    if not publish_res['data'][PUBLISH_MUTATION_NAME]['isValid']:
        raise ApiTesterException("Failed - Publish Changes")
    print("Publishing Changes")


def enforce_policy():
    """
    Executes an "enforce new policy" mutation with graphql-client
    :return: The enforce policy task id
    """
    enforce_policy_res = perform_infinity_request(query_or_mutation=ENFORCE_MUTATION,
                                             version=1,
                                             description="Enforce Policy")
    task_id = enforce_policy_res['data'][ENFORCE_MUTATION_NAME]['id']
    print("Enforce Policy")
    return task_id


def wait_for_enforce_policy_status(task_id):
    """
    Executes a "get task" query with graphql-client until
    the status is "Succeeded".
    :param task_id: The "enforce policy action" task id
    """
    number_of_retries = 0
    sleep_between_retries = 1
    while not check_enforce_policy_status(task_id):
        number_of_retries += 1
        sleep_between_retries *= 2
        print("Check Enforce Policy Status - sleeping for {} seconds and retrying".format(sleep_between_retries))
        time.sleep(sleep_between_retries)
        if number_of_retries == CHECK_ENFORCE_STATUS_RETRIES:
            raise ApiTesterException('Check Enforce Policy Status - Failed after {} retries'.format(number_of_retries))
    print("Policy was Enforced")


def check_enforce_policy_status(task_id):
    """
    Executes a get "task query" with graphql-client.
    Raises exception is status is "Failed"
    :param task_id: The "enforce policy action" task id
    :return: A boolean indicating weather the enforce policy action
             was successful or not
    """
    task_variables = {
        "id": task_id
    }
    check_status_res = perform_infinity_request(query_or_mutation=CHECK_ENFORCE_STATUS_QUERY,
                                           version=1,
                                           variables=task_variables,
                                           description="Check Enforce Policy Status",
                                           raise_exception=False)
    if check_status_res['data'][CHECK_ENFORCE_STATUS_QUERY_NAME]['status'] == 'Failed':
        raise ApiTesterException("Enforce Policy Status id Failed")
    if check_status_res['data'][CHECK_ENFORCE_STATUS_QUERY_NAME]['status'] == 'Succeeded':
        return True
    return False


def discard_changes(failure_stage):
    """
    Executes a "discard changes" mutation with graphql-client.
    This is done if test failed before publishing changes
    :param failure_stage: The test stage that failed
    """
    try:
        client = InfiNextGraphQLClient(endpoint=vars.GRAPHQL_CLIENT_ENDPOINT, headers=vars.all_requests_headers)
    except Exception as clientError:
        print("Failed to initialize GraphQl client on discard changes. Python Exception: {}".format(repr(clientError)))
        return
    try:
        res = client.execute(query=DISCARD_CHANGES_MUTATION, variables=None)
    except Exception as err:
        print("Failed to Discard Changes after {} - Python exception: {}".format(failure_stage, repr(err)))
        return
    if res.status_code != 200:
        print("Failed to Discard Changes after {}".format(failure_stage))
    else:
        print("Discard changes")
        print(failure_stage)

def perform_infinity_request(query_or_mutation='', version=0, variables=None, description='',
                        raise_exception=True):
    """
    Sends a query via graphql client
    :param query_or_mutation: The query to execute
    :param version: the API version to access
    :param variables: The variables (parameters) of the query
    :param description: A short description of the query
    :param raise_exception: A boolean indicating weather to raise exception upon failure
                            or not
    :return: The json response returned from the graphql client endpoint
    """

    if version == 1:
        endpoint = vars.GRAPHQL_CLIENT_ENDPOINT_V1
    else:
        endpoint = vars.GRAPHQL_CLIENT_ENDPOINT
    try:
        client = InfiNextGraphQLClient(endpoint, headers=vars.all_requests_headers)
    except Exception as clientError:
        raise ApiTesterException("Failed to initialize GraphQl client on request - {}. Python Exception: {}".format(description,
                                                                                                                    repr(clientError)))
    failure_message = "Failed - {}".format(description)
    start = time.time()
    try:
        res = client.execute(query=query_or_mutation, variables=variables)
    # this means the request was not handle due to connectivity problems, etc..
    except Exception as err:
        failure_message = "Python requests/graphql-client exception on {} - exception: {}".format(description,
                                                                                                  str(repr(err)))
        raise ApiTesterException(failure_message)

    try:
        json_res = res.json()
    except Exception as err:  # response cannot be parsed to json - should not happen!
        raise ApiTesterException("Failed - Response cannot be parsed to json - {}".format(description))

    if res.status_code != 200 and raise_exception:
        raise ApiTesterException(failure_message)

    return json_res


# used only on REST API (in this test only authentication)
def perform_request(path, method, json_data=None, response_type="json", description="",
                    is_status_code_exception=True, add_body=True):
    """
    Sends all requests of test and logs where necessary
    :param path: The path to send the request to
    :param method: The request method
    :param json_data: The request body
    :param response_type: The response type to be returned
    :param description: Short Description of the request
    :param add_body: A boolean indicating weather to add request body content to the test log
    :param is_status_code_exception: A boolean indicating weather an exception should
                                     be raised if status code is not 200
    """
    request_session = create_session(response_type, description)

    request_url = create_request_url(path)


    failure_message = "Failed - {}".format(description)
    try:
        orig_res = request_session.request(method=method.upper(), url=request_url,
                                           headers=vars.all_requests_headers, json=json_data)

    # this means the request was not handle due to connectivity problems, etc..
    except Exception as err:
        end = time.time()
        failure_message = "Python requests exception on {} - exception: {}".format(description,
                                                                                   str(repr(err)))
        request_session.close()
        raise ApiTesterException(failure_message)

    request_session.close()
    parsed_response = parse_response(response_type, orig_res, description)

    if orig_res.status_code != 200:
        raise ApiTesterException(failure_message)

    return parsed_response

curr_retries_list = []

curr_retry_num = 0


def create_session(response_type, description):
    retry_strategy = CallbackRetry(
        total=vars.REQUESTS_NUMBER_OF_RETRIES,
        status_forcelist=vars.REQUESTS_STATUS_CODES_RETRY,
        method_whitelist=vars.REQUESTS_METHODS_LIST_RETRY,
        backoff_factor=vars.REQUESTS_EXP_SLEEP_RETRY,
        raise_on_status=False,
        callback=add_retry_response_and_status_code,
        response_type=response_type,
        description=description,
        retry_num=1
    )

    request_session = requests.Session()
    adapter = HTTPAdapter(max_retries=retry_strategy)
    request_session.mount("https://", adapter)
    request_session.mount("http://", adapter)
    return request_session


def add_retry_response_and_status_code(response, response_type, description):
    """
    This function is called upon each retry and appends the last response and status code
    to the appropriate key in the log
    :param response: The last response
    :param response_type: The parsing type of the last response (json or test)
    :param description: A short description of the last failed request
    :return A dictionary representing the last retry response
    """
    parsed_response = parse_http_response(response_type, response, description)
    status_code = response.status
    if response_type == "json":
        parsed_response = dumps(parsed_response)
    to_add = {
        "response": parsed_response,
        "status_code": status_code
    }
    return to_add


def parse_http_response(response_type, orig_response, description):
    try:
        if response_type == 'text':
            return orig_response.data.decode()
        else:
            return loads(orig_response.data.decode())
    except Exception:
        raise ApiTesterException("Failed to parse http response - {}".format(description))


class CallbackRetry(Retry):
    def __init__(self, *args, **kwargs):
        self._callback = kwargs.pop('callback', None)
        self._response_type = kwargs.pop('response_type', None)
        self._description = kwargs.pop('description', None)
        self._retry_num = kwargs.pop('retry_num', None)
        self._retries_responses = []
        super(CallbackRetry, self).__init__(*args, **kwargs)

    def new(self, **kw):
        # pass along the subclass additional information when creating
        # a new instance.
        kw['callback'] = self._callback
        kw['response_type'] = self._response_type
        kw['description'] = self._description
        kw['retry_num'] = self._retry_num + 1
        return super(CallbackRetry, self).new(**kw)

    def increment(self, method=None, url=None, response=None, error=None,
                  _pool=None, _stacktrace=None):
        try:
            last_retry_response_description = self._callback(response,
                                                             self._response_type,
                                                             self._description)
            key = "retry_response_and_status_code_{}".format(self._retry_num)

        except Exception as err:
            print('Callback raised an exception, ignoring - {}'.format(err.__doc__))
        return super(CallbackRetry, self).increment(method, url, response, error,
                                                    _pool, _stacktrace)

class InfiNextGraphQLClient:

    def __init__(self, endpoint: str, headers: dict = {}):
        self.endpoint = endpoint
        self.headers = headers

    def __request_body(
        self, query: str, variables: dict = None, operation_name: str = None
    ) -> dict:
        json = {"query": query}

        if variables:
            json["variables"] = variables

        if operation_name:
            json["operationName"] = operation_name

        return json

    def execute(self, query: str, variables: dict = None,
                operation_name: str = None, headers: dict = {}):
        """Make synchronous request to graphQL server.
        same as original class function except no raise_for_status on failure
        and returns the original response' not as json"""
        request_body = self.__request_body(
            query=query, variables=variables, operation_name=operation_name
        )

        result = requests.post(
            self.endpoint,
            json=request_body,
            headers={**self.headers, **headers},
        )

        return result

curr_retries_list = []

curr_retry_num = 0


def create_session(response_type, description):
    retry_strategy = CallbackRetry(
        total=vars.REQUESTS_NUMBER_OF_RETRIES,
        status_forcelist=vars.REQUESTS_STATUS_CODES_RETRY,
        method_whitelist=vars.REQUESTS_METHODS_LIST_RETRY,
        backoff_factor=vars.REQUESTS_EXP_SLEEP_RETRY,
        raise_on_status=False,
        callback=add_retry_response_and_status_code,
        response_type=response_type,
        description=description,
        retry_num=1
    )

    request_session = requests.Session()
    adapter = HTTPAdapter(max_retries=retry_strategy)
    request_session.mount("https://", adapter)
    request_session.mount("http://", adapter)
    return request_session


def add_retry_response_and_status_code(response, response_type, description):
    """
    This function is called upon each retry and appends the last response and status code
    to the appropriate key in the log
    :param response: The last response
    :param response_type: The parsing type of the last response (json or test)
    :param description: A short description of the last failed request
    :return A dictionary representing the last retry response
    """
    parsed_response = parse_http_response(response_type, response, description)
    status_code = response.status
    if response_type == "json":
        parsed_response = dumps(parsed_response)
    to_add = {
        "response": parsed_response,
        "status_code": status_code
    }
    return to_add


def parse_http_response(response_type, orig_response, description):
    try:
        if response_type == 'text':
            return orig_response.data.decode()
        else:
            return loads(orig_response.data.decode())
    except Exception:
        raise ApiTesterException("Failed to parse http response - {}".format(description))


class CallbackRetry(Retry):
    def __init__(self, *args, **kwargs):
        self._callback = kwargs.pop('callback', None)
        self._response_type = kwargs.pop('response_type', None)
        self._description = kwargs.pop('description', None)
        self._retry_num = kwargs.pop('retry_num', None)
        self._retries_responses = []
        super(CallbackRetry, self).__init__(*args, **kwargs)

    def new(self, **kw):
        # pass along the subclass additional information when creating
        # a new instance.
        kw['callback'] = self._callback
        kw['response_type'] = self._response_type
        kw['description'] = self._description
        kw['retry_num'] = self._retry_num + 1
        return super(CallbackRetry, self).new(**kw)

    def increment(self, method=None, url=None, response=None, error=None,
                  _pool=None, _stacktrace=None):
        try:
            last_retry_response_description = self._callback(response,
                                                             self._response_type,
                                                             self._description)
            key = "retry_response_and_status_code_{}".format(self._retry_num)

        except Exception as err:
            print('Callback raised an exception, ignoring - {}'.format(err.__doc__))
        return super(CallbackRetry, self).increment(method, url, response, error,
                                                    _pool, _stacktrace)


class ApiTesterException(Exception):

    def __init__(self, message=""):
        self.message = message

    def __str__(self):
        return f"{self.message}"
