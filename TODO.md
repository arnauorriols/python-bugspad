Python client-side module.
==========================

    Python module to work with Bugspad API like Python-bugzilla does with bugzilla


MANIFESTO
---------

    - fast
    - light
    - clear, easy to implement
    - Keep things clean from the very beginning
    - http://www.artima.com/weblogs/viewpost.jsp?thread=331531

TASKS
-----

~~1. Write functions~~
    - ~~Start with basic API functionalities~~

~~1. Improve/correct commentation~~

2. Organize code for easier readability
    - Group functions by functionality
    - Comply strictly with PEP 8 and PEP 257 style guidelines

3. Deepen into the test cases
    - Search for more assertions
    - Review each one and make sure they are axiomatic

4. Revise each function to match bugspad.go data options
    - Update WEB API doc if outdated
    - add_cc and remove_cc bugspad.go function is not finished, will need
      revision
    - new_bug has emails option to add cc users

5. Add new available functions

**Pending:** Comment out tests.py

TO-ASK
------

- Find out how does 'emails' keyword work in new_bug, and if it exist in others
- Add cc needs some kind of feedback, at least success or error messages
    - add_bug_cc requires list of emails. If only 1 email is provided, should
      it be converted in the python module or in server?

IDEAS
-----

- Add an authentication filter at instantation time.

SERVER FUNCTIONS NEEDED
-----------------------

- Create user?
- View Bug?
