
from btchip.btchip import btchip
from btchip.btchipComm import getDongle


def sha256(text):
    import hashlib
    m = hashlib.sha256()
    m.update(bytearray.fromhex(text))

    return m.digest()


dongle = getDongle(True)
app = btchip(dongle)

# Set passwords
# empty password
app.setBTCVPassword(bytearray(1), btchip.BTCV_PASSWORD_INSTANT)

instantPassword = "instantPassword".encode('utf-8')
recoveryPassword = "recoveryPassword".encode('utf-8')

app.setBTCVPassword(instantPassword, btchip.BTCV_PASSWORD_INSTANT)
app.setBTCVPassword(recoveryPassword, btchip.BTCV_PASSWORD_RECOVERY)

# Set password use
instantPasswordHash = sha256(bytearray(instantPassword).hex().ljust(64, '0'))
recoveryPasswordHash = sha256(bytearray(recoveryPassword).hex().ljust(64, '0'))

app.setBTCVPasswordUse(bytearray(32), btchip.BTCV_TX_ALERT)
app.setBTCVPasswordUse(instantPasswordHash, btchip.BTCV_TX_INSTANT)
app.setBTCVPasswordUse(recoveryPasswordHash, btchip.BTCV_TX_RECOVERY)

# Get new account
address = eval(app.getWalletPublicKey("0'/0/0", btcvAddr=True)['address'])
assert address.decode("utf-8")[0] == 'R'

# Get new accounts
addresses = app.getWalletPublicKeyBatch(["0'/0/0", "0'/0/1"], btcvAddr=True)
assert len(addresses) == 2
for address in addresses:
    assert eval(address['address']).decode("utf-8")[0] == 'R'
