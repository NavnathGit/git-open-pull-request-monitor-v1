Worker Job to monitor and alert if open pull requests are above defined threshold. For example, if there are open pull request count older than three days or more waiting for approval alert will be sent on Slack channel.

Step 1: 
Download source code from above git-hub repository- down load master branch.
If you don’t want to download source code, you can download readymade image from my docker hub account.

https://hub.docker.com/repository/docker/navanthd/git-open-pull-request-monitor

Image: navanthd/git-open-pull-request-monitor:v1


Step 2:  Skip this step if you download the in-built image 
Open Terminal on your machine, navigate to the folder where you have kept source code from above repository 

docker build -t git-open-pull-request-monitor-slim-v1 .

Step 3: 

	There is total three environment variable are required to run this container.

ALERT_THRESHOLD_DAYS – request older than # of days
GIT_API_URL: git api URL for which you want to set monitor
SLACK_WEBHOOK_URL: Slack channel webhook URL

You can set these variables locally and pass it into docker run command. Example shown below.

export ALERT_THRESHOLD_DAYS =1

export GIT_API_URL=https://api.github.com/repos/NavnathGit/DSA-JS/pulls?state=open

export SLACK_WEBHOOK_URL=https://hooks.slack.com/services/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

once you set ENV variable run the below command. Downside of this is this will be one time run, it will not run-on regular interval.

docker run --env GIT_API_URL --env SLACK_WEBHOOK_URL --env ALERT_THRESHOLD_DAYS --name=pull-request-monitor_container-v1 git-open-pull-request-monitor-slim-v1


Other option could be pass environment variables using Config Map and Secret. Please modify the config map and secret yaml file as per your need.

kubectl apply -f worker-config-map.yaml

you need to create new secret using terminal for your Slack-webhook URL.

kubectl apply -f worker-secret.yaml

Finally create Cron-Job which will run on regular interval, I have set it as 1 minute interval for testing. Also, for testing purpose I have set threshold limit as 1 Day old open pull request as I don’t have any open pull request older than a Day.

kubectl apply -f worker-cron-job.yaml

On successful Run:  Message will be posted on Slack channel.  

![image](https://user-images.githubusercontent.com/87501404/152604267-3ff5d482-8c85-4ade-a439-44b1df7f1353.png)

Security: 

Slack webhook URL is stored in either ENV variable or Secret variable based on how we decide to run the job. Web hook URL is encrypted in Kubernetes secret.
