import psycopg2 as pg2
import tweepy
import time
from auxiliary_functions import *


# Functions for specific commands to execute in the bot
def first_time_interaction(tweet, api, db_cur, talked_prev, responses_count):
    handle: str = tweet.user.screen_name
    # search the '?' keyword in the tweet
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
            time.sleep(120)
            responses_count = 0
        if talked_prev:
            api.update_status('@' + handle + " We have interacted before! 😊 :DDD", in_reply_to_status_id=tweet.id)
        else:
            api.update_status('@' + handle + " We haven't interacted before... Hello! :DDD",
                              in_reply_to_status_id=tweet.id)
        upd_q = "UPDATE saved_messages SET replied_by_bot = true WHERE twitter_message_id = %s"
        db_cur.execute(upd_q, (tweet.id,))
        responses_count += 1


def request_convo_thread_interaction(tweet, api, db_cur, responses_count):
    # if prompted the bot ill return with all the available tweets in which the user in question has interacted with
    # the bot!
    id: int = tweet.user.id
    username: str = tweet.user.name
    handle: str = tweet.user.screen_name

    # to quote retweet we must find the url for the different tweets and update status with them
    # the challenge lies in making a thread with these update status
    # we can build each tweet link in the format f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"

    # first search the keyword convo_thread?
    found_one_alone = find_char_keyword(tweet.text, 'convo_thread?')
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
            time.sleep(120)
            responses_count = 0
        # determine if there has been any tweets from the user
        user_tweets_q = """
                        SELECT twitter_message_id
                        FROM saved_messages
                        WHERE sender_id = %s;
        """
        db_cur.execute(user_tweets_q, (id,))
        user_tweets = db_cur.fetchall()
        if len(user_tweets) != 0:
            #commented for now
            if len(user_tweets) == 1:
                api.update_status("I think this is your first interaction with me! 😅", in_reply_to_status_id=tweet.id)
            else:
                api.update_status("Sure! Creating thread of our past interactions!", in_reply_to_status_id=tweet.id)
            responses_count+=1
            # go through all the tweets and connect them
            times = 0
            for interaction in user_tweets:
                times+=1
                # check if cooldown is needed
                if responses_count == 5:
                    print('Waiting.....(slowing down boi)')
                    time.sleep(120)
                    responses_count = 0
                # get the last tweet made by the bot to reply to it and make thread
                last_bot_tweet = api.user_timeline(count=1)[0]
                last_bot_tweet_id = last_bot_tweet.id
                # get tweet id from the database log and formulate the quote retweet link
                target_id = interaction
                target_final_url = f"https://twitter.com/{handle}/status/{target_id[0]}"
                # tweet the result
                api.update_status(str(times) + " " + target_final_url, in_reply_to_status_id=last_bot_tweet_id)
                responses_count += 1
                time.sleep(15)

