"""
https://github.com/jeffthibault/python-nostr
https://pypi.org/project/pynostr/
"""


from nostr.key import PrivateKey
from nostr.relay_manager import RelayManager
from nostr.event import EncryptedDirectMessage

import json
import ssl
import time
import lnmkt as ln

private_key="nsec1pfrgd36tpm02exj35tyvgs33kaylezalq5wdlnl8fc67jzk23ntscelxey"
public_key="npub1wlqptz2wnddnjcs5j9v36cj9em89h5v0jhet433d7med3h6w6u8qr635pc"

def main():
    #get_keys()
    #connect_relays()
    send_msg()
    print("Fin")

def get_keys():
    private_key = PrivateKey()
    print(private_key)
    public_key = private_key.public_key
    print(public_key)
    print(f"Private key: {private_key.bech32()}")
    print(f"Public key: {public_key.bech32()}")

#faut trouver une facon de reutiliser
def send_msg(msg):
    private_key = PrivateKey()
    relay_manager = RelayManager()
    relay_manager.add_relay("wss://nostr-pub.wellorder.net")
    relay_manager.add_relay("wss://relay.damus.io")
    npub = ln.get_npub()

    dm = EncryptedDirectMessage(
        recipient_pubkey=npub,
        cleartext_content=msg
        )
    
    private_key.sign_event(dm)
    relay_manager.publish_event(dm)
    relay_manager.close_all_relay_connections()
    return

if __name__ == "__main__":
    main()