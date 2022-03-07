# Copyright © Check Point Software Technologies Ltd.
# Management API Example Tool - 1.0.0
# Terms & Conditions: https://www.checkpoint.com/about-us/cloud-terms/
# This code example can be copied and reused

import os
import json
from ast import literal_eval


# prod
CLIENT_ID = ""
SECRET_KEY = ""
region = "US"# US or EU

CLOUD_INFRA_HOST = "https://cloudinfra-gw-us.portal.checkpoint.com" if region == 'US' else "https://cloudinfra-gw.portal.checkpoint.com"
APP_PATH = "/app/i2"

AUTH_PATH = "/auth/external"



REQUESTS_NUMBER_OF_RETRIES = 0
REQUESTS_STATUS_CODES_RETRY = [429, 500, 502, 503, 504, 400, 401, 403, 404]
REQUESTS_METHODS_LIST_RETRY = ['POST', 'DELETE', 'GET', 'PUT', 'OPTIONS', 'HEAD', 'TRACE']
REQUESTS_EXP_SLEEP_RETRY = 2
SCHEDULER_WAIT_BEFORE_FIRST_RUN_SECONDS = 10

# content type
CONTENT_TYPE = "application/json"

auth_request_body = {
    "clientId": CLIENT_ID,
    "accessKey": SECRET_KEY
}

all_requests_headers = {
    "user-agent": "Infinity Next Sanity Script",
    "Content-Type": CONTENT_TYPE,
    "Authorization": ""
}

GRAPHQL_CLIENT_ENDPOINT = "{}{}/graphql".format(CLOUD_INFRA_HOST, APP_PATH)
GRAPHQL_CLIENT_ENDPOINT_V1 = "{}{}/graphql/v1".format(CLOUD_INFRA_HOST, APP_PATH)
CHECK_ENFORCE_STATUS_RETRIES = 6
SLEEP_AFTER_CHECK_ENFORCE_STATUS = 10


# ----------PROFILES mutations----------

CREATE_DOCKER_PROFILE_MUTATION = """mutation newDockerProfile($profileInput: DockerProfileInput){
                           newDockerProfile(profileInput: $profileInput){
                             id
                             name
                         }
                         }"""

CREATE_DOCKER_PROFILE_MUTATION_NAME = "newDockerProfile"

UPDATE_DOCKER_PROFILE_MUTATION = """mutation updateDockerProfile($profileInput: DockerProfileInput!, $id: ID!) {
                         updateDockerProfile(profileInput: $profileInput, id: $id) 
                       }"""

DELETE_PROFILE_MUTATION = """mutation deleteProfile($id: ID!){
                           deleteProfile(id: $id)
                            }"""

# ----------PROFILES queries----------

GET_PROFILE_QUERY = """query getProfile($id: ID!){
                        getProfile(id: $id){
                          id
                          name
                         }
                    }"""

GET_AGENTS_QUERY = """query getAgents(){
                        getAgents(){
                          id
                          name
                         }
                    }"""

GET_PROFILES_QUERY = """query getProfiles($matchSearch: String){
                        getProfiles(matchSearch: $matchSearch){
                          id
                          name
                        }
                     }"""

# ----------ASSETS mutations----------

CREATE_WEB_APPLICATION_ASSET_MUTATION = """mutation newWebApplicationAsset($assetInput: WebApplicationAssetInput!) {
                         newWebApplicationAsset(assetInput: $assetInput) {
                           id
                           name
                       }
                       }"""

CREATE_WEB_API_ASSET_MUTATION = """mutation newWebAPIAsset($assetInput: WebAPIAssetInput!) {
                         newWebAPIAsset(assetInput: $assetInput) {
                           id
                           name
                       }
                       }"""

CREATE_GENERIC_ASSET_MUTATION = """mutation newGenericAsset($assetInput: GenericAssetInput!) {
                         newGenericAsset(assetInput: $assetInput) {
                           id
                           name
                       }
                       }"""

UPDATE_GENERIC_ASSET_MUTATION = """mutation updateGenericAsset($assetInput: GenericAssetUpdateInput!, $id: ID!) {
                         updateGenericAsset(assetInput: $assetInput, id: $id) 
                       }"""

UPDATE_SOURCE_IDENTIFIERS_VALUES_MUTATION = """mutation updateWebApplicationSourceIdentifierValues($addIdentifierValue: [String], $id: ID!) {
                         updateWebApplicationSourceIdentifierValues(addIdentifierValue: $addIdentifierValue, id: $id) 
                       }"""

