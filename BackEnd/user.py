class ProfileData:
    """
    A class to store and manage profile data (username and location).
    """

    def __init__(self, username="", location=""):
        """
        Initializes the ProfileData object with optional username and location.
        """
        self._username = username
        self._location = location

    def set_username(self, username):
        """
        Sets the username.
        """
        self._username = username

    def get_username(self):
        """
        Gets the username.
        """
        return self._username

    def set_location(self, location):
        """
        Sets the location.
        """
        self._location = location

    def get_location(self):
        """
        Gets the location.
        """
        return self._location

    def set_profile(self, username, location):
        """
        Sets both the username and location.
        """
        self.set_username(username)
        self.set_location(location)

    def get_profile(self):
        """
        Gets both the username and location as a tuple.
        """
        return self.get_username(), self.get_location()

    def __str__(self):
        """
        Returns a string representation of the profile data.
        """
        return f"Username: {self.get_username()}, Location: {self.get_location()}"
