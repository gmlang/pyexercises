import tweepy
import sqlite3

# OAuth authentication
consumer_key = 'TGnF2UQFR15Im3TYDfyQOw'
consumer_secret = '85jkKlzJ57uk6KzTCMNeKdCCYva6MhAlg897FKGPEmI'
access_token = '129679351-qa9wATbeAU2efqSsh1KEmCdkYo8VkLDDlM3C3QuH'
access_token_secret = '6rO2WS5VTtjJP1mlWPFMk2KrhHRXMbjxUu8MmehFw'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Create local database
conn = sqlite3.connect('twitter.db')
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS
Twitter (name TEXT, is_retrieved INTEGER, location TEXT, 
         num_of_occurrences INTEGER)''')

# meat of the program
while True:
    acct = raw_input('Enter a Twitter account or quit: ')
    if acct == 'quit':
        break
    if len(acct) < 1: # if Enter is pressed
        cur.execute('SELECT name FROM Twitter WHERE is_retrieved = 0 LIMIT 1')
        try:
            acct = cur.fetchone()[0]
        except:
            print 'All accounts stored in database have been retrieved.'
            continue
    cur.execute('UPDATE Twitter SET is_retrieved=1 WHERE name = ?', (acct,))
    countnew = 0
    countold = 0
    # for friend in api.friends(acct): # will only get first 20 friends
    for friend in tweepy.Cursor(api.friends, acct, 'slug').items():  # get all friends      
        name = friend.screen_name
        location = friend.location
        try: # if friend is already in the database
            cur.execute('SELECT num_of_occurrences FROM Twitter WHERE name = ?\
                        LIMIT 1', (name, ))
            count = cur.fetchone()[0]      # retrieve its num_of_occurrences
            cur.execute('UPDATE Twitter SET num_of_occurrences = ? WHERE \
                        name = ?', (count+1, name)) # update its num_of_occurrences
            countold += 1
        except: # otherwise
            cur.execute('''INSERT INTO Twitter 
                           (name, is_retrieved, location, num_of_occurrences)
                           VALUES (?, ?, ?, ?)''', 
                           (name, 0, location, 1)) # store it
            countnew += 1
    print 'New accounts=', countnew, 'revisited=', countold
    conn.commit()
    
cur.close()    