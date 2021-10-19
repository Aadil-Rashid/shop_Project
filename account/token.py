from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    
    # Now we have a function to generate the actual hash value that we are going to send across, for authenticate
    # the user and then activate the user on the system

    def _make_hash_value(self, user, timestamp):
        return ( text_type(user.pk) + text_type(timestamp) + text_type(user.is_active) )


# we can access this facility for this variable: account_activation_token
account_activation_token = AccountActivationTokenGenerator()
