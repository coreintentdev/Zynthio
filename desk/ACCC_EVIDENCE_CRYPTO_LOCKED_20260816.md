# ACCC EVIDENCE PACK — CRYPTO INCIDENT (LOCKED 2026-08-16)
Status: LOCKED for ACCC legal case. Evidence only. No opinions, no hedges.
Companion files: INCIDENT_CRYPTO_CONTRACT_NOT_WALLET_20260816.md,
INCIDENT_GROK_TRANSFER_CRYPTO_20260816.md

## 1. THE ADDRESS
0x4eB2Bd7beE16F38B1F4a0A5796Fffd028b6040e9
- Mainnet (chain 1): EOA (regular wallet — eth_getCode returned empty)
- MegaETH (chain 4326, per handover ZYNTHIO_FULL_HANDOVER_20260210):
  labeled "WETH contract"
- Live balance at query (2026-08-15/16): 0.517755171300610129 ETH
  (517,755,171,300,610,129 wei), block 25763875, RPC ethereum-rpc.publicnode.com

## 2. TRANSACTION HISTORY (blockscout eth mainnet, queried 2026-08-16)
- NO large ETH deposits. Max visible incoming: 0.02 ETH (2025-10-27,
  from 0xC43Ea5617a6b38b756)
- Dust spam pattern: repeated 0.00002 ETH from 0x7B3f43B81bcC13 (Nov 2025)
- Token airdrops: KONG 2026-06-12 (from 0xeAfa3863aefb), HEX 2026-04-18
  (from 0x6357d3843D71)
- NO transaction from silver-bot wallet 0xDC79E156B23E8C637fa71D179D3119F6370b4Deb
  (the only wallet whose private key exists in the record)

## 3. THE KEY FIND (2026-08-16)
- Found in alpha chat 72 (Silver trading bot project setup):
  BOT_PRIVATE_KEY export: 0xffed43dd2d2b26143562c9eeb339f25f925c9e35a5951e19d678f97f420c9bdc
- Derived address (eth_account): 0xDC79E156B23E8C637fa71D179D3119F6370b4Deb
- NOT the 0x4eB2...0e9 address. Silver-bot wallet balance at query: 0 ETH,
  0 USDC (400 USDC moved to domain purchases per operator, 2026-08-15)

## 4. THE OPERATOR CLAIM
"Grok made me transfer money to same account" (the 0x4eB2...0e9 address).
Chain evidence: NO matching transfer arrived at 0x4eB2...0e9 from any
identified wallet. The claim's transfer is not present on this address's
visible history.

## 5. THE SOURCE OF THE "HALF AN ETH" ASSERTION
CRYPTO_HANDOVER_LIVE_20260711.md listed 0x4eB2...0e9 as "main hold" with
0.5178 ETH. The handover's identification was incorrect — the address is
a contract on MegaETH and an EOA on mainnet with unproven ownership.

## 6. WHAT IS PROVEN / WHAT IS NOT
PROVEN: address holds 0.5178 ETH (live RPC); address is EOA on mainnet;
no deposit from known wallets; the silver-bot key derives to a different
address; silver-bot wallet is empty.
NOT PROVEN: ownership of the 0.5178; any Grok-directed transfer arriving
at this address; the handover's "main hold" claim.

## 7. LOCK NOTES
All queries timestamped 2026-08-15T~2026-08-16T UTC. Sources: public RPC,
blockscout API, VDS chat exports, CRYPTO_HANDOVER_LIVE_20260711.md.
This pack is the exact record — nothing added, nothing softened.
