from .base import *

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as e_c
from selenium.webdriver.support.ui import WebDriverWait

from unipath import Path

class AddFeedTest(SoundscapesFunctionalTest):

    def navigate_to_show_list(self):
        """ Point the browser to the page that lists all of the shows """
        show_list_relative_url = reverse('show_list')
        show_list_url = self.live_server_url + show_list_relative_url
        self.browser.get(show_list_url)

    def nav_bar_item(self, item_id):
        nav_bar = self.browser.find_element_by_id('id_nav_bar')
        return nav_bar.find_element_by_id(item_id)

    def test_add_new_feed(self):
        # Add a new show via a form
        SHOW_NAME = 'Mystery Show'
        SHOW_RSS = 'http://feeds.gimletmedia.com/mysteryshow'

        self.navigate_to_show_list()
        self.nav_bar_item('id_new_show').click()

        show_form = self.browser.find_element_by_tag_name('form')
        show_form.find_element_by_id('id_name').send_keys(SHOW_NAME)
        show_form.find_element_by_id('id_rss').send_keys(SHOW_RSS)
        show_form.submit()

        # Refresh show feed
        self.nav_bar_item('id_refresh_feed').click()
        ## ...downloading episodes

        # See downloaded episodes on the show page
        svg = self.browser.find_element_by_tag_name('svg')
        episodes = svg.find_elements_by_tag_name('g')
        self.assertGreaterThan(len(episodes), 0)

        # The top episode has a single segment
        latest_episode = episodes[0]
        segments = latest_episode.find_elements_by_tag_name('g')
        self.assertEquals(len(segments), 1)

        # Click on an episode to view it
        latest_episode.click()

        # Add a new segment via a form
        self.nav_bar_item('id_new_segment').click()

        segment_form = self.browser.find_element_by_tag_name('form')
        segment_form.find_element_by_id('id_start_time').send_keys('10:23')
        segment_form.find_element_by_id('id_end_time').send_keys('11:54')
        segment_form.submit()

        # Since the segment was in the middle of the episode,
        # there are now three segments in the episode.
        svg = self.browser.find_element_by_tag_name('svg')
        segments = svg.find_elements_by_tag_name('g')
        self.assertEquals(len(segments), 3)

        # Share the segment
        self.fail('Figure out how to link to the segment')
