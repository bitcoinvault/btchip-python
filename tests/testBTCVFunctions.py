
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
app.setBTCVPassword("1", btchip.BTCV_PASSWORD_INSTANT)

instantPassword = "instantPassword"
recoveryPassword = "recoveryPassword"

app.setBTCVPassword(instantPassword, btchip.BTCV_PASSWORD_INSTANT)
app.setBTCVPassword(recoveryPassword, btchip.BTCV_PASSWORD_RECOVERY)

# Set password use
instantPasswordHash = sha256(bytearray(instantPassword.encode('utf-8')).hex().ljust(64, '0'))
recoveryPasswordHash = sha256(bytearray(recoveryPassword.encode('utf-8')).hex().ljust(64, '0'))

app.setBTCVPasswordUse(bytearray(32), btchip.BTCV_TX_ALERT)
app.setBTCVPasswordUse(instantPasswordHash, btchip.BTCV_TX_INSTANT)
app.setBTCVPasswordUse(recoveryPasswordHash, btchip.BTCV_TX_RECOVERY)

# Get new account
result = app.getWalletPublicKey("0'/0/0", btcvAddr=True, btcvPubkeyTree=btchip.BTCV_TX_ALERT)
address1 = result['address']
pubkey1 = result['publicKey']
assert address1.decode("utf-8")[0] == 'R'

result = app.getWalletPublicKey("0'/0/0", btcvAddr=True, btcvPubkeyTree=btchip.BTCV_TX_INSTANT)
address2 = result['address']
pubkey2 = result['publicKey']
assert address2.decode("utf-8")[0] == 'R'
assert address2 == address1
assert pubkey2 != pubkey1
