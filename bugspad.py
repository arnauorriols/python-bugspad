# Function temporal container waitting to be organized

from json import dumps
from requests import post


class Bug (object):
    
    def __init__(self, base_url, user, pwd, component_id, bug_id = None):
        self.bug_id = bug_id
        self.component_id = component_id
        self.url = base_url
        self.user = user
        self.pwd = pwd

    def retrieves_bug(funct):
        """
        Decorator for those functions which fetch or modifies existing bugs,
        thus requiring a bug_id. If Bug class is instantiated without bug_id
        the calling of these functions will raise an exception.

        """

        def inner(self, *args, **kwargs):
            if self.bug_id:
                return funct(self, *args, **kwargs)
            else:
                raise NameError ("Not callable without bug_id")

        return inner



    @retrieves_bug
    def add_comment (self, comment):
        """
        Adds a new comment for the given bug in the class' constructor.

        Returns server response, wether the new comment's id if succesful
        or an error message.

        """

        complete_url = "%s/comment/" % self.url

        json_data = {'user' : self.user,
                     'password' : self.pwd,
                     'desc' : comment,
                     'bug_id' : self.bug_id} # Doesn't it require component_id?

        request = post(complete_url, dumps(json_data))

        return request.text # ??



    def new_bug (self, summary, description):
        """
        Files a new bug for the component given in the class constructor.

        Returns server response, wether the new bug's id if succesful, or
        an error message.

        """


        complete_url = "%s/bug/" % self.url

        json_data = {'user' : self.user,
                     'password' : self.pwd,
                     'component_id' : self.component_id,
                     'summary' : summary,
                     'description' : description}

        request = post(complete_url, dumps(json_data))


        """
        **possibility:**

            return Bug(self.url, 
                       self.user, 
                       self.pwd, 
                       self.component_id, 
                       int(request.text))

        """

        return request.text # ??



    @retrieves_bug
    def update_bug(self, **kwargs):
        """
        Updates the bug given in the Bug constructor using 
        the given heyword arguments.

        Returns the server response, wether empty string if succesful or message.

        """

        complete_url = "%s/updatebug/" % self.url

        json_data = {'user' : self.user,
                     'password' : self.pwd,
                     'bug_id' : self.bug_id} # Doesn't it require component_id?

        json_data.update(kwargs)

        request = post(complete_url, dumps(json_data))

        ## FIXME: Should return info about db query succes.
        #  Right now only authentication failure is handled
        #  It also returns 'Wrong input' when there isn't 'status' key.
        #  Needs explanation, can't understand why. 

        return request.text # ??



    def get_component(self, product_id):
        """
        Fetches a component using it's id.

        Returns component id, name and description from the given id.

        """

        complete_url = "%s/components/" % self.url

        json_data = {'product_id' : product_id}
        request = post(complete_url, dumps(json_data))

        return request.text # ??
