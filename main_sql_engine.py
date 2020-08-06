import psycopg2 as pg2
import tweepy
import time
from auxiliary_functions import *

key = 'jsXACC0IeKkmntM2FOvqP5cCm'
secret = 'NBd21TbRBnugK1Z6DAW0LwQRYC8dd5bUtPCvT1A7rqd1OJv3Vw'
consumer_key = '1290503301130313730-azKiPeJBv4gXDo2VMA9oSS4noabJb8'
consumer_secret = 'mAca2fCc6mwvDoonz1czbzMwlpPphdcuMcwDXostYgQhe'

auth = tweepy.OAuthHandler(key, secret)
auth.set_access_token(consumer_key, consumer_secret)

api = tweepy.API(auth)


# establish connection with database
conn = pg2.connect(database='testme', user='postgres', password='password')
#
db_cur = conn.cursor()

responses_count = 0  # we will limit the amount of responses to five every 5 min, this will count them

tweets = api.mentions_timeline()
# db_cur.execute("SELECT COUNT(*) FROM saved_messages")
# stored_messages = db_cur.fetchall()[0][0]
# all_messages = len(tweets)
stored_messages = 0
all_messages = 0

while stored_messages <= all_messages:
    # just in case
    all_messages = len(api.mentions_timeline())
    db_cur.execute("SELECT COUNT(*) FROM saved_messages")
    stored_messages = db_cur.fetchall()[0][0]

    # if there are no new messages wait two minutes
    if stored_messages == all_messages:
        print('Waiting.....')
        time.sleep(120)
        all_messages = len(api.mentions_timeline())
        db_cur.execute("SELECT COUNT(*) FROM saved_messages")
        stored_messages = db_cur.fetchall()[0][0]
        # if two minutes passed terminate!
        if stored_messages == all_messages:
            print('Going to sleep!')
            break
    #   Begin functionality
    else:
        print('Here we go! :)')
        for tweet in tweets:
            # TWEETS storage section
            engine_tweetBot_store_tweets(tweet, db_cur)

            # # # # # # # # # # # # # # # # # # # # # #
            # USER storage
            id: int = tweet.user.id
            username: str = tweet.user.name
            handle: str = tweet.user.screen_name
            # command to add the username first!
            talked_prev = engine_tweetBot_store_user(db_cur, id, username, handle)

            # # # # # # # # # # # # # # # # # # # # # #
            # BOT responds to '?'
            # we check if the text is asking the bot
            text = tweet.text
            # search for a '?' sign
            searching = text.split()
            found_one_alone = False
            for word in searching:
                if word.startswith('@'):
                    continue
                if word == '?':
                    found_one_alone = True

            # determine if it has not responded to the tweet
            need_to_respond_q = """
                                SELECT replied_by_bot
                                FROM saved_messages
                                WHERE twitter_message_id = %s;
                """
            db_cur.execute(need_to_respond_q, (tweet.id,))
            has_responded = db_cur.fetchall()[0][0]

            if found_one_alone and not has_responded:
                # cooldown
                if responses_count == 5:
                    print('Waiting.....(slowing down boi)')
                    time.sleep(30)
                    responses_count = 0
                if talked_prev:
                    api.update_status('@' + handle + " We have interacted before! 😊 :DDD", in_reply_to_status_id=tweet.id)
                else:
                    api.update_status('@' + handle + " We haven't interacted before... Hello! :DDD", in_reply_to_status_id=tweet.id)
                upd_q = "UPDATE saved_messages SET replied_by_bot = true WHERE twitter_message_id = %s"
                db_cur.execute(upd_q, (tweet.id,))
                responses_count += 1

            # Final temporary checks
            db_cur.execute("""
                                    UPDATE users
                                    SET number_of_interactions =    (SELECT COUNT(*)
				                                                    FROM saved_messages
							                                        WHERE users.twitter_user_id = saved_messages.sender_id);""")
conn.commit()
#close connections
conn.close()