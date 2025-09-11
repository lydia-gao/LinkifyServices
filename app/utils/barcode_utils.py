import io
import barcode
from barcode.writer import ImageWriter
from typing import BinaryIO

def to_barcode(original_url: str) -> BinaryIO:
    CODE128 = barcode.get_barcode_class("code128")
    code = CODE128(original_url, writer=ImageWriter())

    buffer = io.BytesIO()
    code.write(buffer)
    buffer.seek(0)
    return buffer  