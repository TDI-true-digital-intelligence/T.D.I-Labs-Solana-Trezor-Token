# PROOF — verified live, reproducible by anyone

> Screenshot-driven? No. **Command-driven.** Any reader can run these exact commands and get these
> exact answers — that's a stronger proof class than an image. (For a visual, run `proof.sh` in
> this repo or watch the session transcript below.)

## The claim under test

**TDI's creator key lives on a Trezor Model T — no software keypair ever held authority.**

## A. The device proves its own identity (requires physical Trezor)

```
$ solana-keygen pubkey usb://trezor?key=0/0
DbJ5opgLXjpHkB4STqiJqJMvnVfhE8Pas4aKymzZPe7W
```

This command asks the *connected hardware device* to derive and report its public key. It cannot
succeed without a real Trezor answering on USB (stock solana-keygen, Agave 4.3, in-tree
remote-wallet). The device confirmed this live on Oct 16 2026, Trezor connected.

## B. Mainnet proves who holds authority (read-only RPC, no device)

```
$ getAccountInfo(3e2PYneVBXTyemNiSQ5VVkuYM4bYNPxLqvWkKjA5zXAM)

  supply:          333333.0 TDI
  mint authority:  None (renounced — supply final forever)
  freeze authority: None (never enabled)
  fee-config authority:  DbJ5opgLXjpHkB4STqiJqJMvnVfhE8Pas4aKymzZPe7W
  withdraw authority:    DbJ5opgLXjpHkB4STqiJqJMvnVfhE8Pas4aKymzZPe7W
  name:            True Digital Intelligence
  metadata update authority: DbJ5opgLXjpHkB4STqiJqJMvnVfhE8Pas4aKymzZPe7W
```

## C. The match (this is the proof)

| From the DEVICE (A) | From MAINNET (B) | Equal? |
|---|---|---|
| `DbJ5...e7W` | every retained authority |  |

Every authority TDI ever had resolves to the key that *just answered from inside a Trezor*.
The five genesis transactions (see [genesis.json](genesis.json)) were each signed by this key —
signatures verifiable via any explorer. **A software keypair never existed for this token.**

## D. The binary is not stock — and you can check it

```
$ strings ~/.cargo/bin/spl-token | grep -c -i trezor
219
```

Rebuild it yourself with the [trezor-mint-kit](https://github.com/TDI-true-digital-intelligence/T.D.I-Labs-Trezor-Mint-Kit)
(~10 min, self-verifying build) and the count comes back non-zero — the stock crates.io binary
returns 0.

## Run the whole proof

```bash
git clone https://github.com/TDI-true-digital-intelligence/tdi-true-digital
cd tdi-true-digital && bash proof.sh
```

Parts B and D run anywhere. Part A runs only with a Trezor plugged in — which is the point.
