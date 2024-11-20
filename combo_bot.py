import re
import datetime
from datetime import timezone
import requests
import json


url = "https://inv.nadeko.net/api/v1/channels/UCzhLhU-OeaXP4nlaMvJfKUQ/"


def most_repeated_combo(prob_combo):
    frequency = {}
    for sublist in prob_combo:
        if sublist is not None:
            sublist_tuple = tuple(sublist)
            if sublist_tuple in frequency:
                frequency[sublist_tuple] += 1
            else:
                frequency[sublist_tuple] = 1

    most_frequent = None
    max_count = 0
    for key, count in frequency.items():
        if count > max_count:
            most_frequent = key
            max_count = count

    return list(most_frequent)


def extract_numbers(sentence):
    numbers = re.findall(r'\b\d+\b', sentence)

    numbers = [int(num) for num in numbers]
    valid_numbers = [num for num in numbers if 1 <= num <= 12]
    if len(valid_numbers) == 3:
        return valid_numbers
    return None


def date_check(timestamp):
    timestamp = int(timestamp)

    dt_object = datetime.datetime.fromtimestamp(timestamp, tz=timezone.utc)
    date_from_timestamp = dt_object.date()
    current_utc_time = datetime.datetime.now(datetime.UTC).date()

    if date_from_timestamp == current_utc_time:
        return "Yes"
    else:
        return "No"


req = requests.get(url).json()
vid_ts = req['latestVideos'][0]['published']
prob_combo = []
if date_check(vid_ts) == "Yes":
    vid_id = req['latestVideos'][0]['videoId']
    comments_req = requests.get('https://inv.nadeko.net/api/v1/comments/' + vid_id).json()
    for i in range(20):
        prob_combo.append(extract_numbers(comments_req['comments'][i]['content']))
else:
    post_req = requests.get(url + "community").json()
    post_id = post_req['comments'][0]['commentId']
    comments_req = requests.get(
        "https://inv.nadeko.net/api/v1/post/" + post_id + "/comments?ucid=UCzhLhU-OeaXP4nlaMvJfKUQ/").json()
    for i in range(20):
        prob_combo.append(extract_numbers(comments_req['comments'][i]['content']))

combo = most_repeated_combo(prob_combo)


file_name = 'combo.json'
with open(file_name, 'r') as file:
    data = json.load(file)

data['combo'] = ','.join(map(str, combo))
data['date'] = str(datetime.datetime.now(datetime.UTC).date())

with open(file_name, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file)
