from unittest.mock import patch

from django.core.management import call_command
# Operation erro, django throws when the database is unavailable
# We'll use this error to simulates if the database is available
# or not when we run our command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        # simulates the beavior of django when the db is available,
        # try and retrieve the database connection,
        # it will retrieves a operation error if the database is not available,
        # if the operation error is not throw than the db is available
        # and the command will continue
        # will overwrite the behavior of the connection handler,
        # just make return true
        # uses patch to mochy the connection handler to
        # just return true everytime was called
        # mocky the behavior of the getitem function
        # overwriten with the and gi is a variable
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            # wait_for_db is the name of the command we created
            call_command('wait_for_db')
            # check if the getitem function is called once
            self.assertEqual(gi.call_count, 1)
    # try the database 5 times and the 6 time  will be sucusseful
    # wait a operation error 1 second and try again
    # this code above remove the delay using the @patch decorator is the same
    # passing the second argument "ts" in the function

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # Gonna raise the OperationError the first 5 times
            # on the 6 time wont' raise the error and return True
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
