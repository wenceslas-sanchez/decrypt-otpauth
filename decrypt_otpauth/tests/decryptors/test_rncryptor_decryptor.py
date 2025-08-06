import pytest
from decrypt_otpauth.decryptors.rncryptor_decryptor import RNCryptorComponents


@pytest.fixture
def too_small_data():
    return b"x" * 65


@pytest.fixture
def valid_data():
    data = bytearray(66)
    data[0] = 3
    data[1] = 1
    data[2:10] = b"enc_salt"
    data[10:18] = b"hmc_salt"
    data[18:34] = b"1234567890123456"
    data[34:34] = b""
    data[34:] = b"0" * 32
    return data


@pytest.fixture
def data_with_cyphertext(valid_data):
    ciphertext = b"hello world encrypted data"
    hmac_value = b"0" * 32
    return bytes(valid_data)[:34] + ciphertext + hmac_value


def test_too_short_data(too_small_data):
    with pytest.raises(ValueError):
        RNCryptorComponents.from_bytes(too_small_data)


def test_valid_data(valid_data):
    components = RNCryptorComponents.from_bytes(valid_data)
    assert components.version == 3
    assert components.options == 1
    assert components.encryption_salt == b"enc_salt"
    assert components.hmac_salt == b"hmc_salt"
    assert components.iv == b"1234567890123456"
    assert components.ciphertext == b""
    assert components.hmac_value == b"00000000000000000000000000000000"
    assert (
        components.header_and_ciphertext == b"\x03\x01enc_salthmc_salt1234567890123456"
    )


def test_data_with_cyphertext(data_with_cyphertext):
    components = RNCryptorComponents.from_bytes(data_with_cyphertext)
    assert components.version == 3
    assert components.options == 1
    assert components.encryption_salt == b"enc_salt"
    assert components.hmac_salt == b"hmc_salt"
    assert components.iv == b"1234567890123456"
    assert components.ciphertext == b"hello world encrypted data"
    assert components.hmac_value == b"00000000000000000000000000000000"
    assert (
        components.header_and_ciphertext
        == b"\x03\x01enc_salthmc_salt1234567890123456hello world encrypted data"
    )
