# Claim basis — what TDI does and does not claim

**Claimed:** TDI is a Solana token whose five identity-defining genesis transactions were all
signed by a Trezor Model T, created with a rebuilt `spl-token` CLI because the stock CLI cannot
sign with Trezor. To the best of our knowledge (5-source sweep, Oct 15 2026) it is the **first
documented** Trezor-signed token creation on Solana.

**Explicitly NOT claimed:** that TDI is the first token on Solana created with *any* hardware
wallet. Ledger devices have been able to sign Solana transactions (including token operations)
for years, and Ledger support ships in the stock CLI's remote-wallet library.

## Evidence behind each part

### 1. The genesis transactions are Trezor-signed (verifiable, not a matter of belief)
- Each tx is finalized on mainnet; its fee-payer/signer resolves to the creator pubkey,
  which is a Trezor Model T at derivation `usb://trezor?key=0/0`.
- The private key never existed outside the device (BIP-39 seed on Trezor; no keypair file was
  ever generated or used for these transactions).

### 2. The stock spl-token CLI cannot sign with Trezor (verified from source)
- `spl-token-cli 5.6.1` depends on `solana-remote-wallet 3.1.x`. In that version line,
  `src/locator.rs` defines `pub enum Manufacturer { Unknown, Ledger }` — parsing `usb://trezor`
  fails with *"not a manufacturer"*.
- Trezor support exists in `solana-remote-wallet 4.x`, which the CLI's pinned dependency set
  cannot resolve to (verified Oct 15 2026 via crates.io + docs.rs source reads).
- Capability delta, same CLI version: `strings` Trezor-string count = **0** (stock) vs **219**
  (rebuilt with the graft).

**How long was Trezor absent? (primary-source version walk, Oct 15 2026 — docs.rs source reads
of `locator.rs` + GitHub tree listings):**

| remote-wallet version | published | Manufacturer enum |
|---|---|---|
| 1.10.0 | 2022-03-03 | `{Unknown, Ledger}` |
| 1.14.0 | 2022-09-13 | `{Unknown, Ledger}` |
| 2.0.0 | 2024-06-21 | `{Unknown, Ledger}` |
| 2.0.24 | 2025-01-23 | `{Unknown, Ledger}` |
| 3.0.0 → 3.1.14 (what the CLI pins) | 2025-08 → 2026-04 | `{Unknown, Ledger}` |
| 4.0.0 | 2026-05-16 | Trezor present |

The solana-labs monorepo tags `v1.3.0` (Jan 2021) and `v1.9.0` (Jan 2022) contain **zero**
trezor source files anywhere in the tree. Conclusion: Trezor support has been absent from the
official Solana CLI stack for **at least 5 years** — "for years" claims are conservative.

### 3. "First documented Trezor-signed creation" (research sweep, Oct 15 2026)
Searched: Brave, X, YouTube, Reddit, GitHub for Trezor-signed Solana token creation. Found:
- Trezor *holding* support: announced Jan 2024 (Vacuumlabs integration; The Block, CoinMarketCap
  coverage) — storing/transacting SPL tokens in Trezor Suite, not creating mints from the CLI.
- Ledger token creation: documented and supported for years (Ledger's own SPL pages; Solana
  StackExchange threads on Ledger-signed token ops).
- No documented instance of a Trezor-signed `spl-token create-token` (or equivalent full-genesis
  flow) predating this repository was found in the sweep.

**Honest limits of #3:** absence of documentation ≠ impossibility. Someone may have done it
without publishing. The claim is therefore scoped to *first documented*, with the toolchain gap
(item 2) explaining why documentation is scarce: until the graft, the stock toolchain made this
practically impossible for a normal user.

## Sources (Oct 15 2026 sweep)
- https://www.theblock.co/post/268667/trezor-hardware-wallets-add-support-for-solana-and-spl
- https://coinmarketcap.com/academy/article/trezor-wallet-now-supports-solana-and-spl-tokens
- https://x.com/vacuumlabs/status/1737764721825128912 (Trezor Solana support integration)
- https://www.ledger.com/coin/wallet/spl (Ledger SPL support — predates)
- https://solana.stackexchange.com/questions/23085/is-it-possible-to-create-spl-token-on-ledger
- docs.rs source reads: `solana-remote-wallet` 3.1.14 `locator.rs` (Manufacturer enum),
  4.0.0 `locator.rs` (Trezor present)

*If you know of an earlier documented Trezor-signed Solana token creation, open an issue —
the claim will be corrected.*
