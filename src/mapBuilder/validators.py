import os

import magic
from django.core.exceptions import ValidationError


def validate_pdf_image_or_audio(file):
    """Make sure the uploaded file's extension matches the content, and is
    within allowable extensions.

    Parameters
    -----------
    file : file
        The file to validate

    Raises
    -------
    ValdiationError
        When file type is unsupported, or has the wrong extension

    """
    # print('validate_is_pdf')
    valid_mime_types = {
        "application/pdf": [".pdf"],
        "image/jpeg": [".jpg", ".jpeg"],
        "image/png": [".png"],
        "image/gif": [".gif"],
        "image/tiff": [".tiff", ".tif"],
        "audio/mpeg3": [".mp3"],
        "audio/x-mpeg-3": [".mp3"],
        "audio/wav": [".wav"],
        "audio/x-wav": [".wav"],
    }
    file_mime_type = magic.from_buffer(file.read(1024), mime=True)
    if file_mime_type not in valid_mime_types.keys():
        # _valid_types = f''
        raise ValidationError(
            f"Unsupported file type. Must be one of the following: "
            f'{", ".join([k for k in valid_mime_types.keys()])}'
        )
    valid_file_extensions = valid_mime_types[file_mime_type]
    ext = os.path.splitext(file.name)[-1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError(
            f"File must have "
            f'{" or ".join([f"{e!r}" for e in valid_file_extensions]) } '
            "as its extension"
        )
