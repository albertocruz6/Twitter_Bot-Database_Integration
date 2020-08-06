import tweepy
import time
import os

key = 'jsXACC0IeKkmntM2FOvqP5cCm'
secret = 'NBd21TbRBnugK1Z6DAW0LwQRYC8dd5bUtPCvT1A7rqd1OJv3Vw'
# bearer = 'AAAAAAAAAAAAAAAAAAAAAB83GgEAAAAAcpoXpPw4bp1DplJUYBbjX1i0P7g%3DOdGmaY5X3I34qjxS2PQEXxPWiJQAZdA8eJfarrcIiRrHJggZmQ'
consumer_key = '1290503301130313730-azKiPeJBv4gXDo2VMA9oSS4noabJb8'
consumer_secret = 'mAca2fCc6mwvDoonz1czbzMwlpPphdcuMcwDXostYgQhe'



auth = tweepy.OAuthHandler(key, secret)
auth.set_access_token(consumer_key,consumer_secret)

api = tweepy.API(auth)
api.update_status('@caro_salaman :3')
# f = open('status.txt', 'w')
# tweets = api.mentions_timeline()
# # f.write(tweets[0])
# print(tweets[0].user.id)
# f.close()