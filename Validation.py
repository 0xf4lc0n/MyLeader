class Validate:
    def __init__(self, cli_args, network_object):
        self._args = cli_args
        self._network_object = network_object
        self.validate()

    def to_int(self, value_to_check):
        try:
            return int(value_to_check)
        except ValueError:
            print("You have to input numbers!")
            exit(1)

    def check_octet(self, octet):
        octet = octet.strip()
        if 0 <= self.to_int(octet) <= 255:
            return int(octet)
        else:
            print("Given address is not valid")
            exit(1)

    def validate(self):
        number_of_arguments = len(self._args)

        if number_of_arguments == 1:
            self._network_object.Address = "127.0.0.1"
            self._network_object.Port = 8010

        elif number_of_arguments == 2:
            ip_octets = [self.check_octet(octet) for octet in self._args[1].split(".")]

            if len(ip_octets) != 4 or ip_octets[0] == 0:
                print("Given address is not valid")
                exit(1)

            self._network_object.Address = self._args[1]
            self._network_object.Port = 8010

        elif number_of_arguments == 3:
            ip_octets = [self.check_octet(octet) for octet in self._args[1].split(".")]

            if len(ip_octets) != 4 or ip_octets[0] == 0:
                print("Given address is not valid")
                exit(1)

            if not (1024 <= self.to_int(self._args[2]) <= 65535):
                print("Giver port is not valid!")
                exit(1)

            self._network_object.Address = self._args[1]
            self._network_object.Port = self._args[2]

        else:
            print("Usage: ")
            print("python Client.py <server_ip_address>\n")
            print("<server_ip_address>")
            print("\tMust be valid ip address. If ip address isn't specified localhost is used.")
            exit(0)
