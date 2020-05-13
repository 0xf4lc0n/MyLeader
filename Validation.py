class Validate:
    def __init__(self, cli_args, network_object, n_obj_name):
        self._args = cli_args
        self._network_object = network_object
        self._network_object_name = n_obj_name

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
            return 0

        elif self._args[1] in ['-h', '--help'] or number_of_arguments > 3:
            print("Usage: ")
            print(f"python3 {self._network_object_name}.py <server_ip_address> <port>\n")
            print("<server_ip_address>")
            print("\tMust be a valid ip address. If the ip address isn't specified localhost is used.\n")
            print("<port>")
            print("\tMust be a valid port in rage from 1024 to 65535. If the port isn't specified 8010 is used.")
            return 1

        elif number_of_arguments == 2:
            ip_octets = [self.check_octet(octet) for octet in self._args[1].split(".")]

            if len(ip_octets) != 4 or ip_octets[0] == 0:
                print("Given address is not valid")
                return 1

            self._network_object.Address = self._args[1]
            self._network_object.Port = 8010

            return 0

        elif number_of_arguments == 3:
            ip_octets = [self.check_octet(octet) for octet in self._args[1].split(".")]

            if len(ip_octets) != 4 or ip_octets[0] == 0:
                print("Given address is not valid")
                return 1

            if not (1024 <= self.to_int(self._args[2]) <= 65535):
                print("Giver port is not valid!")
                return 1

            self._network_object.Address = self._args[1]
            self._network_object.Port = self._args[2]

            return 0
