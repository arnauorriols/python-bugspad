import unittest
from bugspad import Bug
import random


class BugTest (unittest.TestCase):
    """
    TestCase for Bug class.

    """

    def setUp(self):
        self.AUTH_ERROR = "\"Authentication failure.\"\n"
        self.SUCCESS = "\"Success\"\n"
        self.WRONG_KWARGS = "Wrong kwargs"
        self.url = "http://127.0.0.1:9998"
        self.usr = "arnauorriolsmiro@gmail.com"
        self.pwd = "asdf"

        self.no_id_bug = Bug(self.url, self.usr, self.pwd, 47062)
        self.with_id_bug = Bug(self.url, 
                               self.usr, 
                               self.pwd, 
                               47062,
                               random.randint(22567, 22587))

        self.wrong_auth_bug = Bug(self.url, 
                                  "wrongusr", 
                                  self.pwd, 
                                  47062, 
                                  random.randint(22567, 22587))




    def test_add_comment_without_id_raises_Exception(self):

        self.assertRaises(NameError, 
                          self.no_id_bug.add_comment, 
                          "this is a comment")



    def test_add_comment_wrong_auth_returns_AUTH_ERROR(self):

        response = self.wrong_auth_bug.add_comment("this is a comment")
        self.assertEqual(str(response), self.AUTH_ERROR)



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

        response = self.wrong_auth_bug.update_bug(status = "new", 
                                                  hardware = "x86_64")

        self.assertEqual(response, self.AUTH_ERROR)



    def test_update_bug_returns_success_response(self):
        response = self.with_id_bug.update_bug(status = "new", 
                                               hardware = "x86_64",
                                               priority = "high",
                                               severity = "high",
                                               whiteboard = "Some text",
                                               fixedinver = "18",
                                               version = "20",
                                               component_id = 55555)

        self.assertEqual(response, self.SUCCESS) # not really useful



    def test_update_bug_wrong_kwargs_returns_WRONG_KWARGS(self):

        response = self.with_id_bug.update_bug(wrong_kwarg = "dummy")

        self.assertNotEqual(response, self.SUCCESS)



    def test_new_bug_returns_bug_id(self):

        try:
            int(self.with_id_bug.new_bug("This is a summary",
                                         "I had a bug...!",
                                         hardware = "x86_64",
                                         priority = "high",
                                         severity = "high",
                                         whiteboard = "Some text",
                                         fixedinver = "18",
                                         version = "20",
                                         component_id = 55555
                                         ))

        except ValueError:
            self.fail("Server Return is not valid comment id")



    def test_new_bug_wrong_kwargs_returns_WRONG_KWARGS(self):

        response = self.with_id_bug.new_bug("This is a summary", 
                                            "I had a bug...!",
                                            wrong_kwarg = "dummy")

        self.assertEqual(response, self.WRONG_KWARGS)



    def test_get_components_list_returns_components_dict(self):

        response = self.with_id_bug.get_components_list(2)

        self.assertIs(type(response), dict)
        self.assertNotEqual(len(response), 0)
        for component in response.iteritems():
            self.assertEqual(component[0], component[1][1])


if __name__ == "__main__":
    unittest.main(verbosity = 2)

