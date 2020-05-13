import sys
import Validation
import ClientInterface


Interface = ClientInterface.ClientInterface()
validator = Validation.Validate(sys.argv, Interface.Client, "Client")
validation_code = validator.validate()

if validation_code == 0:
    while 1:
        Interface.Menu()
