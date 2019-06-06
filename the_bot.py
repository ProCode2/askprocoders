import tweepy
import psycopg2
import time

FILE_NAME = 'last_seen_id.txt'

def connect_to_database():
	global c
	global con
	con = psycopg2.connect(
	      host = 'localhost',
	      database = 'askprocoders',
	      user = 'postgres',
	      password = '1234')

	c = con.cursor()
	print('connected to database')


def disconnect():
	c.close()
	con.close()
	print('disconnected')




# def create_table():
# 	c.execute('''CREATE TABLE IF NOT EXISTS QA(
# 	   SNO BIGSERIAL PRIMARY KEY     NOT NULL,
# 	   ID           BIGINT    NOT NULL,
# 	   NAME            TEXT     NOT NULL,
# 	   QUESTIONS      TEXT,
# 	   ANSWERS         TEXT,
# 	   SEND            TEXT )''')
# 	con.commit()
# 	print('Table is created')



print("this bot is working")
CONSUMER_KEY = '7di1l1zH2exr1LwrlC9fbt9Fp'
CONSUMER_SECRET = 'sqwgFgssleBF7LyikH9eAjKsEsj2F2Ggqvdk3LLLqXZxFGkLsU'
ACCESS_KEY = '1132924430143905792-QQhRZjWMzEpUSbSTGXG65hBwalwz3H'
ACCESS_SECRET = 'uOg33UdvMLHwwnDgA5b1WLtoyhK7DK55ppvT5wN0Av58L'

auth = tweepy.OAuthHandler(CONSUMER_KEY , CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY , ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

def writeMentions(user_info):
	c.execute('''INSERT INTO qa(id , name , questions) VALUES(%s , %s , %s)''' , (user_info[0] , user_info[1] ,user_info[2]))
	con.commit()
	print('inserted')






def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_and_store():
	last_seen_id = retrieve_last_seen_id(FILE_NAME)
	mentions = api.mentions_timeline(last_seen_id , tweet_mode = 'extended')

	for mention in reversed(mentions):
		print(str(mention.id) +' - '+ mention.user.screen_name +' - ' + mention.full_text)
		user_info = [mention.id , mention.user.screen_name, mention.full_text]
		writeMentions(user_info)
		last_seen_id = mention.id
		store_last_seen_id(last_seen_id , FILE_NAME)
		api.update_status('@' + mention.user.screen_name + ''' HeyThere!We ll reach you in a momment , Don't worry! ''', mention.id)

connect_to_database()
# create_table()
while True:
	reply_and_store()
	time.sleep(2)
	
disconnect()

    

