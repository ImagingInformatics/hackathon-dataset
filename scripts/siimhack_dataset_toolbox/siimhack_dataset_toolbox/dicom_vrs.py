"""
Value representation definitions as in http://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
"""
from typing import Callable

from faker import Faker

from scripts.siimhack_dataset_toolbox.siimhack_dataset_toolbox.dicom_vr_faker import DicomVRProvider


class VR:
    """"A provider that simulate several dicom VR."""

    def __init__(self, short_name, long_name, generator:Callable = None):
        self.short_name = short_name
        self.long_name = self.long_name()
        self.generator = generator


    def __str__(self):
        return f"{self.short_name} ({self.long_name})"


class VRs:
    """DICOM Value Representations"""
    faker = Faker()
    faker.add_provider(DicomVRProvider)
    ApplicationEntity = VR('AE', 'Application Entity')
    AgeString = VR('AS', 'Age String')
    AttributeTag = VR('AT', 'Attribute Tag')
    CodeString = VR('CS', 'Code String')
    Date = VR('DA', 'Date')
    DecimalString = VR('DS', 'Decimal String')
    DateTime = VR('DT', 'Date Time')
    FloatingPointSingle = VR('FL', 'Floating Point Single')
    FloatingPointDouble = VR('FD', 'Floating Point Double')
    IntegerString = VR('IS', 'Integer String')
    LongString = VR('LO', 'Long String')
    LongText = VR('LT', 'Long Text')
    OtherByteString = VR('OB', 'Other Byte String')
    OtherDoubleString = VR('OD', 'Other Double String')
    OtherFloatString = VR('OF', 'Other Float String')
    OtherWordString = VR('OW', 'Other Word String')
    PersonName = VR('PN', 'Person Name')
    ShortString = VR('SH', 'Short String')
    SignedLong = VR('SL', 'Signed Long')
    SequenceOfItems = VR('SQ', 'Sequence of Items')
    SignedShort = VR('SS', 'Signed Short')
    ShortText = VR('ST', 'Short Text')
    Time = VR('TM', 'Time')
    UniqueIdentifier = VR('UI', 'Unique Identifier')
    UnsignedLong = VR('UL', 'Unsigned Long')
    Unknown = VR('UN', 'Unknown')
    UnsignedShort = VR('US', 'Unsigned Short')
    UnlimitedText = VR('UT', 'Unlimited Text')

