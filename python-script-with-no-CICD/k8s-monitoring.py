'''
script for manual checking k8s api for failed pods
'''

import os
import subprocess
import time
import requests

def check_kubectl_availability() -> 0:
    '''Simple function to check if kubectl is correctly in PATH'''
    if (os.system('which kubectl')) != 0:
        print("Kubectl not found, oopsie")
        exit()
    else:
        print("Found kubectl")
        return 0

def get_all_namespaces_as_list() -> list:
    '''
    Get all namespaces in the cluster to be used for other functions
    subprocess.Popen() used here to do the following:
    - run system commands with a mutable STDOUT stream
    - avoid tempfiles and reliance on awk/sed
    '''
    namespace_list = []
    get_namespace = subprocess.Popen(['kubectl', 'get', 'namespaces'], stdout=subprocess.PIPE, universal_newlines=True)
    ns_string = get_namespace.stdout.readlines()
    # Now the ns_string var contains the whole list, first object is headers so don't care about that too much
    ns_string.pop(0)
    for line in ns_string:
        # remove the second and third substring by using split
        line = line.split("  ")[0]
        namespace_list.append(line)
    return namespace_list

def get_all_failed_pods_and_logs_in_namespace(namespace: str) -> dict:
    '''
    Get all pods per namespace to be filtered for failed ones
    Implement data structure using key-value pairs, where the key is the failed pod,
    and the value the logs for the corresponding pod
    '''
    list_of_failed_pods = {}
    # Get stdout from kubectl get pods -n namespace
    all_pods_raw = subprocess.Popen(['kubectl', 'get', 'pods', '-n', namespace], stdout=subprocess.PIPE, universal_newlines=True)
    all_pods = all_pods_raw.stdout.readlines()
    # Find lines with Error in the status field and iterate
    for line in all_pods:
    # Sample for line: ssl-checker-manual-broken-manifest-4-dgczg       Error
        if "Error" in line:
            print(f"Pod failure detected: {line.split(' ')[0]}")
            pod_name = line.split(' ')[0]
            # Get stdout for pod logs
            get_pod_logs = subprocess.Popen(['kubectl', 'logs', '-n', namespace, pod_name], stdout=subprocess.PIPE, universal_newlines=True)
            pod_logs = get_pod_logs.stdout.readlines()
            # Add the logs under the dict's pod_name key
            list_of_failed_pods[pod_name] = pod_logs
    # Sanity print for logging
    print(f"Total number of failed pods found in the {namespace} namespace: {len(list_of_failed_pods)}")
    return list_of_failed_pods

def send_failed_list_to_slack(list_of_failed_pods: list) -> 0:
    '''
    Send the list of failed pods to MM as a template
    The template gets filled with info per failed pod to keep messages short and sweet(ish)
    '''
    mm_header = {
        'Content-Type': 'application/json'
    }
    channel_endpoint = '$URL'
    # # Implement per-pod filler logic
    #print("MM function, using param: " +str(list_of_failed_pods))
    for pod in list_of_failed_pods:
        print("Manual rate limit")
        time.sleep(1)
        pod_logs = str(list_of_failed_pods[pod])
        print("Template for " + pod)
        post_template = {
            'attachments': [
                {
                #"pretext": "Noticed an oopsie :O",
                "color": "#d0342c",
                "author_name": "Kube-notifier script",
                "fields": [
                    {
                        "short": True,
                        "title":"Pod name",
                        "value": f"{pod}"
                    },
                    {
                        "short": False,
                        "title":f"Pod logs for {pod}",
                        "value": "```" + pod_logs + "```"
                    }
                ],
                "text": "Failing pods found in the utility-cluster! :eyes:" ,
                "username": "kube-notifier"
                }
            ]
        }
        send_hook = requests.post(
            url=channel_endpoint, timeout=10, json=post_template, headers=mm_header)
        print("Webhook should be sent")
        print(f"Webhook status: {send_hook.status_code}")
    return 0

'''
Logic section
0) initiate dictionary
1) check kubectl availability
2) get all namespaces
3) get all pods in each namespace
4) check each pod per namespace
5) collect failed pods + their logs
6) create list of pods to communicate
7) check if the list has already been sent
8) loop
'''
# Test adding 5s sleep at the start to let the service acco token mount
print("####Starting up, 5s boot####")
time.sleep(5)
already_sent_pods = {}
# First run, populate dict keys per ns
POPULATE_NAMESPACES = get_all_namespaces_as_list()
for i in POPULATE_NAMESPACES:
    already_sent_pods[i] = ""

# Start a while-true loop to run eternally
while True:
    time.sleep(1)
    KUBECTL = check_kubectl_availability()
    time.sleep(1)
    # If no kubectl, exit
    if KUBECTL != 0:
        print("Kubectl not found! Exiting")
        break
    time.sleep(1)
    ALL_NAMESPACES = get_all_namespaces_as_list()
    time.sleep(1)
    # Loop through all namespaces
    for ns in ALL_NAMESPACES:
        # More logic time: this loop should run almost constantly to get new failed pods.
        # However nobody wants to see the same updates more than once
        # Get failed pods + logs
        FAILED_PODS_AND_LOGS = get_all_failed_pods_and_logs_in_namespace(ns)
        # Check if the last message contains the same stuff as FAILED
        if str(FAILED_PODS_AND_LOGS) in already_sent_pods[ns]:
            print("Message sent already, sleeping.")
            time.sleep(10)
        # If no match and there is something to send, send MM message
        else:
            print(f"Starting  communication for namespace {ns}")
            send_failed_list_to_slack(FAILED_PODS_AND_LOGS)
        # After the message is sent, update the NS-specific key with the value sent to MM
        already_sent_pods[ns] = str(FAILED_PODS_AND_LOGS)
        # Manual rate limit
        time.sleep(1)
    time.sleep(1)

print("""End - this shouldn't happen ever.
If this does exit, it should taint the app so we get a notification
Let's see""")#
