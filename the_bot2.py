import tweepy
import psycopg2
import time


print("this bot is working")
CONSUMER_KEY = '7di1l1zH2exr1LwrlC9fbt9Fp'
CONSUMER_SECRET = 'sqwgFgssleBF7LyikH9eAjKsEsj2F2Ggqvdk3LLLqXZxFGkLsU'
ACCESS_KEY = '1132924430143905792-QQhRZjWMzEpUSbSTGXG65hBwalwz3H'
ACCESS_SECRET = 'uOg33UdvMLHwwnDgA5b1WLtoyhK7DK55ppvT5wN0Av58L'

auth = tweepy.OAuthHandler(CONSUMER_KEY , CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY , ACCESS_SECRET)
api = tweepy.API(auth)

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


def upload_answer():
	c.execute('''SELECT name,id,answers,send FROM qa WHERE answers IS NOT NULL AND send IS NULL ''')
	rows = c.fetchall()
	print(rows)
	for r in rows:
		print(r)
		api.update_status('@' + r[0] + ''' - ''' + r[2], r[1])
		c.execute(''' UPDATE qa SET send ='sent' WHERE id = (%s)''', [r[1]])
		con.commit()
		print(r[0])



def disconnect():
	c.close()
	con.close()
	print('disconnected')

connect_to_database()

while True:
	upload_answer()
	time.sleep(2)

disconnect()