# Copyright © Check Point Software Technologies Ltd.
# Management API Example Tool - 1.0.0
# Terms & Conditions: https://www.checkpoint.com/about-us/cloud-terms/
# This code example can be copied and reused

from mgmt_api_helper_functions import *


def cloudInfra_connect():
    """
    Initializes the headers for all test api requests by requesting a token
    for the given clientId and secretKey.
    """
    if vars.CLIENT_ID == "" or vars.SECRET_KEY == "":
        print("API keys are not configured")
        exit()
    auth_response = perform_request(vars.AUTH_PATH, 'post', vars.auth_request_body, 'json',
                                    description='Initializing headers with token',
                                    add_body=False)
    token = auth_response['data']['token']
    vars.all_requests_headers["Authorization"] = "Bearer {}".format(token)

    print('Initializing headers with token')


def create_generic_asset(asset_input):
    """
    Executes a "create generic asset" mutation with graphql-client
    :param asset_input: the asset input
    :return: The new asset id
    """
    asset_variables = {
        "assetInput": asset_input
    }

    asset_res = perform_infinity_request(query_or_mutation=CREATE_GENERIC_ASSET_MUTATION,
                                    version=1,
                                    variables=asset_variables,
                                    description="Creating Generic Asset")
    asset_id = asset_res['data'][CREATE_GENERIC_ASSET_NAME]['id']
    print("----Creating generic Asset---")
    return asset_id


def update_generic_asset(assetInput, id):
    """
    Executes a "update generic asset" mutation with graphql-client
    :param assetInput: the asset input
    :param id: The id of the asset to update
    :return: Server response
    """
    asset_variables = {
        "assetInput": assetInput,
        "id": id
    }

    response = perform_infinity_request(query_or_mutation=UPDATE_GENERIC_ASSET_MUTATION,
                                    version=1,
                                    variables=asset_variables,
                                    description="Updating Asset")

    print("----Updating generic Asset----")
    return response


def create_web_application_asset(asset_input):
    """
    Executes a "create Web Application asset" mutation with graphql-client
    :param asset_input: the asset input
    :return: The new asset id
    """
    asset_variables = {
        "assetInput": asset_input
    }

    asset_res = perform_infinity_request(query_or_mutation=CREATE_WEB_APPLICATION_ASSET_MUTATION,
                                    version=1,
                                    variables=asset_variables,
                                    description="Creating Asset")
    asset_id = asset_res['data'][CREATE_WEB_APPLICATION_ASSET_NAME]['id']

    print("Creating Web Application Asset", asset_res)
    return asset_id

def create_web_api_asset(asset_input):
    """
    Executes a "create Web API asset" mutation with graphql-client
    :param asset_input: the asset input
    :return: The new asset id
    """

    asset_variables = {
        "assetInput": asset_input
    }

    asset_res = perform_infinity_request(query_or_mutation=CREATE_WEB_API_ASSET_MUTATION,
                                    version=1,
                                    variables=asset_variables,
                                    description="Creating Asset")
    asset_id = asset_res['data'][CREATE_WEB_API_ASSET_NAME]['id']

    print("Creating Web API Asset", asset_res)
    return asset_id

def updateWebApplicationSourceIdentifierValues(id):
    """
    Executes a "update Web Application asset" mutation with graphql-client
    :param id: The id of the asset to update
    :return: Server response
    """
    asset_variables = {
        "addIdentifierValue": ["bubu", "gaga"],
        "id": id
    }

    response = perform_infinity_request(query_or_mutation=UPDATE_SOURCE_IDENTIFIERS_VALUES_MUTATION,
                                    version=1,
                                    variables=asset_variables,
                                    description="Updating Source Identifiers")

    print("Updating Source Identifiers", response)
    return response


def get_asset(id):
    """
    Executes a "get asset" query with graphql-client
    :param id: The id of the asset to get
    :return: Server response
    """
    asset_variables = {
        "id": id
    }

    response = perform_infinity_request(query_or_mutation=GET_ASSET_QUERY,
                                   version=1,
                                   variables=asset_variables,
                                   description="get Asset")

    print("Getting Asset by Id", response)
    return response

def get_assets(matchSearch):
    """
    Executes a "get assets" query with graphql-client
    :param matchSearch: string to match in search
    :return: Server response
    """
    asset_variables = {
        "matchSearch": matchSearch
    }

    response = perform_infinity_request(query_or_mutation=GET_ASSETS_QUERY,
                                   version=1,
                                   variables=asset_variables,
                                   description="get Assets")

    print(" Getting Assets", response)
    return response

