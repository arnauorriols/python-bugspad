# Function temporal container waitting to be organized

from json import dumps
from requests import post


class Bug (object):
    
    def __init__(self, url, user, pwd, component_id, bug_id = None):
        if bug_id:
            self.bug_id = bug_id

        self.component_id = component_id
        self.url = url
        self.user = user
        self.pwd = pwd

    def retrieves_bug(self, funct):
        """
        Decorator for those functions which fetch or modifies existing bugs,
        thus requiring a bug_id. If Bug class is instantiated without bug_id
        the calling of these functions will raise an exception.

        """

        def inner(self, *args, **kwargs):
            if not self.bug_id:
                # TODO: Raise a proper exception
                raise NameError ("Not callable without bug_id")

            else:
                return funct(*args, **kwargs)

        return inner



    @retrieves_bug
    def add_comment (self, comment):
        """
        Adds a new comment for the given bug in the class' constructor.

        Returns server response, wether the new comment's id if succesful
        or an error message.

        """

        json_data = {'user' : self.usr,
                     'password' : self.pwd,
                     'desc' : comment,
                     'bug_id' : self.bug_id} # Doesn't it require component_id?

        request = post(self.url, dumps(json_data))

        return request.text # ??



    def new_bug (self, summary, description):
        """
        Files a new bug for the component given in the class constructor.

        Returns server response, wether the new bug's id if succesful, or
        an error message.

        """

        json_data = {'user' : self.usr,
                     'password' : self.pwd,
                     'component_id' : self.component_id,
                     'summary' : summary,
                     'description' : description}

        request = post(self.url, dumps(json_data))

        return request.text # ??



    @retrieves_bug
    def update_bug(self, **kwargs):
        """
        Updates the bug given in the Bug constructor using 
        the given heyword arguments.

        Returns the server response, wether succesful ('200') or
        an error message.

        """

        json_data = {'user' : self.usr,
                     'password' : self.pwd,
                     'bug_id' : self_bug_id} # Doesn't it require component_id?

        json_data.update(kwargs)

        request = post(self.url, dumps(json_data))

        return request.text # ??



    def get_component(self, product_id):
        """
        Returns component id, name and description from the given id.

        """

        json_data = {'product_id' : product_id}
        request = post(url, dumps(json_data))

        return request.text # ??
