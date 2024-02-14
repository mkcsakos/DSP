import json
from datetime import datetime
import zstandard
from pymongo.mongo_client import MongoClient

uri = "mongodb://danielsz:ysDC3xbgKOj863d7@ac-noqw4xe-shard-00-00.qqrkswo.mongodb.net:27017,ac-noqw4xe-shard-00-01.qqrkswo.mongodb.net:27017,ac-noqw4xe-shard-00-02.qqrkswo.mongodb.net:27017/?ssl=true&replicaSet=atlas-3kz2n9-shard-0&authSource=admin&retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)
db = client['dsp']
collection = db['reddit_raw']


# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)



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



with open('/projects/0/prjs0809/Daniel/DSP/data/RC_2023-10.zst', 'rb') as file_handle:
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
						if len(data['body'].split()) > 4 and len(data['body'].split()) < 40:
							collection.insert_one(data)


				except:
					pass

