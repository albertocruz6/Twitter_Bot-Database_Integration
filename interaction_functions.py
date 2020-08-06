import psycopg2 as pg2
import tweepy
import time
from auxiliary_functions import *


# Functions for specific commands to execute in the bot
def first_time_interaction(tweet, api, db_cur, talked_prev, responses_count):
    handle: str = tweet.user.screen_name
    # search the '?' keyword in the tweeet
    found_one_alone = find_char_keyword(tweet.text, '?')
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
            api.update_status('@' + handle + " We haven't interacted before... Hello! :DDD",
                              in_reply_to_status_id=tweet.id)
        upd_q = "UPDATE saved_messages SET replied_by_bot = true WHERE twitter_message_id = %s"
        db_cur.execute(upd_q, (tweet.id,))
        responses_count += 1