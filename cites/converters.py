import base64


def id_to_url(story_id):
    return base64.b32encode(
        (MakeURLWeird.MAX_STORIES - story_id).to_bytes(5, 'little')
    ).decode('utf-8')


class MakeURLWeird:
    MAX_STORIES = 1000000000000
    regex = '[A-Z0-9]{8}'

    def to_python(self, value):
        return self.MAX_STORIES - int.from_bytes(
            base64.b32decode(value.encode('utf-8')), 'little')

    def to_url(self, value):
        weird_url = '{:8s}'.format(value)
        return weird_url
