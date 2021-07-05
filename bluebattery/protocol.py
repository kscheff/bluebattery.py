from flags import Flags

from . import conversions as cnv
from .commands import BBCommand, BBFrame, BBFrameTypeSwitch, BBValue, BBValueIgnore

SecFrame = BBFrame(output_id="sec", fields=[BBValue("i", "time_of_day_s")])


class Sec(BBCommand):
    """
    time of day in seconds, after power-up it starts with 0, needs to be set after initial connection to correct time.
    Log entry is generated when seconds reach 86400 (24 Hours) and seconds are reset to 0.
    """

    GATT_CHARACTERISTIC = "4b616901-40bd-428b-bf06-698e5e422cd9"
    READ = SecFrame
    WRITE = SecFrame


LogEntryDaysFrame = BBFrame(
    output_id="log/entry_day",
    fields=[
        # bytes 0-1: big endian 16 bit mWh per day**
        BBValue("H", "Wh_day", cnv.cnv_mW_to_W),
        # bytes 2-3: big endian 16-bit max mW per Day**
        BBValue("H", "max_W_day", cnv.cnv_mW_to_W),
        # bytes 4-5: big endian 16-bit min mV per Day
        BBValue("H", "min_V_day", cnv.cnv_mV_to_V),
        # bytes 6-7: big endian 16-bit max mV per Day
        BBValue("H", "max_V_day", cnv.cnv_mV_to_V),
        # bytes 8-9: big endian 16-bit charge time in minutes per Day**
        BBValue("H", "charge_minutes_day"),
        # bytes 10-11: big endian 16-bit day counter for this log entry, counting up from 0
        BBValue("H", "log_entry_day"),
        # bytes 12-13: big endian 16-bit current day (max day count)
        BBValue("H", "day_curent"),
        # bytes 14-15: big endian 16-bit Solar charge in 100 mAh**
        BBValue("H", "solar_charge_Ah", cnv.cnv_100mA_to_A),
        # bytes 16-17: big endian 16-bit SOC in 100 mAh
        BBValue("H", "state_of_charge_Ah", cnv.cnv_100mA_to_A),
        # bytes 18-19: big endian 16-bit max current 100 mA
        BBValue("H", "max_current_A", cnv.cnv_100mA_to_A),
        # bytes 20-21: big endian 16-bit min current -100 mA
        BBValue("H", "min_current_A", cnv.cnv_neg_100mA_to_A),
        # bytes 22-23: big endian 16-bit max SOC 100 mAh
        BBValue("H", "max_state_of_charge_Ah", cnv.cnv_100mA_to_A),
        # bytes 24-25: big endian 16-bit min SOC 100 mAh
        BBValue("H", "min_state_of_charge_Ah", cnv.cnv_100mA_to_A),
        # bytes 26-27: big endian 16-bit binary offset max Temperature (x - 0x8000) / 100 °C
        BBValue("H", "max_temperature_deg_C", cnv.cnv_bb_temp_to_deg_c),
        # bytes 28-29: big endian 16-bit binary offset min Temperature (x - 0x8000) / 100 °C
        BBValue("H", "min_temperature_deg_C", cnv.cnv_bb_temp_to_deg_c),
        # bytes 30-31: big endian 16-bit total external charge per day 100 mAh**
        BBValue("H", "total_external_charge_day_Ah", cnv.cnv_100mA_to_A),
        # bytes 32-33: big endian 16-bit total discharge per day 100 mAh
        BBValue("H", "total_discharge_Ah", cnv.cnv_100mA_to_A),
        # bytes 34-35: big endian 16-bit total charge per day 100 mAh
        BBValue("H", "total_charge_day_Ah", cnv.cnv_100mA_to_A),
        # byte 36: 8-bit frame type 0x00
        BBValueIgnore(),
        # bytes 37-38: big endian 16-bit total booster charge per day 100 mAh (V304)**
        BBValue("H", "total_booster_charge_day_Ah", cnv.cnv_100mA_to_A),
    ],
)

