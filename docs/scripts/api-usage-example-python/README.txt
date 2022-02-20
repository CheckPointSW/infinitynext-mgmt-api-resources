# Copyright © Check Point Software Technologies Ltd.
# Management API Example Tool - 1.0.0
# Terms & Conditions: https://www.checkpoint.com/about-us/cloud-terms/
# This code example can be copied and reused


requirements:
    urllib3==1.25.3
    requests==2.24.0
    JSON_log_formatter==0.3.0
    python_json_logger==2.0.1

included files:
 vars.py:
    This file contains all kind of variables used in the script.
    The following variables should be configured with your particular attributes:

    From Global Settings Infinity Policy API keys:
        # CLIENT_ID = "123456789012345678901234567895940"
        # SECRET_KEY = "123456789012345678901234567896546"




  main.py:
    This is the main function of the script. To run the script use "python main.py"
    In the end of main, there is an option to delete all objects, currently inside remark.

  main_api.py:
    This file contains all the graphql request functions, e.g. create, update, get and delete functions.

  mgmt_api_helper_functions.py:
    This file contain helper functions that are needed for communication, execution, session creation, exceptions handling, etc..
