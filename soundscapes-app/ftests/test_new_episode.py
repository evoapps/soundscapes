from unipath import Path

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from django.test.utils import override_settings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

TEST_MEDIA_ROOT = Path(settings.MEDIA_ROOT + '-test')

@override_settings(MEDIA_ROOT = TEST_MEDIA_ROOT)
class SoundscapesFunctionalTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = webdriver.Firefox()
        cls.browser.implicitly_wait(5)
        super(SoundscapesFunctionalTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(SoundscapesFunctionalTest, cls).tearDownClass()

    def tearDown(self):
        TEST_MEDIA_ROOT.rmtree()
        super(SoundscapesFunctionalTest, self).tearDown()

    def navigate_to_episode_list(self):
        """ Point the browser to the page that lists all of the episodes """
        episode_list_relative_url = reverse('episode_list')
        episode_list_url = self.live_server_url + episode_list_relative_url
        self.browser.get(episode_list_url)

    def get_episodes_in_list(self):
        episode_list = self.browser.find_element_by_id('id_episode_list')
        return episode_list.find_elements_by_tag_name('li')

    def test_upload_a_new_episode(self):
        self.navigate_to_episode_list()

        # There are no episodes present
        episode_items = self.get_episodes_in_list()
        self.assertEquals(len(episode_items), 0)

        # Click to bring up a new episode upload form
        nav_bar = self.browser.find_element_by_id('id_nav_bar')
        upload_button = nav_bar.find_element_by_id('id_new_episode')
        upload_button.click()
        form_locator = (By.TAG_NAME, 'form')
        ec = expected_conditions.presence_of_element_located(form_locator)
        WebDriverWait(self.browser, 10.0).until(ec, 'Form not found')

        # Upload a new episode
        episode_form = self.browser.find_element_by_tag_name('form')
        path_to_new_episode = Path(settings.BASE_DIR, 'ftests/fixtures',
                                   'sample_episode_to_upload.mp3')
        upload_field = episode_form.find_element_by_id('id_mp3')
        upload_field.send_keys(path_to_new_episode)
        episode_form.submit()

        # Redirected back to the episode list after upload
        ep_list_locator = (By.TAG_NAME, 'ul')
        ec = expected_conditions.presence_of_element_located(ep_list_locator)
        WebDriverWait(self.browser, 10.0).until(ec, 'Unordered list not found')

        # The new episode is present in the list
        episode_items = self.get_episodes_in_list()
        self.assertEquals(len(episode_items), 1)