# available starting with Version V2xx, not anymore supported starting V306
LogEntryFrameOld = BBFrame(
    output_id="log/entry",
    fields=[
        # bytes 0-1: 16-bit day counter (relative to current day in frame type 0x00)
        BBValue("H", "log0_day_counter"),
        # bytes 2-3: 16-bit wall time in seconds/2
        BBValue("H", "log0_wall_time", lambda value: value * 2),
        # bytes 4-5: 16-bit average battery voltage mV
        BBValue("H", "log0_avg_battery_voltage_V", cnv.cnv_mV_to_V),
        # bytes 6-7: 16-bit average solar current mA
        BBValue("H", "log0_avg_solar_current_A", cnv.cnv_mA_to_A),
        # bytes 8: solar charger status: aktiv, standby, reduced
        BBValue("B", "log0_solar_charger_status", cnv.cnv_solar_status),
        # bytes 9-10: 16-bit average battery current 100 mA
        BBValue("H", "log0_avg_battery_current_A", cnv.cnv_100mA_to_A),
        # bytes 11-12: 16-bit battery SOC 100 mAh
        BBValue("H", "log0_battery_state_of_charge_A", cnv.cnv_mA_to_A),
        # bytes 13+ 0-1: 16-bit day counter (relative to current day in frame type 0x00)
        BBValue("H", "log0_day_counter"),
        # bytes 13+ 2-3: 16-bit wall time in seconds/2
        BBValue("H", "log0_wall_time", lambda value: value * 2),
        # bytes 13+ 4-5: 16-bit average battery voltage mV
        BBValue("H", "log0_avg_battery_voltage_V", cnv.cnv_mV_to_V),
        # bytes 13+ 6-7: 16-bit average solar current mA
        BBValue("H", "log0_avg_solar_current_A", cnv.cnv_mA_to_A),
        # bytes 13+ 8: solar charger status: aktiv, standby, reduced
        BBValue("B", "log0_solar_charger_status", cnv.cnv_solar_status),
        # bytes 13+ 9-10: 16-bit average battery current 100 mA
        BBValue("H", "log0_avg_battery_current_A", cnv.cnv_100mA_to_A),
        # bytes 13+ 11-12: 16-bit battery SOC 100 mAh
        BBValue("H", "log0_battery_state_of_charge_A", cnv.cnv_mA_to_A),
        # bytes 26-35: reserved
        BBValueIgnore(10),
        # byte 36: 8-bit frame type 0x01
        BBValueIgnore(),
    ],
)

LogEntryFrameNew = BBFrame(
    output_id="log/entry",
    fields=[
        # bytes 0-1: 16-bit day counter (relative to current day in frame type 0x00)
        BBValue("H", "log0_day_counter"),
        # bytes 2-3: 16-bit wall time in seconds/2
        BBValue("H", "log0_wall_time", lambda value: value * 2),
        # bytes 4-5: 16-bit average battery voltage mV
        BBValue("H", "log0_avg_battery_voltage_V", cnv.cnv_mV_to_V),
        # bytes 6-7: 16-bit average solar current mA
        BBValue("H", "log0_avg_solar_current_A", cnv.cnv_mA_to_A),
        # bytes 8: solar charger status: aktiv, standby, reduced
        BBValue("B", "log0_solar_charger_status", cnv.cnv_solar_status),
        # bytes 9-10: 16-bit average battery current 100 mA
        BBValue("H", "log0_avg_battery_current_A", cnv.cnv_100mA_to_A),
        # bytes 11-12: 16-bit battery SOC 100 mAh
        BBValue("H", "log0_battery_state_of_charge_A", cnv.cnv_mA_to_A),
        # bytes 13-14: 16-bit booster average input voltage 10mV (starter)**
        BBValue("H", "log0_avg_booster_input_voltage_V", cnv.cnv_10mV_to_V),
        # bytes 15-16: signed 16-bit booster average current 100 mA**
        BBValue("h", "log_avg_booster_current_A", cnv.cnv_100mA_to_A),
        # bytes 17+ 0-1: 16-bit day counter (relative to current day in frame type 0x00)
        BBValue("H", "log1_day_counter"),
        # bytes 17+ 2-3: 16-bit wall time in seconds/2
        BBValue("H", "log1_wall_time", lambda value: value * 2),
        # bytes 17+ 4-5: 16-bit average battery voltage mV
        BBValue("H", "log1_avg_battery_voltage_V", cnv.cnv_mV_to_V),
        # bytes 17+ 6-7: 16-bit average solar current mA
        BBValue("H", "log1_avg_solar_current_A", cnv.cnv_mA_to_A),
        # bytes 17+ 8: solar charger status: aktiv, standby, reduced
        BBValue("B", "log1_solar_charger_status", cnv.cnv_solar_status),
        # bytes 17+ 9-10: 16-bit average battery current 100 mA
        BBValue("H", "log1_avg_battery_current_A", cnv.cnv_100mA_to_A),
        # bytes 17+ 11-12: 16-bit battery SOC 100 mAh
        BBValue("H", "log1_battery_state_of_charge_A", cnv.cnv_mA_to_A),
        # bytes 17+ 13-14: 16-bit booster average input voltage 10mV (starter)**
        BBValue("H", "log1_avg_booster_input_voltage_V", cnv.cnv_10mV_to_V),
        # bytes 17+ 15-16: signed 16-bit booster average current 100 mA**
        BBValue("h", "log1_avg_booster_current_A", cnv.cnv_100mA_to_A),
        # bytes 34-35: reserved
        BBValueIgnore(2),
        # byte 36: 8-bit frame type 0x01
        BBValueIgnore(),
    ],
)


