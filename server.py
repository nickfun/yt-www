import os
import time
import math
import json
from flask import Flask, render_template, request
import greenstalk
import string
import random


APP_PORT = int(os.environ.get('APP_PORT', -1))
BEANSTALK_PORT = int(os.environ.get('BEANSTALK_PORT', -1))
DOWNLOAD_FOLDER = os.environ.get('DOWNLOAD_FOLDER', './videos')


if APP_PORT == -1:
	print("APP_PORT required")
	exit(-1)
if BEANSTALK_PORT == -1:
	print("BEANSTALK_PORT required")
	exit(-1)

queue = greenstalk.Client(host='127.0.0.1', port=BEANSTALK_PORT)

print("Connected to beanstalk")

def getVideoList():
	videos = []
	for fn in os.listdir(DOWNLOAD_FOLDER):
		parts = fn.split(".")
		i = len(parts)-1
		ext = parts[i]
		if ext in ['mp4', 'mkv', 'webm']:
			parts.pop()
			v_id = ".".join(parts)
			url = DOWNLOAD_FOLDER + '/' + fn
			size = os.path.getsize(DOWNLOAD_FOLDER + "/" + fn)
			videos.append({
				"url": url,
				"name": v_id,
				"id": v_id,
				"size": math.floor(size / 1024 / 1024),
			})
	return videos

def submitUrl(url):
	data = {
		"url": url,
		"type": "video"
	}
	body = json.dumps(data)
	print("inserting: " + body)
	queue.put(body)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index(msg = False):
	print("Message is " + str(msg))
	template_data = {
		"message": msg,
		"video_list": getVideoList(),
		"rand_str": id_generator(),
	}
	return render_template('index.html', data=template_data)

@app.route("/", methods=['POST'])
def submit():
	url = '--nothing--'
	if 'url' in request.values:
		url = request.values['url']
		submitUrl(url)
	return index("You submitted: " + url)

print("web server running on port " + str(APP_PORT))
app.run(host='0.0.0.0', port=APP_PORT, debug=True)
