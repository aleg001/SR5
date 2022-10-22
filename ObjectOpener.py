"""
Created by:
Alejandro Gomez

Features:
Loading an object from a file
Loads textures from file
Generate shader lightining
"""


import struct

"""
Class made to open an object from a file
"""


class ObjectOpener:
    def __init__(self, filename):
        with open(filename, "r") as file:
            self.lines = file.read().splitlines()
        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []
        self.glLines1()

    def glLines1(self):
        for line in self.lines:
            try:
                prefix, value = line.split(" ", 1)
            except:
                continue
            if prefix == "v":
                self.vertices.append(list(map(float, value.split(" "))))
            elif prefix == "f":
                self.faces.append(
                    [list(map(int, vert.split("/"))) for vert in value.split(" ")]
                )
            elif prefix == "vt":
                self.texcoords.append(list(map(float, value.split(" "))))
            elif prefix == "vn":
                self.normals.append(list(map(float, value.split(" "))))


"""
Class made to use a texture from a file
"""


class Texture(object):
    def __init__(self, filename):
        with open(filename, "rb") as file:
            file.seek(10)
            hS = struct.unpack("=l", file.read(4))[0]
            file.seek(18)
            self.width = struct.unpack("=l", file.read(4))[0]
            self.height = struct.unpack("=l", file.read(4))[0]
            file.seek(hS)
            self.pixels = []
            for y in range(self.height):
                cont = 0
                cont = cont + y
                pR = []
                for x in range(self.width):
                    cont1 = 0
                    cont1 = cont1 + x
                    b = ord(file.read(1)) / 255
                    g = ord(file.read(1)) / 255
                    r = ord(file.read(1)) / 255
                    pR.append([r, g, b])
                self.pixels.append(pR)

    def getColor(self, u, v):
        if 0 <= u <= 1:
            if 0 <= v <= 1:
                return self.pixels[int(v * self.height)][int(u * self.width)]
            else:
                return None


"""
Referencia:
https://j2logo.com/args-y-kwargs-en-python/
https://es.wikipedia.org/wiki/Sombreado_plano
https://graphics.fandom.com/wiki/Flat_shading
https://www.giantbomb.com/flat-shading/3015-2277/
https://cglearn.codelight.eu/pub/computer-graphics/shading-and-lighting
"""


class Shader:
    @staticmethod
    def flatShading(render, **kwargs) -> None:

        u, v, w = kwargs["baryCoords"]
        b, g, r = kwargs["colorU"]
        tA, tB, tC = kwargs["textureCoords"]
        tN = kwargs["triangleNormal"]

        b = b / 255
        g = g / 255
        r = r / 255

        if render.textureUsed:

            tempValue = tA[0] * u
            tempValue2 = tB[0] * v
            tempValue3 = tC[0] * w
            tempValue4 = tA[1] * u
            tempValue5 = tB[1] * v
            tempValue6 = tC[1] * w

            tU = tempValue + tempValue2 + tempValue3
            tV = tempValue4 + tempValue5 + tempValue6

            colorizarTextura = render.textureUsed.getColor(tU, tV)
            b *= colorizarTextura[2]
            g *= colorizarTextura[1]
            r *= colorizarTextura[0]

        luzDirecta = [render.luzDirecta.x, render.luzDirecta.y, render.luzDirecta.z]
        invertedLight = [(-i) for i in luzDirecta]

        result = 0
        for i in range(0, len(tN)):
            result += tN[i] * invertedLight[i]
        finalValue = result

        b *= finalValue
        g *= finalValue
        r *= finalValue

        if finalValue > 0:
            return r, g, b
        return 0, 0, 0