class Log(BBCommand):
    """
    Each read access auto increments the day counter until current day is reach, then it wraps around.
    Reading starts at day first available day.
    First all type 0x00 entries are send, then all type 0x01 frames etc.
    Note: Reading "sec" characteristics resets read pointer to earliest available log entry.
    """

    GATT_CHARACTERISTIC = "4b616907-40bd-428b-bf06-698e5e422cd9"
    READ = BBFrameTypeSwitch(
        "36xc",  # 36th byte is the frame type indicator
        {
            (0x00,): LogEntryDaysFrame,
            (0x01,): LogEntryFrameOld,
            (0x02,): LogEntryFrameNew,
        },
    )


BCLiveMeasurementsFrame = BBFrame(
    output_id="live/measurement",
    fields=[
        # byte 0: type
        # byte 1: length
        BBValueIgnore(2),
        # 2 bytes (17) value battery voltage in mV
        BBValue("H", "battery_voltage_V", cnv.cnv_mV_to_V),
        # 2 bytes (18) value solar charge current in 10mA**
        BBValue("H", "solar_charge_current_A", cnv.cnv_10mA_to_A),
        # 3 bytes (00) value Battery Current in mA
        BBValue("¾", "battery_current_A", cnv.cnv_mA_to_A),
    ],
)

BCSolarChargerEBLFrame = BBFrame(
    output_id="live/solar_charger_ebl",
    fields=[
        # byte 0: type
        # byte 1: length
        BBValueIgnore(2),
        # 2 bytes (09) value Solar max Current per day in mA
        BBValue("H", "max_solar_current_day_A", cnv.cnv_mA_to_A),
        # 2 bytes (10) value Solar max Watt per day in 1W
        BBValue("H", "max_solar_watt_day_W"),
        # 2 bytes (19) value solar charge in 10mAh (*)
        BBValue("H", "solar_current_A", cnv.cnv_10mA_to_A),
        # 2 bytes (20) value solar energy in Wh
        BBValue("H", "solar_energy_Wh"),
        # 1 byte (21) status solar charger (*) bit 7 indicates sleep
        BBValue("B", "solar_charger_status"),
    ],
)

BCSolarChargerStandardFrame = BBFrame(
    output_id="live/solar_charger",
    fields=BCSolarChargerEBLFrame.fields
    + [
        # 2 bytes (22) value solar PV module voltage in 10 mV (*)
        BBValue("H", "solar_module_voltage_V", cnv.cnv_10mV_to_V),
    ],
)


class RelayStatus(Flags):
    enabled = ()
    trigger_soc = ()
    trigger_board_voltage = ()
    trigger_starter_voltage = ()
    trigger_temperature = ()
    trigger_solar_current = ()
    trigger_time = ()
    reserved = ()


BCSolarChargerExtendedFrame = BBFrame(
    output_id="live/solar_charger_ext",
    fields=BCSolarChargerStandardFrame.fields
    + [
        # 1 byte  Relais Status (BB-X >= V407)
        #  bit 0: 0:off / 1:on
        #  bit 1: 1:SOC
        #  bit 2: 1:Board Voltage
        #  bit 3: 1:Starter Voltage
        #  bit 4: 1:Temperature
        #  bit 5: 1:Solar Current
        #  bit 6: 1:Time
        #  bit 7: reserved
        BBValue("B", "relay_status", RelayStatus),
    ],
)

