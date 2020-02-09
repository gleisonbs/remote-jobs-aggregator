import aiohttp
import asyncio
from bs4 import BeautifulSoup
import requests
from spider import Spider

class FlexJobsSpider(Spider):
    def __init__(self):
        self.starting_page = 'jobs/web-software-development-programming'
        self.domain = 'https://www.flexjobs.com'
        # self.pages_to_visit = set([f'{self.domain}/{self.starting_page}'])
        self.pages_queue = asyncio.Queue()

    def extract_page_feature(self, bs4_soup):
        print(bs4_soup.title)

    async def update_pages_queue(self, bs4_soup):
        all_a_tags = bs4_soup.find_all('a', {'class': 'page-link'})
        for a_tag in all_a_tags:
            await self.pages_queue.put(f"{self.domain}/{a_tag['href']}")

    async def fetch(self, client, url):
        async with client.get(url) as response:
            return await response.text()

    async def get_pages(self):
        async with aiohttp.ClientSession() as client:
            while not self.pages_queue.empty():
                # print(self.pages_queue)
                url = await self.pages_queue.get()
                response = await self.fetch(client, url)
                current_page = BeautifulSoup(response, 'html.parser')
                # print(current_page)
                # Get other pages urls
                await self.update_pages_queue(current_page)

                # Extract page elements
                self.extract_page_feature(current_page)

    async def run(self):
        await self.pages_queue.put(f'{self.domain}/{self.starting_page}')
        await self.get_pages()

if __name__ == '__main__':
    flex_jobs = FlexJobsSpider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(flex_jobs.run())
