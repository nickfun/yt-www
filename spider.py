import os
import time
import json
import greenstalk
import subprocess

DOWNLOAD_FOLDER = os.environ.get('DOWNLOAD_FOLDER', '.')
BEANSTALK_PORT = int(os.environ.get('BEANSTALK_PORT', -1))

os.chdir(DOWNLOAD_FOLDER)

print("cd to folder " + DOWNLOAD_FOLDER)

if BEANSTALK_PORT == -1:
	print("BEANSTALK_PORT required")
	exit(-1)

queue = greenstalk.Client(host='127.0.0.1', port=BEANSTALK_PORT)

print("Connected to beanstalk")

def downloadVideo(body):
	url = body['url']
	time.sleep(1)
	print("*** DOWNLOADING *** " + url)
	args = [
		'youtube-dl',
		'--restrict-filenames',
		'--write-description',
		'--write-info-json',
		'--no-playlist',
		'--write-thumbnail',
		url
	]
	print(args)
	result = subprocess.run(args)
	print("*** END PROCESS ***	")
	time.sleep(1)
	return True

while True:
	job = queue.reserve()
	print(job.body)
	body = json.loads(job.body)
	if downloadVideo(body):
		queue.delete(job)
		print("job complete")
	else:
		queue.release(job)
		print("job incomplete, returned to queue")
	time.sleep(1)

print("exit spider")