BCBatteryComputer1Frame = BBFrame(
    output_id="live/battery_comp_1",
    fields=[
        # byte 0: type
        # byte 1: length
        BBValueIgnore(2),
        # 2 bytes (01) value Battery Charge in 10mAh (*)
        BBValue("H", "battery_charge_Ah", cnv.cnv_10mA_to_A),
        # 2 bytes (02) value SOC in 0.1% steps
        BBValue("H", "state_of_charge_percent", lambda x: x / 10),
        # 2 bytes (03) value Battery max Current per day in 10mA (*)
        BBValue("H", "max_battery_current_day_A", cnv.cnv_10mA_to_A),
        # 2 bytes (04) value Battery min Current per day in 10mA (*)
        BBValue("H", "min_battery_current_day_A", cnv.cnv_10mA_to_A),
        # 2 bytes (05) value Battery max Charge per day in 10mAh
        BBValue("H", "max_battery_charge_day_A", cnv.cnv_10mA_to_A),
        # 2 bytes (06) value Battery min Charge per day in 10mAh
        BBValue("H", "min_battery_charge_day_A", cnv.cnv_10mA_to_A),
        # 2 bytes (07) value Battery max Voltage per day in 10mV
        BBValue("H", "max_battery_voltage_day_V", cnv.cnv_10mV_to_V),
        # 2 bytes (08) value Battery min Volatge per day in 10mV
        BBValue("H", "min_battery_voltage_day", cnv.cnv_10mV_to_V),
    ],
)

BCBatteryComputer2Frame = BBFrame(
    output_id="live/battery_comp_2",
    fields=[
        # byte 0: type
        # byte 1: length
        BBValueIgnore(2),
        # 2 bytes (11) value Temperature in °C binary offset
        BBValue("H", "temperature_deg_C", cnv.cnv_bb_temp_to_deg_c),
        # 2 bytes (12) value min Temperature per day in °C binary offset
        BBValue("H", "min_temperature_deg_C", cnv.cnv_bb_temp_to_deg_c),
        # 2 bytes (13) value max Temperature per day in °C binary offset
        BBValue("H", "max_temperature_deg_C", cnv.cnv_bb_temp_to_deg_c),
        # 3 bytes (14) value summed total charge per day in 32/225 mAh (*)
        BBValue("¾", "total_charge_day_Ah", lambda x: (x / (32 / 225)) / 1000),
        # 3 bytes (15) value summed total discharge per day in 32/225 mAh (*)
        BBValue("¾", "total_discharge_day_Ah", lambda x: (x / (32 / 225)) / 1000),
        # 3 bytes (16) value summed total external charge per in 32/225 mAh (*)
        BBValue("¾", "total_external_charge_day_Ah", lambda x: (x / (32 / 225)) / 1000),
    ],
)

BCIntradayLogEntryFrame = BBFrame(
    output_id="live/intraday_log",
    fields=[
        # byte 0: type
        # byte 1: length
        BBValueIgnore(2),
        # byte 2: record #
        BBValue("B", "record_number"),
    ],
)

BCNoBoosterDataFrame = BBFrame(
    output_id="live/info",
    fields=[
        # byte 0: type
        # byte 1: length
        BBValueIgnore(2),
        # 2 bytes value output voltage in 10 mV (Board Battery)**
        BBValue("H", "battery_voltage_V", cnv.cnv_10mV_to_V),
        # 2 bytes value input voltage in 10 mV (Starter Battery)**
        BBValue("H", "starter_battery_voltage_V", cnv.cnv_10mV_to_V),
    ],
)

BCBoosterDataFrame = BBFrame(
    output_id="live/booster",
    fields=BCNoBoosterDataFrame.fields
    + [
        # 2 bytes signed value charge current in 100 mA (Booster current)
        BBValue("H", "booster_charge_current_A", cnv.cnv_100mA_to_A),
        # 1 byte status booster
        BBValue("B", "booster_status"),
        # 3 bytes value summed total booster charge per day in 256/18000 Ah
        BBValue("¾", "total_booster_charge_day_Ah", lambda x: x / (256 / 18000)),
    ],
)

BC = BBCommand(
    GATT_CHARACTERISTIC="4b616912-40bd-428b-bf06-698e5e422cd9",
    READ=BBFrameTypeSwitch(
        "BB",
        {
            # byte 0: type
            # byte 1: length
            (0x00, 0x07): BCLiveMeasurementsFrame,
            (0x01, 0x09): BCSolarChargerEBLFrame,
            (0x01, 0x0B): BCSolarChargerStandardFrame,
            (0x01, 0x0C): BCSolarChargerExtendedFrame,
            (0x02, 0x10): BCBatteryComputer1Frame,
            (0x03, 0x0F): BCBatteryComputer2Frame,
            (0x04, 0x01): BCIntradayLogEntryFrame,
            (0x05, 0x0A): BCBoosterDataFrame,
            (0x05, 0x04): BCNoBoosterDataFrame,
        },
    ),
)


SUBSCRIBE_CHARACTERISTICS = (BC,)