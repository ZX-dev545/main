from facebook_scraper import *
import pandas as pd
import os

set_user_agent(
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
posts = get_posts('food', pages=5)
for post in posts:
    print(post['text'][:50])