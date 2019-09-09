import hashlib
import hmac


def make_digest(message):
    return hmac.new(b'secret-shared-key-goes-here', message, hashlib.sha256).hexdigest()


digest = make_digest(b'my payload')
print(digest)
