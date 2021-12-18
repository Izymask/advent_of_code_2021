import math

class Decoder:
    
    def __init__(self, path=None, data=None):
        if path:
            with open(path, 'r') as f:
                self.data = self.hex_str_to_binary(f.read().replace('\n', ''))
        else:
            self.data = data
            
    def get_result(self):
        main_packet, _junk = self.read_packets()
        return main_packet.total_versions, main_packet.get_value()

    def read_packets(self):
        data = self.data
        version = int(data[0:3], 2)
        packet_type = int(data[3:6], 2)
        if packet_type == 4:
            value = ''
            for i in range(6, len(data), 5):
                value += data[i + 1:i + 5]
                if data[i] == '0':
                    break
            value = int(value, 2)
            return LiteralValuePacket(version, packet_type, value), Decoder(data=data[i + 5:])
        length_type = data[6]
        subpackets = []
        if length_type == '0':
            length = int(data[7:22], 2)
            subpacket_decoder = Decoder(data=data[22:22 + length])
            while subpacket_decoder.data:
                subpacket, subpacket_decoder = subpacket_decoder.read_packets()
                subpackets.append(subpacket)
            data = data[22 + length:]
        else:
            length = int(data[7:18], 2)
            data = data[18:]
            for i in range(0, length):
                subpacket, subdecoder = Decoder(data=data).read_packets()
                subpackets.append(subpacket)
                data = subdecoder.data

        return (
            OperatorPacket(version, packet_type, length_type, length, subpackets),
            Decoder(data=data),
        )
        
    def hex_str_to_binary(self, str_to_convert):
        return ''.join(self.hex_char_to_binary(c) for c in str_to_convert)

    def hex_char_to_binary(self, char_to_convert):
        int_value = int(str(char_to_convert), base=16)
        binary_value = bin(int_value)
        return str(binary_value)[2:].zfill(4)
        
        
class Packet:
    def __init__(self, version, type_id):
        self.version = version
        self.type_id = type_id
        
        
class LiteralValuePacket(Packet):
    def __init__(self, version, type_id, value):
        super().__init__(version, type_id)
        self.value = value
    
    @property
    def total_versions(self):
        return self.version
        
    def get_value(self):
        return self.value
     
     
class OperatorPacket(Packet):
    def __init__(self, version, type_id, length_type, length, subpackets):
        super().__init__(version, type_id)
        self.length_type = length_type
        self.length = length
        self.subpackets = subpackets
        
    @property
    def total_versions(self):
        return sum([self.version, *[sp.total_versions for sp in self.subpackets]])
        
    def get_value(self):
        sp_values = [sp.get_value() for sp in self.subpackets]
        if self.type_id == 0:
            return sum(sp_values)
        if self.type_id == 1:
            return math.prod(sp_values)
        if self.type_id == 2:
            return min(sp_values)
        if self.type_id == 3:
            return max(sp_values)
        
        sp1_value, sp2_value = sp_values
        if self.type_id == 5:
            return 1 if sp1_value > sp2_value else 0
        if self.type_id == 6:
            return 1 if sp1_value < sp2_value else 0
        if self.type_id == 7:
            return 1 if sp1_value == sp2_value else 0
