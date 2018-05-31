import requests
from bs4 import BeautifulSoup as bs


class component(object):

    @classmethod
    def get_data(cls, *args, **kwargs):

        base = "https://www.youtube.com/results?search_query="
        qstring = sr
        r = requests.get(base + qstring)
        page = r.text

        # parse using beautiful soup
        soup = bs(page, 'html.parser')

        # Find all <a> tags because they define hyper-links.  The parameter href is the link.
        # Only find <a> tags that are classified as YouTube User Interface XML
        # Tile Links: yt-uix-tile-link
        vids = soup.findAll('a', attrs={'class': 'yt-uix-tile-link'})

        # Extract weblink for each tile using the href property.  Append to
        # list.
        videolist = []
        videoname = []
        for v in vids:
            tmp = 'https://www.youtube.com' + v['href']
            videolist.append(tmp)
            videoname.append(v['title'])

        # Print search results
        print('Recommended videos: ')
        for i in range(len(videolist)):
            if 'googleads' not in videolist[i]:  # avoid google ads
                # title of video, truncated
                print('\n' + videoname[i][0:60])
                print(videolist[i])  # url of video
