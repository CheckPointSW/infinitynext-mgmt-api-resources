# Copyright © Check Point Software Technologies Ltd.
# Management API Example Tool - 1.0.0
# Terms & Conditions: https://www.checkpoint.com/about-us/cloud-terms/
# This code example can be copied and reused

from mgmt_api import cloudInfra_connect
import traceback
import sched
import time
import mgmt_api
scheduler = sched.scheduler(time.time, time.sleep)
from mgmt_api_helper_functions import *

def main():
    can_discard_changes = True
    discard_objects = True
    try:

        print("Starting \n")

        cloudInfra_connect()

        print("Creating shared components\n")

        trigger_name = "{} {}".format("log trigger", generate_random_hex())
        trigger_id = mgmt_api.create_log_trigger({
            "name": trigger_name
        })

        behavior_name = "{} {}".format("behavior", generate_random_hex())
        behavior_id = mgmt_api.create_trusted_source_behavior({
            "name": behavior_name,
            "visibility": "Shared",
            "numOfSources": 3,
            "sourcesIdentifiers": ["192.168.10.1", "192.168.10.2", "192.168.10.3", "192.168.10.4", "192.168.10.5"]
        })

        profile_name = "{} {}".format('Profile', generate_random_hex())
        profile_id = mgmt_api.create_reusable_token_profile({
            "name": profile_name,
            "subType": "Aws",
            "onlyDefinedAssets": True
        })
        print("Creating Web API Asset and components\n")

        modes = [
            {
                "mode": "AccordingToPractice",
                "subPractice": "IPS"
            },
            {
                "mode": "Prevent"
            },
            {
                "mode": "AccordingToPractice",
                "subPractice": "SchemaValidation"
            },
            {
                "mode": "AccordingToPractice",
                "subPractice": "APIAttacks"
            }
        ]
        practice_name = "{} {}".format("ACME Web API Practice", generate_full_random_hex())
        web_api_practice_id = mgmt_api.create_web_api_practice(modes, {
            "name": practice_name,
            "visibility": "Shared"
        })

        web_api_practice_obj = {
            "practiceId": web_api_practice_id,
            "triggers": [trigger_id]
        }

        web_api_asset_name = "{} {}".format("Web API", generate_random_hex())
        web_api_asset_url = "https://api.acme-{}.checkpoint.com".format(generate_full_random_hex())
        asset_input = {
            "name": web_api_asset_name,
            "practices": [web_api_practice_obj],
            "behaviors": [
                behavior_id
            ],
            "profiles": [
                profile_id
            ],
            "URLs": [
                web_api_asset_url
            ],
            "upstreamURL": "http://1.2.3.4",
            "sourceIdentifiers": [{"sourceIdentifier": "HeaderKey", "values": ["users"]}]
        }
        web_api_asset_id = mgmt_api.create_web_api_asset(asset_input)

        print("Creating Web Application Asset and components\n")

        web_application_practice_name = "{} {}".format(PRACTICE_BASE_NAME, generate_full_random_hex())
        web_application_practice_id = mgmt_api.create_web_application_practice(modes, {
            "name": web_application_practice_name,
            "visibility": "Shared"
        })
        web_application_practice_obj = {
            "practiceId": web_application_practice_id,
            "triggers": [trigger_id]
        }

        web_application_asset_name = "{} {}".format("Web Application", generate_random_hex())
        web_application_asset_url = "https://api.acme-{}.checkpoint.com".format(generate_full_random_hex())
        asset_input = {
            "name": web_application_asset_name,
            "practices": [web_application_practice_obj],
            "behaviors":[
                behavior_id
            ],
            "profiles": [
                profile_id
            ],
            "URLs": [
                web_application_asset_url
            ],
            "upstreamURL": "http://1.1.1.1"
        }
        web_application_asset_id = mgmt_api.create_web_application_asset(asset_input)

        response = publish_changes()

        print("publish changes", response)

        # after publish we cannot discard the created objects
        can_discard_changes = False

        task_id = enforce_policy()

        print("enforce policy: got response task", task_id)

        wait_for_enforce_policy_status(task_id)

    except Exception as err:
        if isinstance(err, ApiTesterException):
            if can_discard_changes:
                discard_changes(err.message)
                discard_objects = False
            else:
                print(err.message)
        else:  # this is a python exception
            print("Failed with python exception - {}".format(traceback.format_exc()))
    finally:
        if discard_objects:
            print("")
            # print("Starting Deletion")
            # mgmt_api.delete_asset(asset_id=web_api_asset_id)
            # mgmt_api.delete_asset(asset_id=web_application_asset_id)
            # mgmt_api.delete_practice(practice_id=web_api_practice_id)
            # mgmt_api.delete_practice(practice_id=web_application_practice_id)
            # mgmt_api.delete_trigger(trigger_id=trigger_id)
            # mgmt_api.delete_profile(profile_id=profile_id)
            # mgmt_api.delete_behavior(behavior_id=behavior_id)
            # print("Finished Deletion")
        vars.clean_last_token_from_headers()


if __name__ == "__main__":
    main()
