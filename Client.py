import sys
import Validation
import ClientInterface

Interface = ClientInterface.ClientInterface()
Validation.Validate(sys.argv, Interface.Client)

while 1:
    Interface.Menu()
