from dataclasses import dataclass
from enum import Enum
from typing import Union
import inspect


@dataclass(frozen=True)
class PikoValue:
    name: str
    dxsNr: int
    unit: Union[str, Enum] = ''

    def format(self, value):
        unit = self.unit(value).name if inspect.isclass(self.unit) and issubclass(self.unit, Enum) else self.unit
        return f'{self.name:8s}= {value:g} {unit}'


class PikoStatus(Enum):
    Aus = 0
    Leerlauf = 1
    Anfahren = 2
    Einspeisen_MPP = 3
    abgeregelt = 4
    Einspeisen = 5


dc_u_1 = PikoValue('U DC 1', 33555202, 'V')
dc_i_1 = PikoValue('I DC 1', 33555201, 'A')
dc_p_1 = PikoValue('P DC 1', 33555203, 'W')

dc_u_2 = PikoValue('U DC 2', 33555458, 'V')
dc_i_2 = PikoValue('I DC 2', 33555457, 'A')
dc_p_2 = PikoValue('P DC 2', 33555459, 'W')

dc_u_3 = PikoValue('U DC 3', 33555714, 'V')
dc_i_3 = PikoValue('I DC 3', 33555713, 'A')
dc_p_3 = PikoValue('P DC 3', 33555715, 'W')

dc_p = PikoValue('P DC', 33556736, 'W')

ac_p = PikoValue('P AC', 67109120, 'W')

ac_cos_phi = PikoValue('cos φ', 67110656)
status = PikoValue('Status', 16780032, PikoStatus)
ac_freq = PikoValue('freq', 67110400, 'Hz')

ac_w_total = PikoValue('W AC (total)', 251658753, 'kWh')
ac_w_day = PikoValue('W AC (day)', 251658754, 'Wh')

all = [dc_u_1, dc_i_1, dc_p_1, dc_u_2, dc_i_2, dc_p_2, dc_u_3, dc_i_3, dc_p_3, dc_p, ac_p, ac_cos_phi, status, ac_freq,
       ac_w_total, ac_w_day]
