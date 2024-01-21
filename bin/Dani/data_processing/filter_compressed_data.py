import os
import json
import sys
import csv
from datetime import datetime
import pip
import pickle

# def install(package):
#     if hasattr(pip, 'main'):
#         pip.main(['install', package])
#     else:
#         pip._internal.main(['install', package])

# install('zstandard')

import zstandard

subreddit_list = ['drugs',
				'trees',
				'drugsover30',
				'opiates',
				'askdrugs',
				'drugs_info',
				'realdrugs',
				'drugnerds',
				'researchchemicals',
				'addiction']

posts = []

def read_and_decode(reader, chunk_size, max_window_size, previous_chunk=None, bytes_read=0):
	chunk = reader.read(chunk_size)
	bytes_read += chunk_size
	if previous_chunk is not None:
		chunk = previous_chunk + chunk

	try:
		return chunk.decode()
	

	except UnicodeDecodeError:
		if bytes_read > max_window_size:
			raise UnicodeError(f"Unable to decode frame after reading {bytes_read:,} bytes")
		return read_and_decode(reader, chunk_size, max_window_size, chunk, bytes_read)



with open('/projects/0/prjs0809/Daniel/DSP/data/RC_2023-09.zst', 'rb') as file_handle:
		buffer = ''
		reader = zstandard.ZstdDecompressor(max_window_size=2**31).stream_reader(file_handle)
		while True:
			chunk = read_and_decode(reader, 2**27, (2**29) * 2)
			lines = (buffer + chunk).split("\n")
			for line in lines:
				if line == '':
					continue
				try:
					data = json.loads(line)
					if data['subreddit'].lower() in subreddit_list:
						posts.append(data)

				except:
					pass
			if len(posts) > 30000:
				break


with open ('/projects/0/prjs0809/Daniel/DSP/data/posts.pickle', 'wb') as f:
	pickle.dump(posts, f)
	
