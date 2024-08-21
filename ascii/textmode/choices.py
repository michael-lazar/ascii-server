from django.db import models


class TagCategory(models.TextChoices):
    ARTIST = "artist", "Artist"
    CONTENT = "content", "Content"
    GROUP = "group", "Group"


class LetterSpacing(models.IntegerChoices):
    """
    SAUCE letter spacing.
    """

    LEGACY = 0, "No Preference"
    EIGHT = 1, "8 pixel"
    NINE = 2, "9 pixel"


class AspectRatio(models.IntegerChoices):
    """
    SAUCE aspect ratio.
    """

    LEGACY = 0, "No Preference"
    STRETCH = 1, "Stretch"
    SQUARE = 2, "Square"


class DataType(models.IntegerChoices):
    """
    SAUCE data type.
    """

    NONE = 0, "None"
    CHARACTER = 1, "Character"
    BITMAP = 2, "Bitmap"
    VECTOR = 3, "Vector"
    AUDIO = 4, "Audio"
    BINARYTEXT = 5, "BinaryText"
    XBIN = 6, "XBin"
    ARCHIVE = 7, "Archive"
    EXECUTABLE = 8, "Executable"


class FileType(models.TextChoices):
    """
    SAUCE file type.
    """

    NONE = "None", "None"
    ASCII = "ASCII", "ASCII"
    ANSI = "ANSi", "ANSi"
    ANSIMATION = "ANSiMation", "ANSiMation"
    RIPSCRIPT = "RIP script", "RIP script"
    PCBOARD = "PCBoard", "PCBoard"
    AVATAR = "Avatar", "Avatar"
    HTML = "HTML", "HTML"
    SOURCE = "Source", "Source"
    TUNDRADRAW = "TundraDraw", "TundraDraw"
    GIF = "GIF", "GIF"
    PCX = "PCX", "PCX"
    LBM = "LBM/IFF", "LBM/IFF"
    TGA = "TGA", "TGA"
    FLI = "FLI", "FLI"
    FLC = "FLC", "FLC"
    BMP = "BMP", "BMP"
    GL = "GL", "GL"
    DL = "DL", "DL"
    WPGBITMAP = "WPG Bitmap", "WPG Bitmap"
    PNG = "PNG", "PNG"
    JPG = "JPG/JPeg", "JPG/JPeg"
    MPG = "MPG", "MPG"
    AVI = "AVI", "AVI"
    DXF = "DXF", "DXF"
    DWG = "DWG", "DWG"
    WPGVECTOR = "WPG Vector", "WPG Vector"
    THREEDS = "3DS", "3DS"
    MOD = "MOD", "MOD"
    SIXSIXNINE = "669", "669"
    STM = "STM", "STM"
    S3M = "S3M", "S3M"
    MTM = "MTM", "MTM"
    FAR = "FAR", "FAR"
    ULT = "ULT", "ULT"
    AMF = "AMF", "AMF"
    DMF = "DMF", "DMF"
    OKT = "OKT", "OKT"
    ROL = "ROL", "ROL"
    CMF = "CMF", "CMF"
    MID = "MID", "MID"
    SADT = "SADT", "SADT"
    VOC = "VOC", "VOC"
    WAV = "WAV", "WAV"
    SMP8 = "SMP8", "SMP8"
    SMP8S = "SMP8S", "SMP8S"
    SMP16 = "SMP16", "SMP16"
    SMP16S = "SMP16S", "SMP16S"
    PATCH8 = "PATCH8", "PATCH8"
    PATCH16 = "PATCH16", "PATCH16"
    XM = "XM", "XM"
    HSC = "HSC", "HSC"
    IT = "IT", "IT"
    BINARYTEXT = "binary", "binary"
    XBIN = "XBin", "XBin"
    ZIP = "ZIP", "ZIP"
    ARJ = "ARJ", "ARJ"
    LZH = "LZH", "LZH"
    ARC = "ARC", "ARC"
    TAR = "TAR", "TAR"
    ZOO = "ZOO", "ZOO"
    RAR = "RAR", "RAR"
    UC2 = "UC2", "UC2"
    PAK = "PAK", "PAK"
    SQZ = "SQZ", "SQZ"
    EXECUTABLE = "executable", "executable"


CHARACTER_FILETYPES = [
    FileType.ASCII,
    FileType.ANSI,
    FileType.ANSIMATION,
    FileType.RIPSCRIPT,
    FileType.PCBOARD,
    FileType.AVATAR,
    FileType.HTML,
    FileType.SOURCE,
]

BITMAP_FILETYPES = [
    FileType.GIF,
    FileType.PCX,
    FileType.LBM,
    FileType.TGA,
    FileType.FLI,
    FileType.FLC,
    FileType.BMP,
    FileType.GL,
    FileType.DL,
    FileType.WPGBITMAP,
    FileType.PNG,
    FileType.JPG,
    FileType.MPG,
    FileType.AVI,
]

VECTOR_FILETYPES = [
    FileType.DXF,
    FileType.DWG,
    FileType.WPGVECTOR,
    FileType.THREEDS,
]

AUDIO_FILETYPES = [
    FileType.MOD,
    FileType.SIXSIXNINE,
    FileType.STM,
    FileType.S3M,
    FileType.MTM,
    FileType.FAR,
    FileType.ULT,
    FileType.AMF,
    FileType.DMF,
    FileType.OKT,
    FileType.ROL,
    FileType.CMF,
    FileType.MID,
    FileType.SADT,
    FileType.VOC,
    FileType.WAV,
    FileType.SMP8,
    FileType.SMP8S,
    FileType.SMP16,
    FileType.SMP16S,
    FileType.PATCH8,
    FileType.PATCH16,
    FileType.XM,
    FileType.HSC,
    FileType.IT,
]

ARCHIVE_FILETYPES = [
    FileType.ZIP,
    FileType.ARJ,
    FileType.LZH,
    FileType.ARC,
    FileType.TAR,
    FileType.ZOO,
    FileType.RAR,
    FileType.UC2,
    FileType.PAK,
    FileType.SQZ,
]
