import unittest
from bugspad import Bug
from random import randint


class BugTest(unittest.TestCase):

    """
    TestCase for Bug class.

    """

    def setUp(self):
        self.AUTH_ERROR = "\"Authentication failure.\"\n"
        self.SUCCESS = "\"Success\"\n"
        self.WRONG_KWARGS = "Wrong kwargs"
        self.WRONG_PRODUCT = "No such product."

        self.url = "http://127.0.0.1:9998"
        self.usr = "kushaldas@gmail.com"
        self.pwd = "asdf"

        self.no_id_bug = Bug(self.url, self.usr, self.pwd)
        self.with_id_bug = Bug(self.url,
                               self.usr,
                               self.pwd,
                               randint(1, 10))
        self.wrong_auth_bug = Bug(self.url,
                                  "wrongusr",
                                  self.pwd,
                                  1)


    def test_add_comment_without_id_raises_Exception(self):
        self.assertRaises(NameError,
                          self.no_id_bug.add_comment,
                          "this is a comment")

    def test_add_comment_wrong_auth_returns_AUTH_ERROR(self):
        response = self.wrong_auth_bug.add_comment("this is a comment")
        self.assertEqual(response, self.AUTH_ERROR)

    def test_add_comment_returns_comment_id(self):
        try:
            int(self.with_id_bug.add_comment("this is a comment"))
        except ValueError:
            self.fail("Server Return is not valid comment id")


    def test_update_bug_without_id_raises_Exception(self):
        self.assertRaises(NameError,
                          self.no_id_bug.update_bug,
                          {'hardware' : 'x86_64'})

    def test_update_bug_wrong_auth_returns_AUTH_ERROR(self):
        response = self.wrong_auth_bug.update_bug(status="new",
                                                  hardware="x86_64")
        self.assertEqual(response, self.AUTH_ERROR)

    def test_update_bug_returns_SUCCESS(self):
        response = self.with_id_bug.update_bug(status="new",
                                               hardware="x86_64",
                                               priority="high",
                                               severity="high",
                                               whiteboard="Some text",
                                               fixedinver="18",
                                               version="22",
                                               component_id=55555)
        self.assertEqual(response, self.SUCCESS) # not really useful

    def test_update_bug_wrong_kwargs_returns_WRONG_KWARGS(self):
        response = self.with_id_bug.update_bug(wrong_kwarg="dummy")
        self.assertNotEqual(response, self.SUCCESS)


    def test_new_bug_returns_bug_instance(self):
        response = self.no_id_bug.new_bug("This is a summary",
                                 "I had a bug...!",
                                 hardware="x86_64",
                                 priority="high",
                                 severity="high",
                                 status="new",
                                 whiteboard="Some text",
                                 version="20",
                                 component_id=randint(1, 16000),
                                 emails="kushaldas@gmail.com")

        self.assertIsInstance(response, Bug)
        try:
            int(response.bug_id)
        except ValueError:
            self.fail("Instance has not valid bug's id")

    def test_new_bug_wrong_kwargs_returns_WRONG_KWARGS(self):
        response = self.no_id_bug.new_bug("This is a summary",
                                            "I had a bug...!",
                                            1,
                                            wrong_kwarg="dummy")
        self.assertEqual(response, self.WRONG_KWARGS)

    def test_new_bug_wrong_auth_returns_AUTH_ERROR(self):
        response = self.wrong_auth_bug.new_bug("This is a summary",
                                               "I had a bug...!",
                                               1)
        self.assertEqual(response, self.AUTH_ERROR)


    @unittest.skip("Too slow, comment this line to test this function")
    def test_get_components_list_returns_components_dict(self):
        response = self.no_id_bug.get_components_list(1)

        self.assertIs(type(response), dict)
        self.assertNotEqual(len(response), 0)
        for component in response.iteritems():
            self.assertEqual(component[0], component[1][1])

    @unittest.skip("Too slow, comment this line to test this function")
    def test_get_components_list_auth_not_required(self):
        response = self.wrong_auth_bug.get_components_list(1)

        self.assertIs(type(response), dict)
        self.assertNotEqual(len(response), 0)
        for component in response.iteritems():
            self.assertEqual(component[0], component[1][1])

    def test_get_components_list_wrong_product_id_returns_empty_dict(self):
        response = self.no_id_bug.get_components_list(0)

        self.assertIs(type(response), dict)
        self.assertEqual(len(response), 0)


    def test_add_component_returns_component_info_dict(self):
        response = self.with_id_bug.add_component('new_component',
                                                  'This is an awesome new '
                                                  'useless component',
                                                  1)
        try:
            int(response["id"])
        except ValueError:
            self.fail("Server return is not a valid id value")
        self.assertEqual('new_component', response['name'])
        self.assertEqual('This is an awesome new useless component',
                         response['description'])

    def test_add_component_wrong_product_id_returns_WRONG_PRODUCT(self):
        response = self.with_id_bug.add_component('new_component', 
                                                  'This is an awesome new '
                                                  'useless component',
                                                  0)
        self.assertEqual(response['id'], self.WRONG_PRODUCT)


    def test_get_latest_created_bugs_returns_latest_bugs_list(self):
        response = self.with_id_bug.get_latest_created_bugs()

        self.assertIs(type(response), list)
        self.assertIn(len(response), range(1, 11))  # 10 at max, but not least
        for bug in response:
            self.assertEqual(len(bug.keys()), 3)
            self.assertTrue('id' in bug)
            self.assertTrue('status' in bug)
            self.assertTrue('summary' in bug)

            # Range inversed (start, stop(not included), step)
            self.assertEqual([bug['id'] for bug in response],
                         range(response[0]['id'], (response[-1]['id']-1), -1))


    def test_get_latest_updated_bugs_returns_latest_bugs_list(self):
        response = self.with_id_bug.get_latest_updated_bugs()

        self.assertIs(type(response), list)
        self.assertIn(len(response), range(1, 11))
        for bug in response:
            self.assertEqual(len(bug.keys()), 3)
            self.assertTrue('id' in bug)
            self.assertTrue('status' in bug)
            self.assertTrue('summary' in bug)


    def test_add_release_returns_SUCCESS(self):
        response = self.with_id_bug.add_release('BP-2')
        self.assertEqual(response, self.SUCCESS)


    def test_get_releases_returns_releases_list(self):
        response = self.with_id_bug.get_releases()

        self.assertIs(type(response), list)
        for release in response:
            self.assertIsInstance(release, basestring)


    def test_add_product_returns_product_info_dict(self):
        response = self.with_id_bug.add_product("New product",
                                                "This is going to blow "
                                                "your mind!")
        try:
            int(response["id"])
        except ValueError:
            self.fail("Server return is not a valid id value")
        self.assertIs(type(response), dict)
        self.assertEqual(len(response), 3)
        self.assertTrue('id' in response)
        self.assertTrue('name' in response)
        self.assertTrue('description' in response)
        self.assertEqual(response['name'], "New product")
        self.assertEqual(response['description'],
                         "This is going to blow your mind!")


    def test_add_bug_cc_one_email_returns_empty_string(self):
        response = self.with_id_bug.add_bug_cc('kushaldas@gmail.com')
        self.assertEqual(response, '')

    def test_add_bug_cc_many_parameters_return_empty_string(self):
        response = self.with_id_bug.add_bug_cc('kushaldas@gmail.com',
                                               'arnauorriolsmiro@gmail.com')
        self.assertEqual(response, '')

    def test_add_bug_cc_emails_list_return_empty_string(self):
        emails_list = ['kushaldas@gmail.com', 'arnauorriolsmiro@gmail.com']
        response = self.with_id_bug.add_bug_cc(emails_list)
        self.assertEqual(response, '')

    def test_remove_bug_cc_one_email_returns_empty_string(self):
        response = self.with_id_bug.remove_bug_cc('kushaldas@gmail.com')
        self.assertEqual(response, '')

    def test_remove_bug_cc_many_parameters_returns_empty_string(self):
        response = self.with_id_bug.remove_bug_cc('kushaldas@gmail.com',
                                                  'arnauorriolsmiro@gmail.com')
        self.assertEqual(response, '')

    def test_remove_bug_cc_emails_list_returns_empty_string(self):
        emails_list = ['kushaldas@gmail.com', 'arnauorriolsmiro@gmail.com']
        response = self.with_id_bug.remove_bug_cc(emails_list)
        self.assertEqual(response, '')



if __name__ == "__main__":
    unittest.main(verbosity = 2)

