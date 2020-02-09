import aiohttp
import asyncio
from bs4 import BeautifulSoup
import requests
from spider import Spider

class FlexJobsSpider(Spider):
    def __init__(self):
        self.starting_page = 'jobs/web-software-development-programming'
        self.domain = 'https://www.flexjobs.com'
        self.pages_queue = asyncio.Queue()
        self.pages_already_queued = set()

    async def fetch(self, client, url):
        async with client.get(url) as response:
            return await response.text()


    async def extract_page_feature(self, bs4_soup):
        all_job_a_tags = bs4_soup.select('h5 > a')
        jobs_hrefs = [a_tag['href'] for a_tag in all_job_a_tags]

        for job_href in jobs_hrefs:
            async with aiohttp.ClientSession() as client:
                url = f'{self.domain}{job_href}'
                response = await self.fetch(client, url)
                job_page = BeautifulSoup(response, 'html.parser')
                print(job_page.select('div > h1')[0])


    async def update_pages_queue(self, bs4_soup):
        all_a_tags = bs4_soup.find_all('a', {'class': 'page-link'})
        for a_tag in all_a_tags:
            url = f"{self.domain}/{a_tag['href']}"
            if url not in self.pages_already_queued:
                self.pages_already_queued.add(url)
                await self.pages_queue.put(url)
   

    async def get_pages(self):
        async with aiohttp.ClientSession() as client:
            while not self.pages_queue.empty():
                url = await self.pages_queue.get()
                response = await self.fetch(client, url)
                current_page = BeautifulSoup(response, 'html.parser')
                # print(current_page)
                # Get other pages urls
                await self.update_pages_queue(current_page)

                # Extract page elements
                await self.extract_page_feature(current_page)


    async def run(self):
        await self.pages_queue.put(f'{self.domain}/{self.starting_page}')
        await self.get_pages()

if __name__ == '__main__':
    flex_jobs = FlexJobsSpider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(flex_jobs.run())
