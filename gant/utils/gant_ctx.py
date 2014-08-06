from .gant_docker import GantDocker


class GantCtx:
    def __init__(self):
        self.gd = GantDocker()

    def fromFile(cls, confFile):
        pass

    def initConf(self, basetag, maintag, basedir, prefix, verbose):
        self.conf = GantConf(basetag, maintag, basedir, prefix, verbose)


class GantConf:
    def __init__(self, basetag, maintag, basedir, prefix, verbose):
        self.basetag = basetag
        self.maintag = maintag
        self.basedir = basedir
        self.prefix = prefix
        self.verbose = verbose
