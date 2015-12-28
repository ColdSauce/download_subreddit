from BeautifulSoup import BeautifulSoup
import requests
import time



TOTAL_SUBMISSIONS = 1000 
POSTS_PER_PAGE = 25
TOTAL_PAGES = TOTAL_SUBMISSIONS / POSTS_PER_PAGE
BASE_REDDIT_URL = "http://reddit.com/r/strawmen/new/"
REDDIT_RATE_LIMIT_SECS = 2

# get_page lets you get a specific page in the subreddit's /new/ category
# if you know the count and the after id
def get_page(count, after):
    payload = {'count' : count, 'after' : after}
    r = requests.get(BASE_REDDIT_URL, params = payload)
    return r

# get_first_page gets the first page in the subreddit /new/ category
def get_first_page():
    user_agent = {'User-agent': 'Mozilla/5.0'}
    r = requests.get(BASE_REDDIT_URL, headers = user_agent)
    return r

# get_page_from_raw_url gives you a page if you know the raw url of the
# page you're trying to get. Useful if you are getting the url from
# some anchor tag in the html itself.
def get_page_from_raw_url(url):
    user_agent = {'User-agent': 'Mozilla/5.0'}
    r = requests.get(url, headers = user_agent)
    return r

       
# get_submissions_from_soup returns a list of submissions that 
# have i.imgur.com in them. This is because this script is only
# useful to me atm. However, I will make this more general in 
# the future.
def get_submissions_from_soup(soup_data):
    submissions = []
    for a in soup_data.findAll('a', href=True):
        if 'http://i.imgur.com' in str(a['href']):
            submissions.append(str(a['href']))
    return submissions

# get_next_url_from_soup gets the url of the page after the 
# current one.
def get_next_url_from_soup(soup_data):
    for a in soup_data.findAll('a', href=True):
        if 'next' in str(a.contents[0]):
            return str(a['href'])


def main():

    all_submissions = []
    first_page = get_first_page().text
    soup = BeautifulSoup(first_page)
    submissions = get_submissions_from_soup(soup)
    next_url = get_next_url_from_soup(soup)
    time.sleep(REDDIT_RATE_LIMIT_SECS)
    count = POSTS_PER_PAGE
    try:
        # Runs until it doesn't have a next button. 
        # Not the most elegant way of doing things but it works.
        # TODO: Make this not be a try/except lmaonade. 
        while 1:
            print "Now doing: " + str(count)
            count = count + POSTS_PER_PAGE 
            page = get_page_from_raw_url(next_url).text
            soup = BeautifulSoup(page)
            submissions = get_submissions_from_soup(soup)

            # TODO: Make this for loop go away. 
            for submission in submissions:
                all_submissions.append(submission)

            next_url = get_next_url_from_soup(soup)
            print 'next url: ' + str(next_url)
            time.sleep(REDDIT_RATE_LIMIT_SECS)

    except:
        with open('submissions.txt', 'w') as f:
            for submission in all_submissions:
                f.write(str(submission) + "\n")


if __name__ == "__main__":
    main()