def delete_asset(asset_id):
    """
    Executes a "delete asset" mutation with graphql-client
    :param asset_id: The id of the asset to be deleted
    """
    delete_asset_variables = {
        "id": asset_id
    }
    res = perform_infinity_request(query_or_mutation=DELETE_ASSET_MUTATION,
                        version=1,
                        variables=delete_asset_variables,
                        description="Deleting Asset")
    print("Deleting Asset", res, "\n")

def create_exception_behavior(behavior_input):
    """
    Executes a "create exception behavior" mutation with graphql-client
    :param behavior_input: The behavior input
    :return: The new behavior id
    """

    behavior_variables = {
        "behaviorInput": behavior_input
    }

    behavior_res = perform_infinity_request(query_or_mutation=CREATE_BEHAVIOR_MUTATION,
                                    version=1,
                                    variables=behavior_variables,
                                    description="Creating Exception behavior")
    behavior_id = behavior_res['data'][CREATE_BEHAVIOR_MUTATION_NAME]['id']
    print("Creating exception behavior", behavior_res)
    return behavior_id

def create_trusted_source_behavior(behavior_input):
    """
    Executes a "create trusted source behavior" mutation with graphql-client
    :param behavior_input: the behavior input
    :return: The new behavior id
    """

    behavior_variables = {
        "behaviorInput": behavior_input
    }

    behavior_res = perform_infinity_request(query_or_mutation=CREATE_TRUSTED_SOURCE_BEHAVIOR_MUTATION,
                                    version=1,
                                    variables=behavior_variables,
                                    description="Creating Trusted source behavior")
    behavior_id = behavior_res['data'][CREATE_TRUSTED_SOURCE_BEHAVIOR_MUTATION_NAME]['id']
    print("Creating Trusted Source behavior", behavior_res, "\n")
    return behavior_id


def update_exception_behavior(behavior_input, id):
    """
    Executes a "update exception behavior" mutation with graphql-client
    :param behavior_input: the behavior input
    :param id: The id of the behavior to update
    :return: Server response
    """
    behavior_variables = {
        "behaviorInput": behavior_input,
        "id": id
    }

    response = perform_infinity_request(query_or_mutation=UPDATE_EXCEPTION_BEHAVIOR_MUTATION,
                                    version=1,
                                    variables=behavior_variables,
                                    description="Updating exception Behavior")

    print("Updating exception behavior", response)
    return response


def get_behavior(id):
    """
    Executes a "get behavior" mutation with graphql-client
    :param id: The id of the behavior to get
    :return: Server response
    """
    behavior_variables = {
        "id": id
    }

    response = perform_infinity_request(query_or_mutation=GET_BEHAVIOR_QUERY,
                                   version=1,
                                   variables=behavior_variables,
                                   description="get behavior")

    print("Getting behavior by Id", response)
    return response

def get_behaviors(matchSearch):
    """
    Executes a "get behaviors" mutation with graphql-client
    :param matchSearch: string to match in search
    :return: Server response
    """
    behavior_variables = {
        "matchSearch": matchSearch
    }

    response = perform_infinity_request(query_or_mutation=GET_BEHAVIORS_QUERY,
                                   version=1,
                                   variables=behavior_variables,
                                   description="get behaviors")

    print("Getting behaviors", response)
    return response

def delete_behavior(behavior_id):
    """
    Executes a "delete behavior" mutation with graphql-client
    :param behavior_id: The id of the behavior to be deleted
    """
    delete_behavior_variables = {
        "id": behavior_id
    }
    res = perform_infinity_request(query_or_mutation=DELETE_BEHAVIOR_MUTATION,
                        version=1,
                        variables=delete_behavior_variables,
                        description="Deleting Behavior")
    print("Deleting Behavior: ", behavior_id, res, "\n")


def create_web_application_practice(modes, practice_input):
    """
    Executes a "create web application practice" mutation with graphql-client
    :param asset_id: The id of the asset to associate the practice with
    :return: The new practice id
    """
    practice_variables = {
        "modes": modes,
        "practiceInput": practice_input
    }
    practice_res = perform_infinity_request(query_or_mutation=CREATE_WEB_APPLICATION_PRACTICE_MUTATION,
                                       variables=practice_variables,
                                       description="Creating Practice")
    practice_id = practice_res['data'][CREATE_WEB_APPLICATION_PRACTICE_MUTATION_NAME]['id']
    print("Creating Web Application Practice")
    return practice_id


def create_web_api_practice(modes, practice_input):
    """
    Executes a "create web api practice" mutation with graphql-client
    :param modes: sub practices modes
    :param practice_input: the practice input
    :return: The new practice id
    """
    practice_variables = {
        "modes": modes,
        "practiceInput": practice_input
    }
    practice_res = perform_infinity_request(query_or_mutation=CREATE_WEB_API_PRACTICE_MUTATION,
                                       variables=practice_variables,
                                       description="Creating Practice")
    practice_id = practice_res['data'][CREATE_WEB_API_PRACTICE_MUTATION_NAME]['id']
    print("Creating Web API Practice", practice_res, "\n")
    return practice_id

