##
## This file is part of the libsigrokdecode project.
##
## Copyright (C) 2020 Jorge Solla Rubiales <jorgesolla@gmail.com>
##
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in all
## copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
## SOFTWARE.

import sigrokdecode as srd
import struct
from common.srdhelper import SrdIntEnum
import enum

class OpCode(enum.IntEnum):
    GetStatus = 0xC0
    WriteRegister = 0x0D
    ReadRegister = 0x1D
    WriteBuffer = 0x0E
    ReadBuffer = 0x1E
    SetSleep = 0x84
    SetStandby = 0x80
    SetFS = 0xC1
    SetTx = 0x83
    SetRx = 0x82
    SetRxDutyCycle = 0x94
    SetCAD = 0xC5
    SetTxContinuousWave = 0xD1
    SetTxContinuousPremable = 0xD2
    SetPacketType = 0x8A
    GetPacketType = 0x11
    SetRFFrequency = 0x86
    SetTxParams = 0x8E
    SetPAConfig = 0x95
    SetCADParams = 0x88
    SetBufferBaseAddress = 0x8F
    SetModulationParams = 0x8B
    SetPacketParams = 0x8C
    GetRxBufferStatus = 0x13
    GetPacketStatus = 0x14
    GetRSSIInst = 0x15
    GetStats = 0x10
    ResetStats = 0x00
    SetDioIrqParams = 0x08
    GetIrqStatus = 0x12
    ClearIrqStatus = 0x02
    Calibrate = 0x89
    CalibrateImage = 0x98
    SetRegulatorMode = 0x96
    GetDeviceErrors = 0x17
    ClearDeviceErrors = 0x07
    SetDIO3AsTCXOCtrl = 0x97
    SetTxFallbackMode = 0x93
    SetDIO2AsRfSwitchCtrl = 0x9d
    SetStopRxTimerOnPreamble = 0x9F
    SetLoRaSymbTimeout = 0xA0,


class CommandStatus(enum.IntEnum):
    Reserved = 0x0
    RFU = 0x1
    DataAvailable = 0x2
    CommandTimeout = 0x3
    CommandProcessingError = 0x4
    FailureToExecuteCommand = 0x5
    CommandTxDone = 0x6


class ChipMode(enum.IntEnum):
    Unused = 0x0
    RFU = 0x1
    STBY_RC = 0x2
    STBY_XOSC = 0x3
    FS = 0x4
    RX = 0x5
    TX = 0x6


class StdbyConfig(enum.IntEnum):
    STDBY_RC = 0
    STDBY_XOSC = 1


class RegulatorMode(enum.IntEnum):
    OnlyLDO = 0
    DC_DC_LDO = 1

class TcxoVoltage(enum.IntEnum):
    Voltage_1_6 = 0x00
    Voltage_1_7 = 0x01
    Voltage_1_8 = 0x02
    Voltage_2_2 = 0x03
    Voltage_2_4 = 0x04
    Voltage_2_7 = 0x05
    Voltage_3_0 = 0x06
    Voltage_3_3 = 0x07

    def volt(self):
        if self == TcxoVoltage.Voltage_1_6:
            return 1.6
        if self == TcxoVoltage.Voltage_1_7:
            return 1.7
        if self == TcxoVoltage.Voltage_1_8:
            return 1.8
        if self == TcxoVoltage.Voltage_2_2:
            return 2.2
        if self == TcxoVoltage.Voltage_2_4:
            return 2.4
        if self == TcxoVoltage.Voltage_2_7:
            return 2.7
        if self == TcxoVoltage.Voltage_3_0:
            return 3.0
        if self == TcxoVoltage.Voltage_3_3:
            return 3.3


class CalibrationSetting(enum.Flag):
    RC64k = enum.auto()
    RC13M = enum.auto()
    PLL = enum.auto()
    ADC_pulse = enum.auto()
    ADC_bulk_N = enum.auto()
    ADC_bulk_P = enum.auto()
    Image = enum.auto()


class PacketType(enum.IntEnum):
    GFSK = 0
    LORA = 1


