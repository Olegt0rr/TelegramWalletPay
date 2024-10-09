from ipaddress import IPv4Address, IPv4Network
from typing import Union

import pytest
from telegram_wallet_pay.tools.ip_filter import DEFAULT_WALLET_WEBHOOK_IPS, IPFilter


def test_default_init() -> None:
    ip_filter = IPFilter()
    for ip in DEFAULT_WALLET_WEBHOOK_IPS:
        assert ip_filter.check(ip)


@pytest.mark.parametrize(
    ("ip", "result"),
    [
        ("127.0.0.1", True),
        ("127.0.0.2", False),
        (IPv4Address("127.0.0.1"), True),
        (IPv4Address("127.0.0.2"), False),
        (IPv4Address("192.168.0.32"), True),
        ("192.168.0.33", False),
        ("10.111.0.5", True),
        ("10.111.0.100", True),
        ("10.111.1.100", False),
    ],
)
def test_check_ip(ip: Union[str, IPv4Address], result: bool) -> None:
    ip_filter = IPFilter(
        ips=[
            "127.0.0.1",
            IPv4Address("192.168.0.32"),
            IPv4Network("10.111.0.0/24"),
        ],
    )
    assert (ip in ip_filter) is result


@pytest.mark.parametrize(
    ("ip", "ip_range"),
    [
        ("127.0.0.1", {IPv4Address("127.0.0.1")}),
        ("91.108.4.0/22", set(IPv4Network("91.108.4.0/22").hosts())),
        (IPv4Address("91.108.4.5"), {IPv4Address("91.108.4.5")}),
        (IPv4Network("91.108.4.0/22"), set(IPv4Network("91.108.4.0/22").hosts())),
    ],
)
def test_allow_ip(ip: str, ip_range: set[IPv4Address]) -> None:
    ip_filter = IPFilter([])
    ip_filter.allow_ip(ip)
    assert ip_filter._allowed_ips == ip_range


def test_allow_wrong_ip() -> None:
    ip_filter = IPFilter([])
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        ip_filter.allow_ip(42)