def update_web_application_practice(practiceInput, id):
    """
    Executes a "update web application practice" mutation with graphql-client
    :param practiceInput: the practice input
    :param id: The id of the practice to update
    :return: Server response
    """
    practice_variables = {
        "practiceInput": practiceInput,
        "id": id
    }

    response = perform_infinity_request(query_or_mutation=UPDATE_WEB_APPLICATION_PRACTICE_MUTATION,
                                    version=1,
                                    variables=practice_variables,
                                    description="Updating practice")

    print("Updating webApplication practice", response)
    return response


def get_practice(id):
    """
    Executes a "get practice" query with graphql-client
    :param id: The id of the practice to get
    :return: Server response
    """
    practice_variables = {
        "id": id
    }

    response = perform_infinity_request(query_or_mutation=GET_PRACTICE_QUERY,
                                   version=1,
                                   variables=practice_variables,
                                   description="get practice")

    print("Getting practice by Id", response)
    return response

def get_practices(matchSearch):
    """
    Executes a "get practices" query with graphql-client
    :param matchSearch: string to match in search
    :return: Server response
    """
    practice_variables = {
        "matchSearch": matchSearch
    }

    response = perform_infinity_request(query_or_mutation=GET_PRACTICES_QUERY,
                                   version=1,
                                   variables=practice_variables,
                                   description="get practices")

    print("Getting practices", response)
    return response


def delete_practice(practice_id):
    """
    Executes a "delete practice" mutation with graphql-client
    :param practice_id: The id of the practice to be deleted
    """
    delete_practice_variables = {
        "id": practice_id
    }
    result = perform_infinity_request(query_or_mutation=DELETE_PRACTICE_MUTATION,
                        version=1,
                        variables=delete_practice_variables,
                        description="Deleting Practice")
    print("Deleting Practice: ", practice_id, result, "\n")

def create_log_trigger(trigger_input):
    """
    Executes a "create log trigger" mutation with graphql-client
    :param trigger_input: the trigger input
    :return: The new trigger id
    """
    trigger_variables = {
        "triggerInput": trigger_input
    }

    trigger_res = perform_infinity_request(query_or_mutation=CREATE_LOG_TRIGGER_MUTATION,
                                    version=1,
                                    variables=trigger_variables,
                                    description="Creating Log trigger")
    trigger_id = trigger_res['data'][CREATE_LOG_TRIGGER_NAME]['id']
    print("Creating generic trigger", trigger_res, "\n")
    return trigger_id


def update_log_trigger(trigger_input, id):
    """
    Executes a "update log trigger" mutation with graphql-client
    :param trigger_input: the trigger input
    :param id: The id of the trigger to update
    :return: Server response
    """
    trigger_variables = {
        "triggerInput": trigger_input,
        "id": id
    }

    response = perform_infinity_request(query_or_mutation=UPDATE_LOG_TRIGGER_MUTATION,
                                    version=1,
                                    variables=trigger_variables,
                                    description="Updating trigger")

    print("Updating log trigger", response)
    return response


def get_trigger(id):
    """
    Executes a "get trigger" query with graphql-client
    :param id: The id of the trigger to get
    :return: Server response
    """
    trigger_variables = {
        "id": id
    }

    response = perform_infinity_request(query_or_mutation=GET_TRIGGER_QUERY,
                                   version=1,
                                   variables=trigger_variables,
                                   description="get trigger")

    print("Getting trigger by Id", response)
    return response

def get_triggers(matchSearch):
    """
    Executes a "get triggers" query with graphql-client
    :param matchSearch: string to match in search
    :return: Server response
    """
    trigger_variables = {
        "matchSearch": matchSearch
    }

    response = perform_infinity_request(query_or_mutation=GET_TRIGGERS_QUERY,
                                   version=1,
                                   variables=trigger_variables,
                                   description="get triggers")

    print("Getting triggers", response)
    return response

def delete_trigger(trigger_id):
    """
    Executes a "delete trigger" mutation with graphql-client
    :param trigger_id: The id of the zone to be deleted
    """
    delete_trigger_variables = {
        "id": trigger_id
    }
    res = perform_infinity_request(query_or_mutation=DELETE_TRIGGER_MUTATION,
                        version=1,
                        variables=delete_trigger_variables,
                        description="Deleting Trigger")
    print("Deleting Trigger", res, "\n")


