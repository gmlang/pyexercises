import tweepy
import sqlite3
import time
import itertools

CONSUMER_KEY = 'replace with your consumer_key found on twitter dev'
CONSUMER_SECRET = 'replace with your consumer_secret found on twitter dev'
ACCESS_TOKEN = 'replace with your access_token found on twitter dev'
ACCESS_TOKEN_SECRET ='replace w. your access_token_secret found on twitter dev'

def wait(num_of_api_calls):
    num_of_api_calls += 1
    if num_of_api_calls > 15:
        time.sleep(60*16)
        num_of_api_calls = 0
    return num_of_api_calls
    
def paginate(iterable, page_size):
    while True:
        i1, i2 = itertools.tee(iterable)
        iterable, page = (itertools.islice(i1, page_size, None),
                          list(itertools.islice(i2, page_size)))
        if len(page) == 0:
            break
        yield page

def get_user_from_table(cur, user_name, user_location):
    """returns False if user is already in the database; True otherwise 

    cur: a sqlite3 connection cursor to a database
    user_name: string
    user_location: string
    """
    new = False
    cur.execute('SELECT num_of_occurrences FROM Twitter WHERE name=? LIMIT 1', 
                (user_name, ))
    try: # if user is already in the database
        count = cur.fetchone()[0]      # retrieve its num_of_occurrences
        cur.execute('UPDATE Twitter SET num_of_occurrences = ? WHERE name = ?',
                    (count+1, user_name)) # update its num_of_occurrences
    except: # otherwise
        cur.execute('''INSERT INTO Twitter (name, is_retrieved, location, 
                       num_of_occurrences) VALUES (?, ?, ?, ?)''', 
                       (user_name, 0, user_location, 1)) # store it 
        new = True    
    return new 

    
if __name__ == '__main__':
    # OAuth authentication
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Create local database
    conn = sqlite3.connect('twitter.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Twitter 
                   (name TEXT, is_retrieved INTEGER, location TEXT, 
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
        countnew, countold = 0, 0
        num_of_api_calls = 0
        # for friend in api.friends(acct): # will only get first 20 friends
        # for friend_list in tweepy.Cursor(api.friends, id=acct).pages():  # each friend_list will only have 20 friends
        for friends_ids_lst in tweepy.Cursor(api.friends_ids, id=acct).pages():  # each friends_ids_lst has 5000 or less friends
            num_of_api_calls = wait(num_of_api_calls)
            for block in paginate(friends_ids_lst, 100): # break friends_ids_lst into blocks of size 100, twitter limit is 100                
                num_of_api_calls = wait(num_of_api_calls)
                for friend in api.lookup_users(user_ids=block):
                    name = friend.screen_name
                    location = friend.location
                    new = get_user_from_table(cur, name, location)
                    if new: countnew += 1 
                    else: countold += 1
        print 'New accounts=', countnew, 'revisited=', countold
        conn.commit()
        
    cur.close()    