class Register(enum.IntEnum):
    PacketParams = 0x0704
    PayloadLength = 0x0702
    SynchTimeout = 0x0706
    Syncword = 0x06C0
    LoRaSyncword = 0x0740
    GeneratedRandomNumber = 0x0819
    AnaLNA = 0x08E2
    AnaMixer = 0x08E5
    RxGain = 0x08AC
    XTATrim = 0x0911
    OCP = 0x08E7
    RetentionList = 0x029F
    IQPolarity = 0x0736
    TxModulation = 0x0889
    TxClampCfg = 0x08D8
    RTCCtrl = 0x0902
    EvtClr = 0x0944


class IrqMask(enum.Flag):
    TxDone = enum.auto()
    RxDone = enum.auto()
    PreambleDetected = enum.auto()
    SyncWordValid = enum.auto()
    HeaderValid = enum.auto()
    HeaderErr = enum.auto()
    CrcErr = enum.auto()
    CadDone = enum.auto()
    CadDetected = enum.auto()
    Timeout = enum.auto()
    Unused1 = enum.auto()
    Unused2 = enum.auto()
    Unused3 = enum.auto()
    Unused4 = enum.auto()
    Unused5 = enum.auto()
    Unused6 = enum.auto()


class SleepModeStartConfig(enum.IntEnum):
    ColdStart = 0
    WarmStart = 1

class SleepModeTimeoutConfig(enum.IntEnum):
    RTCTimeoutDisable = 0
    RTCWakupOnTimeout = 1


class RampTime(enum.IntEnum):
    SET_RAMP_10 = 0
    SET_RAMP_20 = 1
    SET_RAMP_40 = 2
    SET_RAMP_80 = 3
    SET_RAMP_200 = 4
    SET_RAMP_800 = 5
    SET_RAMP_1700 = 6
    SET_RAMP_3400 = 7

    def ramp_time(self):
        if self == RampTime.SET_RAMP_10:
            return 10
        if self == RampTime.SET_RAMP_20:
            return 20
        if self == RampTime.SET_RAMP_40:
            return 40
        if self == RampTime.SET_RAMP_80:
            return 80
        if self == RampTime.SET_RAMP_200:
            return 200
        if self == RampTime.SET_RAMP_800:
            return 800
        if self == RampTime.SET_RAMP_1700:
            return 1700
        if self == RampTime.SET_RAMP_3400:
            return 3400


PA_DUTY_CYCLE_MAPPING = {
    (0x04, 0x07): "+22 dBm",
    (0x03, 0x05): "+20 dBm",
    (0x02, 0x03): "+17 dBm",
    (0x04, 0x06): "+14 dBm",
    (0x00, 0x03): "+10 dBm",
}

class LoraSF(enum.IntEnum):
    SF5 = 0x05
    SF6 = 0x06
    SF7 = 0x07
    SF8 = 0x08
    SF9 = 0x09
    SF10 = 0x0A
    SF11 = 0x0B
    SF12 = 0x0C


class LoraBW(enum.IntEnum):
    LORA_BW_7 = 0x00
    LORA_BW_10 = 0x08
    LORA_BW_15 = 0x01
    LORA_BW_20 = 0x09
    LORA_BW_31 = 0x02
    LORA_BW_41 = 0x0A
    LORA_BW_62 = 0x03
    LORA_BW_125 = 0x04
    LORA_BW_250 = 0x05
    LORA_BW_500 = 0x06

    def bandwidth(self):
        if self == self.LORA_BW_7:
            return 7.81
        if self == self.LORA_BW_10:
            return 10.42
        if self == self.LORA_BW_15:
            return 15.63
        if self == self.LORA_BW_20:
            return 20.83
        if self == self.LORA_BW_31:
            return 31.25
        if self == self.LORA_BW_41:
            return 41.67
        if self == self.LORA_BW_62:
            return 62.50
        if self == self.LORA_BW_125:
            return 125.0
        if self == self.LORA_BW_250:
            return 250.0
        if self == self.LORA_BW_500:
            return 500.0


class LoraCR(enum.IntEnum):
    LORA_CR_4_5 = 0x01
    LORA_CR_4_6 = 0x02
    LORA_CR_4_7 = 0x03
    LORA_CR_4_8 = 0x04


