import psycopg2 as pg2
import tweepy


# Defining important processes in functions to modularize the development
# First Stage
def engine_tweetBot_store_tweets(tweet, db_cur):
    # TWEETS storage section
    # divided in two parts: the bot's tweets and the tweets on the different existing threads
    tweet_id = tweet.id
    # 1. we get the existing tweet id's to determine if the should be inserted in databases
    db_cur.execute("SELECT twitter_message_id FROM saved_messages")
    message_ids = db_cur.fetchall()
    db_cur.execute("SELECT twitter_message_id FROM saved_messages")
    if (tweet_id,) not in message_ids:
        if len(tweet.text) > 0:
            insert_mes_q = """INSERT INTO saved_messages(twitter_message_id, sender_id, has_text, message_contents)
                                        VALUES(%s,%s,%s,%s)"""
            db_cur.execute(insert_mes_q, (tweet.id, tweet.user.id, True, tweet.text))
        else:
            insert_mes_q = """INSERT INTO saved_messages(twitter_message_id, sender_id)
                                                    VALUES(%s,%s)"""
            db_cur.execute(insert_mes_q, (tweet.id, tweet.user.id))
        # if it's also a reply
        if tweet.in_reply_to_status_id is not None:
            replying_message_id = tweet.in_reply_to_status_id
            replying_to_id = tweet.in_reply_to_user_id
            # if has text
            if len(tweet.text) > 0:
                insert_mes_q = """INSERT INTO saved_replies(twitter_message_id, parent_message_id, sender_id, receiver_id, has_text, message_contents)
                                                    VALUES(%s,%s,%s,%s,%s,%s)"""
                db_cur.execute(insert_mes_q,
                               (tweet.id, replying_message_id, tweet.user.id, replying_to_id, True, tweet.text))
            else:
                insert_mes_q = """INSERT INTO saved_replies(twitter_message_id, parent_message_id, sender_id, receiver_id)
                                                                    VALUES(%s,%s,%s,%s)"""
                db_cur.execute(insert_mes_q, (tweet.id, replying_message_id, tweet.user.id, replying_to_id))


def engine_tweetBot_store_user(db_cur, id, username, handle):
    # bool confirming that we talked or not before
    # check query to see if id exists
    db_cur.execute("SELECT twitter_user_id FROM users")
    ch_q = db_cur.fetchall()
    if len(ch_q) == 0 or (id,) not in ch_q:
        new_vals = (id, username, handle)
        insert_q = """
                            INSERT INTO users(twitter_user_id,username,curr_handle)
                            VALUES (%s,%s,%s)
                            """
        db_cur.execute(insert_q, new_vals)
        return False
    # if it exists, confirm all info of known users
    else:
        # confirming users
        call_q = "SELECT username,curr_handle FROM users WHERE twitter_user_id = %s"
        db_cur.execute(call_q, [id])
        confirm_q = db_cur.fetchall()
        for us in confirm_q:
            if username != us[0]:
                upd_q = "UPDATE users SET username = %s WHERE twitter_user_id = %s"
                db_cur.execute(upd_q, (username, id))
            if handle != us[1]:
                upd_q = "UPDATE users SET curr_handle = %s WHERE twitter_user_id = %s"
                db_cur.execute(upd_q, (handle, id))
        return True

#def engine_tweetBot_respond_interaction(tweet, db_cur, tw_api):


# General function to find specific keyword
# Later a design with Reg.Expr must be made to find longer command sequences
# TEMPORARY
def find_char_keyword(text, keyword):
    searching = text.split()
    for word in searching:
        if word.startswith('@'):
            continue
        if word == keyword:
            return True
    return False
