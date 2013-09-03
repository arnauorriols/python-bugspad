# Python-Bugspad
# ==============
#
# Python front-end module using Bugspad API.
#
# ********************************************

from json import dumps, loads
from requests import post, get


class Bug (object):
    """
    Object that manages all bug manipulation. Requires a registered user
    and password as parameters; if the user is not registered, an
    'authentication failure' error message is return on every function.

    There are 2 forms in which this object can be instantiated.
        - Without bug_id: Can call only those generic functions which doesn't
          require a concrete bug representation. Those which require bug_id
          will raise a NameError exception when called without bug_id.

        - With bug_id: Represents a bug, thus apart from the functions
          available without bug_id, it allows those functions that manages
          a concrete bug, being able to update it, comment it...

    base_url refers to the base url of the server.

    """

    # This works as **kwargs filter
    OPTIONAL_KWARGS = ('priority',
                       'severity',
                       'status',
                       'hardware',
                       'whiteboard',
                       'fixedinver',
                       'version',
                       'component_id',
                       'subcomponent_id',
                       'emails')



    def __init__(self, base_url, user, pwd, bug_id = None):
        self.bug_id = bug_id
        self.url = base_url
        self.user = user
        self.pwd = pwd



    def requires_bug_id(funct):
        """
        Decorator for those functions which fetch or modifies existing bugs,
        thus requiring a bug_id. If Bug class is instantiated without bug_id
        the calling of these functions will raise a NameError exception.

        """

        def inner(self, *args, **kwargs):
            if self.bug_id:
                return funct(self, *args, **kwargs)
            else:
                raise NameError ("Not callable without bug_id")

        return inner



    def optional_args_filter(funct):
        """
        Decorator that filters optional keyword arguments, accepting only
        those data fields available in the Bugspad API:
            - severity
            - priority
            - status
            - version
            - hardware
            - whiteboard
            - fixedinver
            - component_id
            - subcomponent_id
            - emails

        Applicable to those functions which accepts arbitrary keyword
        arguments. If any of the keyword arguments added is not in
        OPTIONAL_KWARGS list, those functions will return "Wrong kwargs"
        string invariably.

        """

        def inner(self, *args, **kwargs):
            for arg in kwargs.keys():
                if arg not in self.OPTIONAL_KWARGS:
                    return "Wrong kwargs"

                # Server requires a list as 'emails' value
                if arg == 'emails' \
                and not isinstance(kwargs['emails'], (list, tuple)):
                    kwargs['emails'] = [kwargs['emails']]

            return funct(self, *args, **kwargs)

        return inner



    @requires_bug_id
    def add_comment (self, comment):
        """
        Adds a new comment to the bug, therefore requires an instance with
        bug_id provided.

        Returns server response, either the new comment's id if succesful
        or an error message. [WHICH?]

        """

        complete_url = "%s/comment/" % self.url

        json_data = {'user' : self.user,
                     'password' : self.pwd,
                     'desc' : comment,
                     'bug_id' : self.bug_id}

        request = post(complete_url, dumps(json_data))

        return request.text # ??



    @optional_args_filter
    def new_bug (self, summary, description, component_id, **kwargs):
        """
        Files a new bug for the component given in the class constructor.

        params: 
            - Summary, description and component_id are needed
            - kwargs are optional, and include:
                * priority
                * severity
                * status
                * version
                * hardware
                * witheboard
                * subcomponent_id
                * emails (list/tulpe?)

        Returns a new instance with the new bug's id, thus representing it
        and being able to modify it.

        """

        # FIND OUT WHAT ABOUT 'EMAILS' KEYWORD

        complete_url = "%s/bug/" % self.url

        json_data = {'user' : self.user,
                     'password' : self.pwd,
                     'component_id' : component_id,
                     'summary' : summary,
                     'description' : description}

        json_data.update(kwargs) # Adds optional args if any

        request = post(complete_url, dumps(json_data))

        return Bug(self.url,
                   self.user,
                   self.pwd,
                   int(request.text))



    @optional_args_filter
    @requires_bug_id
    def update_bug(self, **kwargs):
        """
        Updates the bug given in the Bug constructor using 
        the given heyword arguments.

        Returns the server response, wether empty string if succesful or message.

        """

        complete_url = "%s/updatebug/" % self.url

        json_data = {'user' : self.user,
                     'password' : self.pwd,
                     'bug_id' : self.bug_id} 

        json_data.update(kwargs)

        request = post(complete_url, dumps(json_data))

        return request.text # ??



    def get_components_list(self, product_id):
        """
        Fetches a components list from a product's id.

        Returns the components of the given product in a dict, where keys are
        component's name and values are a list containing id, name and
        description of each key.

        """

        complete_url = "%s/components/%s/" % (self.url, product_id)
        request = get(complete_url) 

        json_response = request.json
        return request.json



    def add_component(self, name, description, product_id):
        """
        Adds new component to the given product_id product. Requires 
        the name and description of the product. owner is thought to be the
        bug's user self. 

        Returns server response: if success, returns the new component's id, 
        Error message 'No such product' otherwise. 

        """

        complete_url = "%s/component/" % self.url
        json_data = {'user' : self.user,
                     'password' : self.pwd,
                     'owner' : self.user,
                     'name' : name,
                     'description' : description,
                     'product_id' : product_id}

        request = post(complete_url, dumps(json_data))

        return request.json



    def get_latest_created_bugs(self):
        """
        Fetches the 10 latest created bugs' id. 

        Returns a list containing these 10 bugs, as a dictionary containing
        bug's id, status and summary. This info can be used to create other 
        Bug instances with proper bug id.

        """

        complete_url = "%s/latestcreated/" % self.url
        request = get(complete_url)

        # Server's response is not well formed json data, needs to be
        # recursively parsed.
        # FIXME: Server's returns a list of string, not a list of json objects
        parsed_request = []
        for bug_string in request.json:
            parsed_request.append(loads(bug_string))

        return parsed_request



    def get_latest_updated_bugs(self):
        """
        Fetches the 10 latest updated bugs' id.

        Returns a list containing these 10 bugs, as a dictionary containing
        bug's id, status and summary.

        """

        complete_url = "%s/latestupdated/" % self.url
        request = get(complete_url)

        parsed_request = []
        for bug_string in request.json:
            parsed_request.append(loads(bug_string))

        return parsed_request



    def add_release(self, release_name):
        """
        Adds release to database, of which the name is provided in
        release_name parameter. Returns SUCCESS msg.
        
        """

        complete_url = "%s/releases/" % self.url
        json_data = {'user' : self.user,
                     'password' : self.pwd,
                     'name' : release_name}

        request = post(complete_url, dumps(json_data))

        return request.text



    def get_releases(self):
        """
        Fetches the releases list, and returns a list with all releases name
        as strings.

        """

        complete_url = "%s/releases/" % self.url
        request = get(complete_url)

        return request.json



    def add_product(self, product_name, product_description):
        """
        Adds new product to database, specifying name and description of it.

        Returns a dictionary containing id, name and description of the new
        added product.

        """

        complete_url = "%s/product/" % self.url
        json_data = {'user' : self.user,
                     'password' : self.pwd,
                     'name' : product_name,
                     'description' : product_description}

        request = post(complete_url, dumps(json_data))

        return request.json


    
    @requires_bug_id
    def add_bug_cc(self, *emails): # REVISE FUNCTION NAME
        """
        Adds cc users to the bug represented by the class instance. It admits
        either one email or many, as many parameters or in a single list/tuple.
        Must be a registered user email, otherwise it won't be
        added.

        Returns empty string.

        """

        # ASK KUSHAL IF POSSIBLE TO ADD SOME FEEDBACK WHEN SUCCEED OR ERROR

        complete_url = "%s/bug/cc" % self.url

        if isinstance(emails[0], (list, tuple)): # unpack if list is passed
            emails = emails[0]

        json_data = {'user' : self.user,
                     'password' : self.pwd,
                     'bug_id' : self.bug_id,
                     'action' : 'add',
                     'emails' : emails}

        request = post(complete_url, dumps(json_data))

        return request.text


    
    @requires_bug_id
    def remove_bug_cc(self, *emails):
        """
        Removes cc users from the bug represented by the class instance.
        Emails can be either a single email, or many mails, as many parameters
        or in a single list/tuple as the only parameter.

        Returns empty string.

        """

        complete_url = "%s/bug/cc" % self.url

        if isinstance(emails[0], (list, tuple)):
            emails = emails[0]

        json_data = {'user' : self.user,
                     'password' : self.pwd,
                     'bug_id' : self.bug_id,
                     'action' : 'remove',
                     'emails' : emails}

        request = post(complete_url, dumps(json_data))

        return request.text
