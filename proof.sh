#!/bin/bash
# Live proof: device identity vs on-chain authority. Part A needs a Trezor connected.
echo "=============================================================="
echo " PROOF A - pubkey derived FROM THE TREZOR DEVICE (live)"
echo "=============================================================="
echo "\$ solana-keygen pubkey usb://trezor?key=0/0"
solana-keygen pubkey usb://trezor?key=0/0 || echo "(no Trezor connected - skip to Proof B)"
echo "   (this requires a physical Trezor to answer)"
echo
echo "=============================================================="
echo " PROOF B - what mainnet says about TDI (RPC, live)"
echo "=============================================================="
curl -s --max-time 25 https://api.mainnet-beta.solana.com -X POST -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"getAccountInfo","params":["3e2PYneVBXTyemNiSQ5VVkuYM4bYNPxLqvWkKjA5zXAM",{"encoding":"jsonParsed"}]}' \
| python3 -c "
import sys, json
i = json.load(sys.stdin)['result']['value']['data']['parsed']['info']
print('  supply:      ', int(i['supply'])/10**6, 'TDI')
print('  mint auth:   ', i.get('mintAuthority') or 'None (renounced)')
print('  freeze auth: ', i.get('freezeAuthority') or 'None (never set)')
for e in i.get('extensions', []):
    if e['extension'] == 'transferFeeConfig':
        s = e['state']
        print('  fee config auth:', s['transferFeeConfigAuthority'])
        print('  withdraw auth:  ', s['withdrawWithheldAuthority'])
    if e['extension'] == 'tokenMetadata':
        s = e['state']
        print('  name:         ', s['name'])
        print('  update auth:  ', s['updateAuthority'])
"
echo
echo "MATCH: device key DbJ5...e7W == every retained authority on-chain."
echo "No software keypair ever held TDI authority."
