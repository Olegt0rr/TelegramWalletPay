"""Webhook IP security module.

Inspired by aiogram's webhook security module:
https://github.com/aiogram/aiogram

Docs:
https://docs.wallet.tg/pay/#operation/completedOrder
"""

from collections.abc import Sequence
from ipaddress import IPv4Address, IPv4Network
from typing import Any, Union

DEFAULT_WALLET_WEBHOOK_IPS = (
    IPv4Address("172.255.248.29"),
    IPv4Address("172.255.248.12"),
)


class IPFilter:
    """Tool for adding and checking allowed IP addresses."""

    def __init__(
        self,
        ips: Sequence[
            Union[str, IPv4Network, IPv4Address]
        ] = DEFAULT_WALLET_WEBHOOK_IPS,
    ) -> None:
        self._allowed_ips: set[IPv4Address] = set()

        if ips:
            self.allow_ip(*ips)

    def allow_ip(self, *ips: Union[str, IPv4Network, IPv4Address]) -> None:
        """Add IP or network to allowed list."""
        for ip in ips:
            ip_list = self._convert_ips(ip)
            self._allowed_ips.update(ip_list)

    def check(self, ip: Union[str, IPv4Address]) -> bool:
        """Check IP is allowed."""
        if not isinstance(ip, IPv4Address):
            ip = IPv4Address(ip)
        return ip in self._allowed_ips

    def __contains__(self, item: Union[str, IPv4Address]) -> bool:
        """Check IP is in allowed list."""
        return self.check(item)

    @staticmethod
    def _convert_ips(ip: Any) -> list[IPv4Address]:  # noqa: ANN401
        """Convert passed data to IP list."""
        if isinstance(ip, str):
            ip = IPv4Network(ip) if "/" in ip else IPv4Address(ip)

        if isinstance(ip, IPv4Address):
            return [ip]

        if isinstance(ip, IPv4Network):
            return list(ip.hosts())

        msg = f"Invalid type of IP address: {type(ip)} ('{ip}')"
        raise TypeError(msg)