DELETE_ASSET_MUTATION = """mutation deleteAsset($id: String!){
                         deleteAsset(id: $id)
                       }"""

CREATE_WEB_APPLICATION_ASSET_NAME = "newWebApplicationAsset"

CREATE_WEB_API_ASSET_NAME = "newWebAPIAsset"

CREATE_GENERIC_ASSET_NAME = "newGenericAsset"
# ----------ASSETS queries----------

GET_ASSET_QUERY = """query getAsset($id: String!, $userDefined: Boolean){
                        getAsset(id: $id, userDefined: $userDefined){
                          id
                          name
                         }
                  }"""

GET_ASSETS_QUERY = """query getAssets($matchSearch: String, $userDefined: Boolean, $sortBy: String){
                        getAssets(matchSearch: $matchSearch, userDefined: $userDefined, sortBy: $sortBy){
                         assets{
                          id
                          name
                         }
                        }
                  }"""

# ----------ZONES mutations----------
CREATE_GENERIC_ZONE_MUTATION = """mutation newGenericZone($zoneInput: GenericZoneInput!) {
                                    newGenericZone(zoneInput: $zoneInput) {
                                       id
                                       name
                                    }
                               }"""

CREATE_GENERIC_ZONE_NAME = "newGenericZone"

UPDATE_GENERIC_ZONE_MUTATION = """mutation updateGenericZone($zoneUpdateInput: GenericZoneUpdateInput!, $id: ID!) {
                         updateGenericZone(zoneUpdateInput: $zoneUpdateInput, id: $id) 
                       }"""

DELETE_ZONE_MUTATION = """mutation deleteZone($id: ID!){
                           deleteZone(id: $id)
                         }"""

# ----------ZONES queries----------

GET_ZONE_QUERY = """query getZone($id: ID!){
                        getZone(id: $id){ id }
                }"""

GET_ZONES_QUERY = """query getZones($matchSearch: String, $userDefined: Boolean, $sortBy: String){
                        getZones(matchSearch: $matchSearch, userDefined: $userDefined, sortBy: $sortBy){
                         zones{
                          id
                          name
                         }
                        }
                  }"""

# ----------TRIGGERS mutations----------


CREATE_LOG_TRIGGER_MUTATION = """mutation newLogTrigger($triggerInput: LogTriggerInput!) {
                         newLogTrigger(triggerInput: $triggerInput) {
                           id
                           name
                       }
                       }"""

CREATE_LOG_TRIGGER_NAME = "newLogTrigger"

UPDATE_LOG_TRIGGER_MUTATION = """mutation updateLogTrigger($triggerInput: LogTriggerInput!, $id: ID!) {
                         updateLogTrigger(triggerInput: $triggerInput, id: $id) 
                       }"""

DELETE_TRIGGER_MUTATION = """mutation deleteTrigger($id: ID!){
                           deleteTrigger(id: $id)
                            }"""
# ----------TRIGGERS queries----------

GET_TRIGGERS_QUERY = """query getTriggers($matchSearch: String){
                        getTriggers(matchSearch: $matchSearch){ 
                          id 
                          name
                        }
                    }"""

GET_TRIGGER_QUERY = """query getTrigger($id: ID!){
                        getTrigger(id: $id){
                          id
                          name
                         }
                     }"""

# ----------BEHAVIORS mutations----------

CREATE_BEHAVIOR_MUTATION = """mutation newExceptionBehavior($ownerId: ID, $practiceId: ID, $behaviorInput: ExceptionBehaviorInput) {
                         newExceptionBehavior(ownerId: $ownerId, practiceId: $practiceId, behaviorInput: $behaviorInput) {
                           id
                           name
                       }
                       }"""

CREATE_TRUSTED_SOURCE_BEHAVIOR_MUTATION = """mutation newTrustedSourceBehavior($ownerId: ID, $practiceId: ID, $behaviorInput: TrustedSourceBehaviorInput) {
                         newTrustedSourceBehavior(ownerId: $ownerId, practiceId: $practiceId, behaviorInput: $behaviorInput) {
                           id
                           name
                       }
                       }"""

CREATE_BEHAVIOR_MUTATION_NAME = "newExceptionBehavior"
CREATE_TRUSTED_SOURCE_BEHAVIOR_MUTATION_NAME = "newTrustedSourceBehavior"

