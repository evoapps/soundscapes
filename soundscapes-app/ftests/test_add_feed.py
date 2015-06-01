from .base import *

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as e_c
from selenium.webdriver.support.ui import WebDriverWait

from unipath import Path

class AddFeedTest(SoundscapesFunctionalTest):

    def nav_bar_item(self, item_id):
        nav_bar = self.browser.find_element_by_id('id_nav_bar')
        return nav_bar.find_element_by_id(item_id)

    def test_add_new_feed(self):
        # Add a new show via a form
        SHOW_NAME = 'StartUp'
        SHOW_RSS = 'http://feeds.gimletmedia.com/hearstartup'

        self.navigate_to_show_list()
        self.nav_bar_item('id_new_feed').click()

        show_form = self.browser.find_element_by_tag_name('form')
        show_form.find_element_by_id('id_name').send_keys(SHOW_NAME)
        show_form.find_element_by_id('id_rss').send_keys(SHOW_RSS)
        show_form.submit()

        # Download episode via show's episodes page
        episodes = self.get_items_in_list('id_episode_list')
        latest_episode = episodes[0]
        latest_episode.find_element_by_id('id_download_episode').click()

        self.fail('Figure out css locator for successfully downloaded episode')
        wait_for_locator = (By.CLASS_NAME, 'downloaded')
        error_msg = 'Episode not downloaded'
        wait_for = e_c.presence_of_element_located(wait_for_locator)
        WebDriverWait(self.browser, 10.0).until(wait_for, error_msg)

        # See downloaded episodes on homepage
        self.navigate_to_home_page()
        svg = self.browser.find_element_by_tag_name('svg')
        episode_nodes = svg.find_elements_by_tag_name('g')
        self.assertEquals(len(episode_nodes), 1)

        # View an episode
        episode_node = episode_nodes[0]
        episode_node.find_element_by_id('id_view').click()

        # Add a new segment via a form
        self.nav_bar_item('id_new_segment').click()

        segment_form = self.browser.find_element_by_tag_name('form')
        segment_form.find_element_by_id('id_start_time').send_keys('10:23')
        segment_form.find_element_by_id('id_end_time').send_keys('11:54')
        segment_form.submit()

        # Since the segment was in the middle of the episode,
        # there are now three segments in the episode.
        segments = self.get_items_in_list('id_segment_list')
        self.assertEquals(len(segments), 3)

        # Share the segment
        self.fail('Figure out how to link to the segment')
