from unipath import Path

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from django.test.utils import override_settings

from selenium import webdriver

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

    def get_items_in_list(self, list_id):
        episode_list = self.browser.find_element_by_id(list_id)
        return episode_list.find_elements_by_tag_name('li')
