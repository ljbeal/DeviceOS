from deviceos import Output, Device


class Network(Device):
    """
    Stub class for reporting the IP diagnostic

    Serves as an example for displaying static and diagnostic information
    """
    def __init__(self, ip):
        super().__init__(name="network", interval=86400)
        self.ip = ip
        self.interfaces = [Output(name="IP", icon="mdi:ip-network-outline", diagnostic=True)]

    def read(self):
        return {"IP": self.ip}