UPDATE_EXCEPTION_BEHAVIOR_MUTATION = """mutation updateExceptionBehavior($behaviorInput: ExceptionBehaviorUpdateInput!, $id: ID!) {
                         updateExceptionBehavior(behaviorInput: $behaviorInput, id: $id) 
                       }"""

DELETE_BEHAVIOR_MUTATION = """mutation deleteBehavior($id: ID!){
                           deleteBehavior(id: $id)
                         }"""

# ----------BEHAVIORS queries----------

GET_BEHAVIOR_QUERY = """query getTrigger($id: String!){
                        getTrigger(id: $id){ id }"""

GET_BEHAVIOR_QUERY = """query getBehavior($id: ID!){
                        getBehavior(id: $id){
                          id
                          name
                         }
                     }"""

GET_BEHAVIORS_QUERY = """query getBehaviors($matchSearch: String, $includePrivateBehaviors: Boolean, $sortBy: String){
                        getBehaviors(matchSearch: $matchSearch, includePrivateBehaviors: $includePrivateBehaviors, sortBy: $sortBy){
                         id
                         name
                         }
                      }"""


# ----------PRACTICES mutations----------

CREATE_WEB_APPLICATION_PRACTICE_MUTATION = """mutation newWebApplicationPractice($ownerId: ID, $modes: [PracticeModeInput], $practiceInput: WebApplicationPracticeInput){
                            newWebApplicationPractice(ownerId: $ownerId, modes: $modes, practiceInput: $practiceInput){
                              id
                              name
                       }
                       }"""

CREATE_WEB_API_PRACTICE_MUTATION = """mutation newWebAPIPractice($ownerId: ID, $modes: [PracticeModeInput], $practiceInput: WebAPIPracticeInput){
                            newWebAPIPractice(ownerId: $ownerId, modes: $modes, practiceInput: $practiceInput){
                              id
                              name
                       }
                       }"""

UPDATE_WEB_APPLICATION_PRACTICE_MUTATION = """mutation updateWebApplicationPractice($practiceInput: WebApplicationPracticeUpdateInput!, $ownerId : ID,  $id: ID!) {
                         updateWebApplicationPractice(practiceInput: $practiceInput, ownerId: $ownerId, id: $id) 
                       }"""

PRACTICE_BASE_NAME = "WAAP Gem Best Practice"

CREATE_WEB_APPLICATION_PRACTICE_MUTATION_NAME = "newWebApplicationPractice"

CREATE_WEB_API_PRACTICE_MUTATION_NAME = "newWebAPIPractice"

DELETE_PRACTICE_MUTATION = """mutation deletePractice($id: ID!){
                            deletePractice(id: $id)
                          }"""

# ----------PRACTICES queries----------

GET_PRACTICE_QUERY = """query getPractice($id: ID!){
                        getPractice(id: $id){
                          id
                          name
                         }
                    }"""

GET_PRACTICES_QUERY = """query getPractices($matchSearch: String, $includePrivatePractices: Boolean, $practiceType: PracticeType, $sortBy: String){
                        getPractices(matchSearch: $matchSearch, includePrivatePractices: $includePrivatePractices, practiceType: $practiceType, sortBy: $sortBy){ 
                            id
                            name
                         }
                      }"""

# ----------POLICY mutations----------

PUBLISH_MUTATION = """mutation publishChanges{
    publishChanges{
    isValid
    }
    }"""

PUBLISH_MUTATION_NAME = "publishChanges"

ENFORCE_MUTATION = """mutation enforcePolicy{
    enforcePolicy {
    id
    }
    }"""

ENFORCE_MUTATION_NAME = "enforcePolicy"

DISCARD_CHANGES_MUTATION = """mutation discardChanges{
    discardChanges
    }"""

# ----------POLICY queries----------

CHECK_ENFORCE_STATUS_QUERY = """query getTask($id: ID!) {
                                 getTask(id: $id){
                                   id
                                   status
                               }
                               }"""

CHECK_ENFORCE_STATUS_QUERY_NAME = "getTask"

CHECK_ENFORCE_STATUS_RETRIES = 6

SLEEP_AFTER_CHECK_ENFORCE_STATUS = 10





def clean_last_token_from_headers():
    global all_requests_headers
    all_requests_headers["Authorization"] = ""
