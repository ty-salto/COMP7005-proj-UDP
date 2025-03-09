import secrets
def is_valid_address_port(addrport, is_port):
    if not addrport:
        raise ValueError("Missing Arguments: usage -ip <ip> -port <port>")
        return False
    if is_port:
        if addrport < 1 or addrport > 65535:
            raise ValueError("Invalid Port Number: Must be a number within range 1-65535")
            return False
        return True
    sections = addrport.split('.')
    if len(sections) != 4:
        raise ValueError("Invalid Address: Must be in the following format xxx.xxx.xxx.xxx")
        return False
    for section in sections:
        if not section.isdigit() or int(section) < 0 or int(section) > 255:
            raise ValueError("Invalid Address: Must be all numbers within range 0-255")
            return False
    return True

def valid_fixed_or_range_number(number):
    if not number:
        raise ValueError("Value must be not be empty")
        return False
    if not number.isdigit():
        raise ValueError("Invalid Number: Must be a number")
        return False
    return True

def validate_key(key):
    if not key:
        raise ValueError("Missing Key: usage -k <key>")
        return False
    for char in key:
        if not char.isalpha():
            raise ValueError("Invalid Key: Must be all alphabetic characters")
            return False
    return True


def read_file(file):
    try:
        with open(file) as f:
            return f.read()
    except Exception as e:
        print("File Error", e)

def packet_uid_generator() -> str:
    return secrets.token_hex(8)

