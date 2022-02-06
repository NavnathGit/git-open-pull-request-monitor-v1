import json
import sys
import os
import requests
from datetime import datetime


def get_pull_request_data(api_url, alert_threshold_days):

    pull_request_data = []
    older_than_threshold_days = 'NO'
    res = requests.get(api_url)
    res_data = res.json()
    if (len(res_data)) != 0:
        for item in res_data:
            pull_request_datails = {}
            created_date_time = item['created_at']
            pull_request_create_date = datetime.fromisoformat(datetime.strptime(
                created_date_time, "%Y-%m-%dT%H:%M:%SZ").isoformat())

            todays_date = datetime.fromisoformat(
                datetime.now().replace(microsecond=0).isoformat())

            if (abs(todays_date - pull_request_create_date).days) >= int(alert_threshold_days):
                older_than_threshold_days = 'YES'

            pull_request_datails['html_url'] = item['html_url']
            pull_request_datails['older_than_threshold'] = older_than_threshold_days
            pull_request_data.append(pull_request_datails)

        return pull_request_data


def contains_old_pull_request(pull_req_data):
    for index in range(len(pull_req_data)):
        for key in pull_req_data[index]:
            if pull_req_data[index][key] == 'YES':
                return True
    return False


def get_pull_request_links(pull_req_data):
    pull_request_links = []
    for index in range(len(pull_req_data)):
        for key in pull_req_data[index]:
            if key == 'html_url':
                pull_request_links.append(pull_req_data[index][key])
    return pull_request_links


def post_message_on_slack(slack_webhook_url, pull_req_data):
    pull_request_links = (get_pull_request_links(pull_req_data))
    links = ''
    for x in range(len(pull_request_links)):
        links += (str(pull_request_links[x]) + "\n")
    message = (f"Need Attention: Please approve open pull requests {links}")
    title = (f"New Incoming Message :zap:")
    slack_data = {
        "username": "NotificationBot",
        "icon_emoji": ":satellite:",
        # "channel" : "#git-pull-request-approval-queue",
        "attachments": [
            {
                    "color": "#9733EE",
                    "fields": [
                        {
                            "title": title,
                            "value": message,
                            "short": "false",
                        }
                    ]
            }
        ]
    }
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json",
               'Content-Length': byte_length}
    response = requests.post(
        slack_webhook_url, data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)


if __name__ == '__main__':

    git_api_url = os.environ.get('GIT_API_URL')
    slack_webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
    alert_threshold_days = os.environ.get('ALERT_THRESHOLD_DAYS')

    if git_api_url and slack_webhook_url and alert_threshold_days:
        pull_req_data = get_pull_request_data(
            git_api_url, alert_threshold_days)
        if pull_req_data:
            old_pull_request = contains_old_pull_request(pull_req_data)
            if old_pull_request:
                post_message_on_slack(slack_webhook_url, pull_req_data)
            else:
                print('No pending pull request found older than threshold')
        else:
            print(
                'Open pull request threshold has not reached or no open pull requests pending for approval')
    else:
        print('Please provide all required parameters')
