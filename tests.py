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
        self.url = "http://127.0.0.1:9998"
        self.usr = "arnauorriolsmiro@gmail.com"
        self.pwd = "asdf"

        self.no_id_bug = Bug(self.url, self.usr, self.pwd, 1)
        self.with_id_bug = Bug(self.url, 
                               self.usr, 
                               self.pwd, 
                               1,
                               random.randint(1, 20))

        self.wrong_auth_bug = Bug(self.url, 
                                  "wrongusr", 
                                  self.pwd, 
                                  1, 
                                  random.randint(1, 20))




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



    def test_update_bug_returns_succes_response(self):
        response = self.with_id_bug.update_bug(status = "new", 
                                               hardware = "x86_64")

        self.assertEqual(response, self.SUCCESS)



    #@unittest.expectedFailure
    def test_update_bug_wrong_kwargs_returns_error_msg(self):

        response = self.with_id_bug.update_bug(wrong_kwarg = "dummy")

        self.assertNotEqual(response, self.SUCCESS)


if __name__ == "__main__":
    unittest.main(verbosity = 2)

