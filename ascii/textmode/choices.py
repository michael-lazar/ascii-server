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


class FileType(models.IntegerChoices):
    """
    SAUCE file type.
    """

    NONE = 0, "None"
    ASCII = 1, "ASCII"
    ANSI = 2, "ANSi"
    ANSIMATION = 3, "ANSiMation"
    RIPSCRIPT = 4, "RIP script"
    PCBOARD = 5, "PCBoard"
    AVATAR = 6, "Avatar"
    HTML = 7, "HTML"
    SOURCE = 8, "Source"
    TUNDRADRAW = 9, "TundraDraw"
    GIF = 10, "GIF"
    PCX = 11, "PCX"
    LBM = 12, "LBM/IFF"
    TGA = 13, "TGA"
    FLI = 14, "FLI"
    FLC = 15, "FLC"
    BMP = 16, "BMP"
    GL = 17, "GL"
    DL = 18, "DL"
    WPGBITMAP = 19, "WPG Bitmap"
    PNG = 20, "PNG"
    JPG = 21, "JPG/JPeg"
    MPG = 22, "MPG"
    AVI = 23, "AVI"
    DXF = 24, "DXF"
    DWG = 25, "DWG"
    WPGVECTOR = 26, "WPG Vector"
    THREEDS = 27, "3DS"
    MOD = 28, "MOD"
    SIXSIXNINE = 29, "669"
    STM = 30, "STM"
    S3M = 31, "S3M"
    MTM = 32, "MTM"
    FAR = 33, "FAR"
    ULT = 34, "ULT"
    AMF = 35, "AMF"
    DMF = 36, "DMF"
    OKT = 37, "OKT"
    ROL = 38, "ROL"
    CMF = 39, "CMF"
    MID = 40, "MID"
    SADT = 41, "SADT"
    VOC = 42, "VOC"
    WAV = 43, "WAV"
    SMP8 = 44, "SMP8"
    SMP8S = 45, "SMP8S"
    SMP16 = 46, "SMP16"
    SMP16S = 47, "SMP16S"
    PATCH8 = 48, "PATCH8"
    PATCH16 = 49, "PATCH16"
    XM = 50, "XM"
    HSC = 51, "HSC"
    IT = 52, "IT"
    BINARYTEXT = 53, "binary"
    XBIN = 54, "XBin"
    ZIP = 55, "ZIP"
    ARJ = 56, "ARJ"
    LZH = 57, "LZH"
    ARC = 58, "ARC"
    TAR = 59, "TAR"
    ZOO = 60, "ZOO"
    RAR = 61, "RAR"
    UC2 = 62, "UC2"
    PAK = 63, "PAK"
    SQZ = 64, "SQZ"
    EXECUTABLE = 65, "executable"


CHARACTER_FILETYPES = [
    FileType.ASCII,
    FileType.ANSI,
    FileType.ANSIMATION,
    FileType.RIPSCRIPT,
    FileType.PCBOARD,
    FileType.AVATAR,
    FileType.HTML,
    FileType.SOURCE,
    FileType.TUNDRADRAW,
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
