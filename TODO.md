Python client-side module.
==========================

    Python module to work with Bugspad like Python-bugzilla does with bugzilla


MANIFESTO
---------

    - fast
    - light
    - clear, easy to implement
    - Keep things clean from the very beginning
    - http://www.artima.com/weblogs/viewpost.jsp?thread=331531


~~1. Write functions~~
    - ~~Start with basic API functionalities~~

2. Organize code for easier readability
    - Group functions by functionality

3. Deepen into the test cases
    - Search for more assertions
    - Review each one and make sure they are axiomatic

4. Revise each function to match bugspad.go data options
    - Update WEB API doc if outdated
    - add_cc and remove_cc bugspad.go function is not finished, will need
      revision
    - new_bug has emails option to add cc users

TO-ASK
------

- Find out how does 'emails' keyword work in new_bug, and if it exist in others
- Add cc needs some kind of feedback, at least success or error messages
