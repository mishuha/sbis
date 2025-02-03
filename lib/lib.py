# -*- coding: utf-8 -*-
import platform


def get_OS() -> [str, str]:
    system, release = platform.system(),  platform.release()
    return system, release


def str2float(row: str):
    return float(row.replace(',', '.'))


def byte2Mbyte(n: float):
    return n / (1 << 20)

