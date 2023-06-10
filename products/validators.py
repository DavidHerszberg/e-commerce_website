import os, copy
import magic
from django.core.exceptions import ValidationError

def validate_is_csv(file):
    valid_file_extensions = ['.csv']
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('נא לבחור קובץ CSV בלבד')
    test_file = copy.deepcopy(file)
    valid_mime_types = ['text/csv', 'text/plain']
    file_mime_type = magic.from_buffer(test_file.read(1024), mime=True)
    if file_mime_type not in valid_mime_types:
        raise ValidationError('קובץ לא תקין')
