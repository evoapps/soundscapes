from .base import *

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from unipath import Path

class UploadNewEpisodeTest(SoundscapesFunctionalTest):

    def test_upload_a_new_episode(self):
        self.navigate_to_episode_list()

        # There are no episodes present
        episode_items = self.get_episodes_in_list()
        self.assertEquals(len(episode_items), 0)

        # Click to bring up a new episode upload form
        nav_bar = self.browser.find_element_by_id('id_nav_bar')
        upload_button = nav_bar.find_element_by_id('id_new_episode')
        upload_button.click()

        # Upload a new episode
        episode_form = self.browser.find_element_by_tag_name('form')
        path_to_new_episode = Path(settings.BASE_DIR, 'ftests/fixtures',
                                   'reply-all-26.mp3')
        upload_field = episode_form.find_element_by_id('id_mp3')
        upload_field.send_keys(path_to_new_episode)
        episode_form.submit()

        # Redirected back to the episode list after upload
        ep_list_locator = (By.ID, 'id_episode_list')
        ec = expected_conditions.presence_of_element_located(ep_list_locator)
        WebDriverWait(self.browser, 10.0).until(ec, 'Episode list not found')

        # The new episode is present in the list
        episode_items = self.get_episodes_in_list()
        self.assertEquals(len(episode_items), 1)

    def test_upload_a_new_episode_with_lookup(self):
        self.navigate_to_episode_list()

        # There are no episodes present
        episode_items = self.get_episodes_in_list()
        self.assertEquals(len(episode_items), 0)

        # Click to bring up a new episode upload form
        nav_bar = self.browser.find_element_by_id('id_nav_bar')
        upload_button = nav_bar.find_element_by_id('id_new_episode')
        upload_button.click()

        # Upload a new episode
        episode_form = self.browser.find_element_by_tag_name('form')

        path_to_new_episode = Path(settings.BASE_DIR, 'ftests/fixtures',
                                   'reply-all-26.mp3')
        upload_field = episode_form.find_element_by_id('id_mp3')
        upload_field.send_keys(path_to_new_episode)

        episode_form.find_element_by_id('id_look_up_on_save').click()
        episode_form.submit()

        # Redirected back to the episode list after upload
        ep_list_locator = (By.ID, 'id_episode_list')
        ec = expected_conditions.presence_of_element_located(ep_list_locator)
        WebDriverWait(self.browser, 10.0).until(ec, 'Episode list not found')

        # The new episode is present in the list
        episode_items = self.get_episodes_in_list()
        self.assertEquals(len(episode_items), 1)

        # Correct meta data was extracted from the mp3 file
        episode = episode_items[0]
        show_name = episode.find_element_by_id('id_show_name').text
        self.assertEquals(show_name, 'Reply All')
