import primative

class PacketSerializer(object):

    def serialize(self, packet):
        b = bytearray()
        primative.w_vi(b, self.id)
        for f in self.fields:
            f[1][1](b, getattr(packet, f[0]))

        return b

    def deserialize(self, b):
        d = dict()
        for f in self.fields:
            d[f[0]] = f[1][0](b)

        new = self.new if hasattr(self, "new") else lambda **kwargs: self.type(**kwargs)

        return new(**d)
