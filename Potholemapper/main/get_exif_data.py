# credit: https://gitlab.com/-/snippets/2215069

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional

from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS


def get_labeled_exif(file) -> Dict[str, Any]:
    """Get EXIF data as a human readable dict."""
    image: Image.Image = Image.open(file)
    image.verify()

    # call private method before fixing PIL issue:
    # https://github.com/python-pillow/Pillow/issues/5863
    exif = image._getexif()  # noqa
    if exif is None:
        return None
    else:
        return {TAGS.get(key, key): value for key, value in exif.items()}


def get_gps_info(exif_data: Dict[str, Any]) -> Dict[str, Any]:
    """Get GPS Info data as a human readable dict."""
    gps_info = exif_data.get("GPSInfo", {})
    return {GPSTAGS.get(key, key): value for key, value in gps_info.items()}


def _get_gps_coord(coord_name: str, gps_info: Dict[str, Any]) -> Optional[float]:
    """Get and convert GPS Info coordinates."""
    coord_key = f"GPS{coord_name.capitalize()}"
    coord_value = gps_info.get(coord_key)
    if coord_value is None:
        return None

    d, m, s = coord_value
    decimal_degrees = (
        Decimal(d.numerator) / Decimal(d.denominator)
        + Decimal(m.numerator) / Decimal(m.denominator) / Decimal(60)
        + Decimal(s.numerator) / Decimal(s.denominator) / Decimal(3600)
    )

    coord_ref_key = f"{coord_key}Ref"
    coord_ref = gps_info.get(coord_ref_key)
    if coord_ref in {"S", "W"}:
        decimal_degrees *= -1

    return round(float(decimal_degrees), ndigits=7)


def _get_altitude(exif_geo: Dict[str, Any]) -> Optional[float]:
    altitude = exif_geo.get("GPSAltitude")
    if altitude is None:
        return None

    altitude_ref = exif_geo.get("GPSAltitudeRef")
    if altitude_ref == 1:
        altitude *= -1

    return altitude


def get_location(exif_data: Dict[str, Any]) -> Dict[str, Optional[float]]:
    """
    Returns the latitude, longitude and altitude, if available
    """
    gps_info = get_gps_info(exif_data)

    location = {
        "latitude": _get_gps_coord("Latitude", gps_info),
        "longitude": _get_gps_coord("Longitude", gps_info),
        "altitude": _get_altitude(gps_info),
    }
    return {k: v for k, v in location.items() if v is not None}


def get_datetime(exif_data: Dict[str, Any]) -> Optional[datetime]:
    return exif_data.get("DateTimeOriginal")
