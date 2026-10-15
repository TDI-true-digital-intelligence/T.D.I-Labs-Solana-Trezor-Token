# Verify receipts — machine-checkable facts

Every line below was produced by a real command run on the build machine (Oct 15 2026),
each independently re-checkable by any reader.

## A. The graft is crypto-pure (only Cargo.toml lines differ)

```
# Sources of remote-wallet 4.0.0 (from crates.io) vs the kit's graft:
diff patches/remote-wallet-trezor/src <(crates.io solana-remote-wallet-4.0.0 src)
-> identical. Zero crypto-code changes.

# The only modifications (both in Cargo.toml, both mechanical):
1. version 4.0.0 -> 3.1.14   (so the CLI's "3.1.0+" requirement matches the patch)
2. solana-pubkey req "~4.1.0" -> "3.0.0"  (relax, to co-exist with the CLI's pinned train)
```

## B. Stock CLI vs rebuilt CLI (same version, spl-token-cli 5.6.1)

```
$ strings spl-token.old | grep -c -i trezor
0
$ strings ~/.cargo/bin/spl-token | grep -c -i trezor
219
```

Old binary preserved at `~/.local/share/solana/install/active_release/bin/spl-token.old`.

## C. Why the stock CLI fails (from library source, docs.rs)

```
# solana-remote-wallet 3.1.14 (what stock CLI 5.6.1 links):
pub enum Manufacturer { Unknown, Ledger }
# -> usb://trezor parses as "not a manufacturer"

# solana-remote-wallet 4.0.0 (the graft source): Trezor present in the same enum
```

## D. On-chain receipts (RPC, read-only, re-runnable anytime)

```
getAccountInfo(3e2PYneVBXTyemNiSQ5VVkuYM4bYNPxLqvWkKjA5zXAM, jsonParsed):
  mintAuthority:    null                      (renounced — tx 4fFC75…)
  freezeAuthority:  null                      (never enabled)
  supply:           333333000000              (333,333.0 TDI, 6 decimals — tx 2wEzGY…)
  tokenMetadata:    name "True Digital Intelligence", symbol "TDI",
                    uri https://srv1537297.hstgr.cloud/tdi/token.json  (tx 5zBDSr…)
  transferFeeConfig: 193 bps, newer/older epoch fees identical,
                     authorities = creator pubkey (retained by design)
```

## E. Full genesis signature set

See [genesis.json](genesis.json) / [README.md](README.md) — 5/5 finalized on mainnet,
each signed by the Trezor Model T at `usb://trezor?key=0/0`.

## F. Off-chain assets (live URLs)

```
$ curl -sI https://srv1537297.hstgr.cloud/tdi/logo.png    -> 200, image/png, 309934 bytes
$ curl -s  https://srv1537297.hstgr.cloud/tdi/token.json  -> valid JSON, name/symbol/image
TLS: Let's Encrypt, served via Traefik on the project VPS
sha256(live logo.png) first 16 hex == sha256(local kit copy) first 16 == 519855892a34f4a9
```

---

*Produced by the Trezor Mint Protocol build system
([trezor-mint-kit](https://github.com/agi-digital-dot/trezor-mint-kit)).*
