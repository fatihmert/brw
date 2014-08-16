#-*- coding: utf-8 -*-

import struct, re
import sys

# Author:           Fatih Mert DOĞANCAN
# Github:           fatihmert
# Mail:             fatihmertdogancan@hotmail.com
# Release:          16.08.2014
# Version:          0.1 (First)

class brw:
    def __init__(self,dosya,mod):
        self.ctypes = {
        "pad byte":'x',"bool":'?', #_Bool
        "char":'c',"signed char":'b',"schar":"b","uchar":"B","unsigned char":'B',
        "short":'h',"unsigned short":'H',"ushort":"H","int":'i',"unsigned int":'I',
        "uint":"I","ulong":"L","ll":"q","LL":"q","ull":"Q","uLL":"Q","ULL":"Q",
        "long":'l',"unsigned long":'L',"long long":'q',"unsigned long long":'Q',"dobule":"d",
        "void":"P"}
        self.memread = {
        "native":"@",
        "n":"@",
        "sn":"@",
        "snative":"=", #standart native
        "standart native":"=",
        "little-endian":"<", #günümüz bilgisayarlarının kullandığı okuma  yöntemi
        "le":"<",
        "big-endian":">",
        "be":">",
        "nw":"!",
        "network":"!"}
        #self.strL = 0 #stringLength
        self.getSeek = 0
        self.mod = mod
        self.dosya = dosya
        if self.mod == "wb" or self.mod == "rb":
            self.mod = mod
        elif self.mod == "pack":
            self.mod = "wb"
        elif self.mod == "unpack":
            self.mod = "rb"
        self.obj = open(self.dosya,self.mod)
        self.memo = "<" #little endian
        self.structString = ""

    def setMem(self,setString):
        """
        string*
        native -> @
        n -> @
        standart native -> =
        sn -> @
        snative -> =
        little-endian -> < #günümüz bilgisayarlarının kullandığı okuma yöntemi(varsayılandır)
        le -> <
        big-endian -> >
        be -> >
        network -> !
        nw -> !

        ya da

        direk olarak sembolleri kullanın, app.setMem("<") gibi
        """
        try:
            if self.memread[setString]:
                self.memo = self.memread
            elif {v:k for k, v in self.memread.items()}[setString]:
                self.memo = setString
        except:
            pass


    def getType(self,sr):
        """
        string*
        char -> s
        char[] -> s
        string -> s
        char[n] -> ns
        bool -> ?
        signed char -> b
        schar -> b
        unsigned char -> B
        uchar -> B
        short -> h
        unsigned short -> H
        ushort -> H
        int -> i
        unsigned int -> I
        uint -> I
        long -> l
        unsigned long -> L
        ulong -> L
        long long -> q
        ll -> q
        LL -> q
        unsigned long long -> Q
        ull -> Q
        uLL -> Q
        ULL -> Q
        dobule -> d
        void -> P
        """
        stringRE = re.search('\[([0-9]+)?\]',sr)

        try:
            strLen = stringRE.group(1)
            #return len(str)
            if len(sr) > 6:
                if strLen in ("0","1"):
                    return "s"
                return "%ss"%strLen
            elif len(sr) in (4,6):
                return "s"
            else:
                return "s"
            #return "KEY: %s :: KOSELI: %s :: LEN: %u"%(key,koseli,koseliNo)

        except:
            #raise "UNKNOWN C-TYPE"
            #return sys.exc_info()[:2]
            try:
                return self.ctypes[sr]
            except KeyError as err:
                if str(err) == "'string'":
                    return "s"
                #raise "UNKNOWN C-TYPE"

    def _seek(self,clc):
        """
        void*
        calc(getType(byte)) değeri işler,
        sınıf kendi kullanıyor, return olmadığından kullanışlı değildir
        """
        self.getSeek += clc
        self.obj.seek(self.getSeek)


    def calc(self,byte):
        """
        string*
        Girdiğiniz değer tiplerinin bellekte kapladığı byte'ı döndürür.
        """
        return int(struct.calcsize("{}".format(self.getType(byte))))

    def bilgi(self):
        return "Dosya adı: %s\nDosyanın modu: %s\nMemory: %s\nSeek: %s"%(self.dosya,self.mod,self.memo,self.getSeek)

    def pack(self,byte,io):
        #self.mod = "wb"
        self.structString = self.memo + self.getType(byte)
        self.obj.write(struct.pack(self.structString,io))
        self._seek(self.calc(byte))

    def unpack(self,byte):
        self.structString = self.memo + self.getType(byte)
		#tek tek okuttuğumuz için demetin ilk değerini almamız gerekiyor
        ret = struct.unpack(self.structString,self.obj.read(self.calc(byte)))[0] #demetin ilk değeri
        self._seek(self.calc(byte))
        return ret

    def close(self):
        self.obj.close()

    def __enter__(self):
        return self

    def __exit__(self,v1,v2,v3):
        self.obj.close()


if __name__ == "__main__":
    with brw("yeni.fmd","pack") as fmdFile:
        print fmdFile.bilgi()
        try:
            fmdFile.pack('char[7]',"istihza")
            fmdFile.pack('int',112323)
            fmdFile.pack('uint',1112323)
            fmdFile.pack('char[7]',"kapandi")
        except:
            print sys.exc_info()[:2]

    with brw("yeni.fmd","unpack") as fmdOpen:
        try:
            print fmdOpen.unpack('char[7]') #istihza
            print fmdOpen.unpack('int') #112323
            print fmdOpen.unpack('int') #1112323
            print fmdOpen.unpack('char[5]') #kapan
        except:
            print sys.exc_info()[:2]



