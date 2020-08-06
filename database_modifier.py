import psycopg2 as pg2



# establish connection with database
conn = pg2.connect(database='testme', user='postgres', password='password')
#
cur = conn.cursor()
'''
# cur.execute("DROP TABLE IF EXISTS saved_messages CASCADE ; DROP TABLE IF EXISTS saved_replies CASCADE ; DROP TABLE IF EXISTS users CASCADE")
cur.execute("""
-- CREATE TABLE users(
--	user_id SERIAL PRIMARY KEY,
--	twitter_user_id BIGINT NOT NULL UNIQUE,
--	username VARCHAR(50) NOT NULL, 	curr_handle VARCHAR(50) NOT NULL UNIQUE
-- );

CREATE TABLE saved_messages(
	message_id SERIAL PRIMARY KEY,
	twitter_message_id BIGINT NOT NULL UNIQUE,
	sender_id BIGINT NOT NULL,
	is_multimedia BOOLEAN DEFAULT false,
	has_text BOOLEAN  DEFAULT false NOT NULL,
	replied_by_bot BOOLEAN DEFAULT false,
	message_contents VARCHAR(240) CHECK(has_text = true),
	stored_date DATE DEFAULT CURRENT_DATE,
	is_deleted BOOLEAN DEFAULT false,
	number_of_interactions INTEGER DEFAULT 0
);

CREATE TABLE saved_replies(
	reply_id SERIAL PRIMARY KEY,
    twitter_message_id BIGINT NOT NULL UNIQUE,
	parent_message_id BIGINT NOT NULL, 
	sender_id BIGINT NOT NULL,
	receiver_id BIGINT  NOT NULL,
	is_multimedia BOOLEAN DEFAULT false,
	has_text BOOLEAN  DEFAULT false NOT NULL,
	message_contents VARCHAR(240) CHECK(has_text = true)
)
            """)

'''








conn.commit()
#close connections
conn.close()