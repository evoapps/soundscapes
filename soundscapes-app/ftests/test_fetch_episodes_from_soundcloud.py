from unipath import Path

class FetchEpisodesFromSoundcloudTest(SoundscapesFunctionalTest):

    def test_fetch_episodes_from_soundcloud(self):
        self.navigate_to_episode_list()

        # There are no episodes present
        episode_items = self.get_episodes_in_list()
        self.assertEquals(len(episode_items), 0)

        # Click to bring up a new episode upload form
        nav_bar = self.browser.find_element_by_id('id_nav_bar')
        update_button = nav_bar.find_element_by_id('id_update_feed')
        update_button.click()

        # Redirected back to the episode list after upload
        ep_list_locator = (By.ID, 'id_episode_list')
        ec = expected_conditions.presence_of_element_located(ep_list_locator)
        WebDriverWait(self.browser, 10.0).until(ec, 'Episode list not found')

        episode_items = self.get_episodes_in_list()
        self.assertGreaterThan(len(episode_items), 10)