def create_generic_zone(zone_input):
    """
    Executes a "create generic zone" mutation with graphql-client
    :param zone_input: the zone input
    :return: The new zone id
    """
    zone_variables = {
        "zoneInput": zone_input
    }

    zone_res = perform_infinity_request(query_or_mutation=CREATE_GENERIC_ZONE_MUTATION,
                                    version=1,
                                    variables=zone_variables,
                                    description="Creating Generic zone")
    zone_id = zone_res['data'][CREATE_GENERIC_ZONE_NAME]['id']
    print("----Creating generic zone---")
    return zone_id


def update_generic_zone(zone_input, id):
    """
    Executes a "update generic zone" mutation with graphql-client
    :param zone_input: the zone input
    :param id: The id of the zone to update
    :return: Server response
    """
    zone_variables = {
        "zoneUpdateInput": zone_input,
        "id": id
    }

    response = perform_infinity_request(query_or_mutation=UPDATE_GENERIC_ZONE_MUTATION,
                                    version=1,
                                    variables=zone_variables,
                                    description="Updating zone")

    print("----Updating generic zone----")
    return response


def get_zone(id):
    """
    Executes a "get zone" query with graphql-client
    :param id: The id of the zone to get
    :return: Server response
    """
    zone_variables = {
        "id": id
    }

    response = perform_infinity_request(query_or_mutation=GET_ZONE_QUERY,
                                   version=1,
                                   variables=zone_variables,
                                   description="get zone")

    print("----Getting zone by Id----")
    return response

def get_zones(matchSearch):
    """
    Executes a "get zones" mutation with graphql-client
    :param matchSearch: string to match in search
    :return: Server response
    """
    zone_variables = {
        "matchSearch": matchSearch
    }

    response = perform_infinity_request(query_or_mutation=GET_ZONES_QUERY,
                                   version=1,
                                   variables=zone_variables,
                                   description="get zones")

    print("----Getting zones----")
    return response

def delete_zone(zone_id):
    """
    Executes a "delete zone" mutation with graphql-client
    :param zone_id: The id of the zone to be deleted
    """
    delete_zone_variables = {
        "id": zone_id
    }
    perform_infinity_request(query_or_mutation=DELETE_ZONE_MUTATION,
                        version=1,
                        variables=delete_zone_variables,
                        description="Deleting Zone")
    print("Deleting Zone")

def create_reusable_token_profile(profile_input):
    """
    Executes a "create reusable token profile" mutation with graphql-client
    :param profile_input: the profile input
    :return: The new profile id
    """
    profile_variables = {
        "profileInput": profile_input
    }

    profile_res = perform_infinity_request(query_or_mutation=CREATE_REUSABLE_TOKEN_PROFILE_MUTATION,
                                    version=1,
                                    variables=profile_variables,
                                    description="Creating Reusable profile")
    profile_id = profile_res['data'][CREATE_REUSABLE_TOKEN_PROFILE_MUTATION_NAME]['id']
    print("Creating reusable profile", profile_res, "\n")
    return profile_id


def update_reusable_token_profile(profile_input, id):
    """
    Executes a "update reusable token profile" mutation with graphql-client
    :param profile_input: the profile input
    :param id: The id of the profile to update
    :return: Server response
    """
    profile_variables = {
        "profileInput": profile_input,
        "id": id
    }

    response = perform_infinity_request(query_or_mutation=UPDATE_REUSABLE_TOKEN_PROFILE_MUTATION,
                                    version=1,
                                    variables=profile_variables,
                                    description="Updating profile")

    print("Updating reusable profile", response)
    return response


def get_profile(id):
    """
    Executes a "get profile" query with graphql-client
    :param id: The id of the profile to get
    :return: Server response
    """
    profile_variables = {
        "id": id
    }

    response = perform_infinity_request(query_or_mutation=GET_PROFILE_QUERY,
                                   version=1,
                                   variables=profile_variables,
                                   description="get profile")

    print("Getting profile by Id", response)
    return response

def get_profiles(matchSearch):
    """
    Executes a "get profiles" query with graphql-client
    :param matchSearch: string to match in search
    :return: Server response
    """
    profile_variables = {
        "matchSearch": matchSearch
    }

    response = perform_infinity_request(query_or_mutation=GET_PROFILES_QUERY,
                                   version=1,
                                   variables=profile_variables,
                                   description="get profiles")

    print("Getting profiles", response)
    return response

def delete_profile(profile_id):
    """
    Executes a "delete profile" mutation with graphql-client
    :param profile_id: The id of the profile to be deleted
    """
    delete_profile_variables = {
        "id": profile_id
    }
    res = perform_infinity_request(query_or_mutation=DELETE_PROFILE_MUTATION,
                        version=1,
                        variables=delete_profile_variables,
                        description="Deleting Profile")
    print("Deleting Profile: ", profile_id, res, "\n")
