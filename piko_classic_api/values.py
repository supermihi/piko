from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from numbers import Number
from typing import Any

"""
Zur Info.

//Leistungswerte
    ID_DCEingangGesamt = 33556736;         // in W
    ID_Ausgangsleistung = 67109120;        // in W
    ID_Eigenverbrauch = 83888128;          // in W
    //Status
    ID_Status = 16780032;                  // 0:Off
    //Statistik - Tag
    ID_Ertrag_d = 251658754;               // in Wh
    ID_Hausverbrauch_d = 251659010;        // in Wh
    ID_Eigenverbrauch_d = 251659266;       // in Wh
    ID_Eigenverbrauchsquote_d = 251659278; // in %
    ID_Autarkiegrad_d = 251659279;         // in %
    //Statistik - Gesamt
    ID_Ertrag_G = 251658753;               // in kWh
    ID_Hausverbrauch_G = 251659009;        // in kWh
    ID_Eigenverbrauch_G = 251659265;       // in kWh
    ID_Eigenverbrauchsquote_G = 251659280; // in %
    ID_Autarkiegrad_G = 251659281;         // in %
    ID_Betriebszeit = 251658496;           // in h
    //Momentanwerte - PV Genertor
    ID_DC1Spannung = 33555202;             // in V
    ID_DC1Strom = 33555201;                // in A
    ID_DC1Leistung = 33555203;             // in W
    ID_DC2Spannung = 33555458;             // in V
    ID_DC2Strom = 33555457;                // in A
    ID_DC2Leistung = 33555459;             // in W
    //Momentanwerte Haus
    ID_HausverbrauchSolar = 83886336;      // in W
    ID_HausverbrauchBatterie = 83886592;   // in W
    ID_HausverbrauchNetz = 83886848;       // in W
    ID_HausverbrauchPhase1 = 83887106;     // in W
    ID_HausverbrauchPhase2 = 83887362;     // in W
    ID_HausverbrauchPhase3 = 83887618;     // in W
    //Netz Netzparameter
    ID_NetzAusgangLeistung = 67109120;     // in W
    ID_NetzFrequenz = 67110400;            // in Hz
    ID_NetzCosPhi = 67110656;
    //Netz Phase 1
    ID_P1Spannung = 67109378;              // in V
    ID_P1Strom = 67109377;                 // in A
    ID_P1Leistung = 67109379;              // in W
    //Netz Phase 2
    ID_P2Spannung = 67109634;              // in V
    ID_P2Strom = 67109633;                 // in A
    ID_P2Leistung = 67109635;              // in W
    //Netz Phase 3
    ID_P3Spannung = 67109890;              // in V
    ID_P3Strom = 67109889;                 // in A
    ID_P3Leistung = 67109891;              // in W 
https://forum.fhem.de/index.php?PHPSESSID=ft1pbll7cqjpbhh7plp2l8slao&msg=677942  
"""


@dataclass(frozen=True)
class PikoValue:
    name: str
    dxsNr: int
    unit: str | None = None
    wire_data: tuple[str, int] | None = None
    parse: Callable[[float], Any] = lambda v: v

    @property
    def description(self):
        unit_suffix = '' if self.unit is None else f' (in {self.unit})'
        return f'{self.name.replace("_", " ")}{unit_suffix}'

    @property
    def full_name(self):
        if self.wire_data is None:
            return self.name

        wire_name, value = self.wire_data
        return f'{self.name}_{wire_name}_{value}'

    def format(self, value):
        fmt_value = f'{value:g}' if isinstance(value, Number) else value
        return f'{self.full_name:16s} = {fmt_value} {self.unit or ""}'


class PikoStatus(Enum):
    Aus = 0
    Leerlauf = 1
    Anfahren = 2
    Einspeisen_MPP = 3
    abgeregelt = 4
    Einspeisen = 5


def per_wire(name: str, unit: str | None, wire_label: str, dxs_wire_1: int, dxs_wire_2: int, dxs_wire_3: int) -> tuple[
    PikoValue, PikoValue, PikoValue]:
    p1, p2, p3 = [PikoValue(name, dxs, unit, wire_data=(wire_label, i)) for i, dxs in
                  enumerate([dxs_wire_1, dxs_wire_2, dxs_wire_3], start=1)]
    return p1, p2, p3


dc_input_voltage = per_wire('DC_voltage', 'U', 'input', 33555202, 33555458, 33555714)
dc_input_current = per_wire('DC_current', 'I', 'input', 33555201, 33555457, 33555713)
dc_input_phase = per_wire('DC_power', 'W', 'input', 33555203, 33555459, 33555715)

dc_power_total = PikoValue('DC_power_total', 33556736, 'W')

ac_power_total = PikoValue('AC_power_total', 67109120, 'W')

ac_phase_power = per_wire('AC_power', 'W', 'phase', 67109379, 67109635, 67109891)
ac_phase_current = per_wire('AC_current', 'A', 'phase', 67109377, 67109633, 67109889)
ac_phase_voltage = per_wire('AC_voltage', 'V', 'phase', 67109378, 67109634, 67109890)

ac_cos_phi = PikoValue('cos_phi', 67110656)
status = PikoValue('status', 16780032, parse=PikoStatus)
ac_frequency = PikoValue('frequency', 67110400, 'Hz')

ac_energy_total = PikoValue('AC_energy_total', 251658753, 'kWh')
ac_energy_day = PikoValue('AC_energy_day', 251658754, 'Wh')
operating_time = PikoValue('operating_time', 251658496, 'h')

ALL_VALUES = [*dc_input_voltage, *dc_input_current, *dc_input_phase, dc_power_total, *ac_phase_voltage, *ac_phase_power,
              *ac_phase_current, ac_power_total,
              ac_cos_phi, status, ac_frequency,
              ac_energy_total, ac_energy_day,
              operating_time]
