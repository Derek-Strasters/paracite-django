import base64


def id_to_url(primary_id):
    return base64.b32encode(
        (MakeURLWeird.MAX_STORIES - primary_id).to_bytes(5, 'little')
    ).decode('utf-8')


class MakeURLWeird:
    MAX_STORIES = 1000000000000  # FIXME: this isn't enough
    regex = '[A-Za-z0-9]{8}'
    expected_format = '{:8}'

    def to_python(self, value):
        return self.MAX_STORIES - int.from_bytes(
            base64.b32decode(value.encode('utf-8'), casefold=True), 'little')

    def to_url(self, value):
        weird_url = self.expected_format.format(value)
        return weird_url