class LoraLowDataRateOptimize(enum.IntEnum):
    OFF = 0x00
    ON = 0x01


class LoraHeaderType(enum.IntEnum):
    VariableLength = 0
    FixedLength = 1

class LoraCrcType(enum.IntEnum):
   CRC_OFF = 0
   CRC_ON = 1

class LoraIqType(enum.IntEnum):
   Standard = 0
   Inverted = 1


Ann = SrdIntEnum.from_str('Ann', 'OPCODE COMMAND_STATUS CHIP_MODE READ WRITE REGISTER')

class Decoder(srd.Decoder):
    api_version = 3
    id = 'sx1262'
    name = 'SX1262'
    longname = 'Semtec SX1262'
    desc = '433MHz transceiver chip.'
    license = 'mit'
    inputs = ['spi']
    outputs = []
    tags = ['IC', 'Wireless/RF']

    annotations = (
        ('cmd', 'Command sent to the device'),
        ('command-status', 'Status of command'),
        ('chip-mode', 'Mode the chip is in'),
        ('read_data', 'Data read from the device'),
        ('written_data', 'Data sent to the device'),
        ('register', 'Register address'),
        # ('resp', 'Response to commands received from the device'),
        # ('warning', 'Warning'),
    )
    annotation_rows = (
        ('opcodes', 'Opcodes', (Ann.OPCODE,)),
        ('status', 'Status', (Ann.COMMAND_STATUS, Ann.CHIP_MODE)),
        ('write', 'Write', (Ann.WRITE, Ann.REGISTER)),
        ('read', 'Read', (Ann.READ, )),
        # ('registers', 'Registers', (Ann.REG_WR, Ann.REG_RD)),
        # ('tx', 'Transmitted data', (Ann.TX,)),
        # ('rx', 'Received data', (Ann.RX,)),
        # ('warnings', 'Warnings', (Ann.WARN,)),
    )

    def __init__(self):
        self.ss_cmd, self.es_cmd = 0, 0
        self.cs_asserted = False
        self._packet_type = None
        self.reset()

    def reset(self):
        self.mosi_bytes, self.miso_bytes = [], []
        self.cmd_samples = {'ss': 0, 'es': 0}

    def start(self):
        self.out_ann = self.register(srd.OUTPUT_ANN)

    def process_status(self, status):
        command_status = CommandStatus(status >> 1 & 0x7)
        chip_mode = ChipMode(status >> 4 & 0x7)
        self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                 self.out_ann, [Ann.CHIP_MODE, [chip_mode._name_]])
        self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                 self.out_ann, [Ann.COMMAND_STATUS, [command_status._name_]])

    def process_cmd(self):
        opcode = OpCode(self.mosi_bytes[0][0])
        # Report opcode if not reported in case
        if opcode not in [OpCode.ReadRegister, OpCode.WriteRegister]:
            self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                     self.out_ann, [Ann.OPCODE, [opcode._name_]])

        # Process all opcodes, I wish I had match
        if opcode == OpCode.GetStatus:
            self.process_status(self.miso_bytes[1][0])

        elif opcode == OpCode.SetStandby:
            standby_config = StdbyConfig(self.mosi_bytes[1][0])
            self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                     self.out_ann, [Ann.WRITE, [standby_config._name_]])

        elif opcode == OpCode.SetRegulatorMode:
            mode = self.mosi_bytes[1][0]
            self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                     self.out_ann, [Ann.WRITE, [RegulatorMode(mode)._name_]])

        elif opcode == OpCode.SetDIO2AsRfSwitchCtrl:
            mode = self.mosi_bytes[1][0]
            self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                     self.out_ann, [Ann.WRITE, ["enabled" if mode else "disabled"]])

        elif opcode == OpCode.ClearDeviceErrors:
            # The datasheet says we're receiving status bytes, but the
            # data I see (0xF0) isn't valid as such, so just don't process
            # anything.
            pass

        elif opcode == OpCode.SetDIO3AsTCXOCtrl:
            voltage = TcxoVoltage(self.mosi_bytes[1][0])
            timeout = (self.mosi_bytes[2][0] << 16 | self.mosi_bytes[3][0] << 8 | self.mosi_bytes[4][0]) * 15.625
            self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                     self.out_ann, [Ann.WRITE, [f"{voltage.volt()}V {timeout:0.2f}us"]])

        elif opcode == OpCode.Calibrate:
            calibration = CalibrationSetting(self.mosi_bytes[1][0])
            names = self._flag_enum_names(calibration, CalibrationSetting)
            self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                     self.out_ann, [Ann.WRITE, [names]])

        elif opcode == OpCode.SetPacketType:
            self._packet_type = PacketType(self.mosi_bytes[1][0])
            self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                     self.out_ann, [Ann.WRITE, [self._packet_type._name_]])

        elif opcode == OpCode.WriteRegister:
            register = self._mosi_16_bit_register(1)
            try:
                register = Register(register)._name_
            except ValueError:
                register = f"{register:04X}"
            self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                    self.out_ann, [Ann.OPCODE, [f"{opcode._name_}:{register}"]])
            payload = [mosi[0] for mosi in self.mosi_bytes[3:]]
            self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                     self.out_ann, [Ann.WRITE, [" ".join(f"0x{b:02X}" for b in payload)]])

        elif opcode == OpCode.ReadRegister:
            register = self.mosi_bytes[1][0] << 8 | self.mosi_bytes[2][0]
            try:
                register = Register(register)._name_
            except ValueError:
                register = f"{register:04X}"
            self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                    self.out_ann, [Ann.OPCODE, [
                        f"Read reg:{register}",
                        f"R:{register}"
                    ]])
            # The read register has to leave a gap of one
            # byte between asserting the address and then
            # receiving valid data - thus index 4!
            payload = [miso[0] for miso in self.miso_bytes[4:]]
            self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                     self.out_ann, [Ann.READ, [" ".join(f"0x{b:02X}" for b in payload)]])

        elif opcode == OpCode.SetBufferBaseAddress:
            tx_base_address, rx_base_address = self.mosi_bytes[1][0], self.mosi_bytes[2][0]
            self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                     self.out_ann, [
                         Ann.REGISTER,
                         [
                             f"tx_base_address: 0x{tx_base_address:02X} rx_base_address: 0x{rx_base_address:02X}",
                             f"0x{tx_base_address:02X} 0x{rx_base_address:02X}"
                         ]
                     ]
            )

        elif opcode == OpCode.CalibrateImage:
            freq1, freq2 = self.mosi_bytes[1][0], self.mosi_bytes[2][0]
            band = f"0x{freq1:02X}-0x{freq2:02X}"
            if (freq1, freq2) == (0x6b, 0x6f):
                band = "430 - 440"
            if (freq1, freq2) == (0x75, 0x81):
                band = "470 - 510"
            if (freq1, freq2) == (0xc1, 0xc5):
                band = "779 - 787"
            self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                     self.out_ann, [Ann.WRITE, [band]])

        elif opcode == OpCode.SetDioIrqParams:
            # We only have 10 IRQ sources
            irq_mask = self._flag_enum_names(IrqMask(self._mosi_16_bit_register(1) & 0x3ff), IrqMask)
            dio1_mask = self._flag_enum_names(IrqMask(self._mosi_16_bit_register(3) & 0x3ff), IrqMask)
            dio2_mask = self._flag_enum_names(IrqMask(self._mosi_16_bit_register(5) & 0x3ff), IrqMask)
            dio3_mask = self._flag_enum_names(IrqMask(self._mosi_16_bit_register(7) & 0x3ff), IrqMask)
            self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                     self.out_ann,
                     [Ann.WRITE,
                      [
                          f"irq_mask: {irq_mask} dio1_mask: {dio1_mask} "
                          f"dio2_mask: {dio2_mask} dio3_mask: {dio3_mask}",
                          # f"{irq_mask} {dio1_mask} "
                          # f"{dio2_mask} {dio3_mask}",
                      ]])

        elif opcode == OpCode.ClearIrqStatus:
            # We only have 10 IRQ sources
            clear_mask = self._flag_enum_names(IrqMask(self._mosi_16_bit_register(1) & 0x3ff), IrqMask)
            self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                     self.out_ann,
                     [Ann.WRITE,
                      [
                          clear_mask,
                      ]])

        elif opcode == OpCode.GetIrqStatus:
            # We only have 10 IRQ sources
            irq_mask = self._flag_enum_names(IrqMask(self._miso_16_bit_register(2) & 0x3ff), IrqMask)
            self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                     self.out_ann,
                     [Ann.READ,
                      [
                          irq_mask,
                      ]])

        elif opcode == OpCode.GetRSSIInst:
            rssi = self.miso_bytes[2][0]
            self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                     self.out_ann,
                     [Ann.READ,
                      [
                          f"{-rssi/2}dBm" ,
                      ]])

        elif opcode == OpCode.SetRFFrequency:
            freq = self._mosi_32_bit_register(1)
            if self._xtal_freq is not None:
                freq = f"{self._xtal_freq * freq / 2**25}"
            else:
                freq = f"{freq:04X}"
            self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                     self.out_ann,
                     [Ann.WRITE,
                      [
                       freq
                      ]])

        elif opcode == OpCode.SetSleep:
            config = self.mosi_bytes[1][0] & 0b101
            start_config = SleepModeStartConfig(config >> 2 & 1)
            timeout_config = SleepModeTimeoutConfig(config & 1)
            self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                     self.out_ann,
                     [Ann.WRITE,
                      [
                       f"{start_config._name_} {timeout_config._name_}",
                       f"{config:02X}",
                      ]])
        elif opcode == OpCode.SetTx:
            timeout = self._mosi_24_bit_register(1) * 15.625
            self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                     self.out_ann,
                     [Ann.WRITE,
                      [
                       f"{timeout:0.2f}us",
                      ]])
        elif opcode == OpCode.SetTxParams:
            power = struct.unpack("b", bytes([self.mosi_bytes[1][0]]))[0]
            ramp_time = RampTime(self.mosi_bytes[2][0])
            self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                     self.out_ann,
                     [Ann.WRITE,
                      [
                       f"power: {power}dBm ramp_time: {ramp_time.ramp_time():0.2f}us",
                       f"{power}dBm {ramp_time.ramp_time():0.2f}us",
                      ]])

        elif opcode == OpCode.WriteBuffer:
            offset = self.mosi_bytes[1][0]
            payload = " ".join([f"{b[0]:02X}" for b in self.mosi_bytes[2:]])
            self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                     self.out_ann,
                     [Ann.WRITE,
                      [
                       f"offset: {offset} payload: {payload}",
                       f"{offset} {payload}",
                      ]])

        elif opcode == OpCode.SetModulationParams:
            if self._packet_type is None:
                self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                         self.out_ann,
                         [Ann.WRITE,
                          [
                           f"<configuration error: packet_type not set>",
                           f"<error>"
                          ]])
            elif self._packet_type == PacketType.GFSK:
                self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                         self.out_ann,
                         [Ann.WRITE,
                          [
                           f"<todo: GFSK params>",
                           f"<todo>"
                          ]])
            elif self._packet_type == PacketType.LORA:
                sf = LoraSF(self.mosi_bytes[1][0])
                bandwidth = LoraBW(self.mosi_bytes[2][0])
                cr = LoraCR(self.mosi_bytes[3][0])
                ldro = LoraLowDataRateOptimize(self.mosi_bytes[4][0])

                self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                         self.out_ann,
                         [Ann.WRITE,
                          [
                           f"{sf._name_} {bandwidth.bandwidth():0.2f}kHz {cr._name_} {ldro._name_}",
                          ]])

        elif opcode == OpCode.SetPacketParams:
            if self._packet_type is None:
                self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                         self.out_ann,
                         [Ann.WRITE,
                          [
                           f"<configuration error: packet_type not set>",
                           f"<error>"
                          ]])
            elif self._packet_type == PacketType.GFSK:
                self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                         self.out_ann,
                         [Ann.WRITE,
                          [
                           f"<todo: GFSK packet params>",
                           f"<todo>"
                          ]])
            elif self._packet_type == PacketType.LORA:
                preamble_length = self._mosi_16_bit_register(1)
                header_type = LoraHeaderType(self.mosi_bytes[3][0])
                payload_length = self.mosi_bytes[4][0]
                crc_type = LoraCrcType(self.mosi_bytes[5][0])
                iq_type = LoraIqType(self.mosi_bytes[6][0])
                self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                         self.out_ann,
                         [Ann.WRITE,
                          [
                           f"preamble length: {preamble_length} {header_type._name_} payload length: {payload_length} {crc_type._name_} {iq_type._name_}",
                           f"{preamble_length} {header_type._name_} {payload_length} {crc_type._name_} {iq_type._name_}",
                          ]])
        elif opcode == OpCode.SetPAConfig:
            pa_duty_cycle = self.mosi_bytes[1][0]
            hp_max = self.mosi_bytes[2][0]
            device_sel = self.mosi_bytes[3][0]
            pa_lut = self.mosi_bytes[4][0]
            # Datasheet 13.1.14
            assert device_sel == 0 and pa_lut == 1
            pa_config = PA_DUTY_CYCLE_MAPPING.get(
                (pa_duty_cycle, hp_max),
                f"<unknown: {pa_duty_cycle:02X} {hp_max:02X}>"
            )
            self.put(self.cmd_samples['ss'], self.cmd_samples['es'],
                     self.out_ann,
                     [Ann.WRITE,
                      [
                          pa_config,
                          f"{pa_duty_cycle:02X} {hp_max:02X}"
                      ]])
        else:
            print("unhandled opcode:", opcode._name_)

    def _mosi_16_bit_register(self, offset):
        return self.mosi_bytes[offset][0] << 8 | self.mosi_bytes[offset + 1][0]

    def _mosi_24_bit_register(self, offset):
        return self.mosi_bytes[offset][0] << 16 | \
               self.mosi_bytes[offset + 1][0] << 8  | \
               self.mosi_bytes[offset + 2][0]

    def _mosi_32_bit_register(self, offset):
        return self.mosi_bytes[offset][0] << 24 | self.mosi_bytes[offset + 1][0] << 16 | \
               self.mosi_bytes[offset + 2][0] << 8 | self.mosi_bytes[offset + 3][0]

    def _miso_16_bit_register(self, offset):
        return self.miso_bytes[offset][0] << 8 | self.miso_bytes[offset + 1][0]

    def _flag_enum_names(self, flags, type_):
        # This is weird, used to be
        # ["|".join(c._name_ for c in calibration)]
        # but that's not supported in Python 3.6, even though
        # opossite claims of the documentation.
        names = []
        for m in type_:
            if flags & m:
                names.append(m.name)
        if not names:
            return "<empty>"
        return f"<{'|'.join(names)}>"

    def set_cs_status(self, sample, asserted):
        if self.cs_asserted == asserted:
            return

        if asserted:
            self.cmd_samples['ss'] = sample
            self.cmd_samples['es'] = -1
        else:
            self.cmd_samples['es'] = sample

        self.cs_asserted = asserted

    def decode(self, start_sample, end_sample, data):
        ptype, data1, data2 = data

        if ptype == 'CS-CHANGE':
            current_value = data2
            if data1 is None and current_value is None:
                self.requirements_met = False
                raise ChannelError('CS# pin required.')

            if data1 is None and current_value == 0:
                self.set_cs_status(start_sample, True)

            elif data1 is None and current_value == 1:
                self.set_cs_status(start_sample, False)

            elif data1 == 1 and current_value == 0:
                self.set_cs_status(start_sample, True)

            elif data1 == 0 and current_value == 1:
                self.set_cs_status(start_sample, False)
                if len(self.mosi_bytes):
                    try:
                        self.process_cmd()
                    finally:
                        self.reset()

        elif ptype == 'DATA':
            # Ignore traffic if CS is not asserted.
            if self.cs_asserted is False:
                return
            mosi, miso = data1, data2

            if miso is None or mosi is None:
                raise ChannelError('Both MISO and MOSI pins required.')

            self.mosi_bytes.append((mosi, start_sample, end_sample))
            self.miso_bytes.append((miso, start_sample, end_sample))

    @property
    def _xtal_freq(self):
        # After some digging I think the module
        # always requires a 32MHz oscillator,
        # the whole RC13/XOSC stuff seems to be
        # just for standby having lower power
        # draw vs. quicker switch-times keeping the
        # XOSC on.
        return 32_000_000
