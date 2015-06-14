from .base import *

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from unipath import Path

class AddFeedTest(SoundscapesFunctionalTest):

    def navigate_to_show_list(self):
        """ Point the browser to the page that lists all of the shows """
        show_list_relative_url = reverse('show_list')
        show_list_url = self.live_server_url + show_list_relative_url
        self.browser.get(show_list_url)

    def find_nav_bar_item(self, item_id):
        nav_bar = self.browser.find_element_by_id('id_nav_bar')
        return nav_bar.find_element_by_id(item_id)

    def find_svg_episodes(self):
        svg = self.browser.find_element_by_tag_name('svg')
        return svg.find_elements_by_css_selector('g.episode')

    def test_add_new_feed(self):
        # Add a new show via a form
        SHOW_NAME = 'Mystery Show'
        SHOW_RSS = 'http://feeds.gimletmedia.com/mysteryshow'

        self.navigate_to_show_list()
        self.find_nav_bar_item('id_new_show').click()

        show_form = self.browser.find_element_by_tag_name('form')
        show_form.find_element_by_id('id_name').send_keys(SHOW_NAME)
        show_form.find_element_by_id('id_rss_url').send_keys(SHOW_RSS)
        show_form.submit()

        # See downloaded episodes on the show page
        episodes = self.find_svg_episodes()
        self.assertGreater(len(episodes), 0)

        # Download the first episode
        first_episode = episodes[0]
        first_episode.find_element_by_class_name('download').click()
        self.wait_for(tag = 'body')

        """
        Unsure whether downloading a episode should drill down to
        view the episode or should stay on the show view list. Right now
        it is assumed that downloading an episode drills down to view
        the episode.
        """
        episodes = self.find_svg_episodes()
        first_episode = episodes[0]
        first_episode.find_element_by_class_name('view').click()
        self.wait_for(tag = 'body')

        # Episodes start with a single segment
        svg = self.browser.find_element_by_tag_name('svg')
        segments = svg.find_elements_by_css_selector('path.segment')
        self.assertEquals(len(segents), 1)

        # Add a new segment via a form
        self.nav_bar_item('id_new_segment').click()

        segment_form = self.browser.find_element_by_tag_name('form')
        segment_form.find_element_by_id('id_start_time').send_keys('10:23')
        segment_form.find_element_by_id('id_end_time').send_keys('11:54')
        segment_form.submit()

        # Redirects to show view page

        # Since the segment was in the middle of the episode,
        # there are now three segments in the episode.
        svg = self.browser.find_element_by_tag_name('svg')
        segments = svg.find_elements_by_css_selector('path.segment')
        self.assertEquals(len(segments), 3)

        # Share the segment
        self.fail('Figure out how to link to the segment')
