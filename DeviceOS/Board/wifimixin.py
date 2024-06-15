"""
Mixin class providing wifi functionality
"""
import time
import network  # pylint: disable=import-error

from machine import Pin  # pylint: disable=import-error


class WiFiMixin:
    """
    Adds wifi related functions

    expects an ssid and password at _wlan_ssid and _wlan_pass
    """

    __slots__ = [
        "_wlan",
        "_wlan_ssid",
        "_wlan_pass",
        ]

    @property
    def wlan(self) -> network.WLAN:
        """Returns the internal wlan object"""
        if not hasattr(self, "_wlan"):
            return None
        return self._wlan

    def connect_to_wifi(self) -> None:
        """
        Create wifi object and attempt to connect
        """
        self._wlan = network.WLAN(network.STA_IF)

        self.wlan.active(True)
        self.wlan.connect(self._wlan_ssid, self._wlan_pass)

        led = Pin("LED", Pin.OUT)

        led_orig_state = led.value()

        try:
            led.on()
            n_ellipses = 0
            max_ellipses = 3
            while not self.has_wifi:
                n_ellipses += 1
                if n_ellipses > max_ellipses:
                    n_ellipses = 1
                print(
                    "Waiting for WiFi connection" + "." * n_ellipses,
                    end=" " * max_ellipses + "\r",
                )
                led.toggle()

                time.sleep(0.5)
        except Exception as ex:
            print(f"Waiting for WiFi connection... Error:\n{str(ex)}")
        else:
            print("Waiting for WiFi connection... Done.")
        finally:
            led.value(led_orig_state)

    def wifi_off(self) -> None:
        """Disconnect and disable wifi chip to save power"""
        self.wlan.deinit()
        self._wlan = None

    def wifi_on(self) -> None:
        """Alias to reconnect after calling wifi_off"""
        self.connect_to_wifi()

    @property
    def has_wifi(self) -> bool:
        """Returns True if there is a valid, functional WiFi connection"""
        return (
            self.wlan is not None
            and self.wlan.isconnected()
            and self.wlan.status() >= 0
        )

    @property
    def ip(self) -> None | str:
        """Returns the current ip address, None if there is no connection."""
        if not self.has_wifi:
            return None
        return self.wlan.ifconfig()[0]

    @property
    def DNS(self) -> None | str:
        """Returns the address of the DNS server, None if there is no connection."""
        if not self.has_wifi:
            return None
        return self.wlan.ifconfig()[3]

    @property
    def hostname(self) -> None | str:
        """Returns the defined hostname, None if there is no connection."""
        if not self.has_wifi:
            return None
        return network.hostname()
