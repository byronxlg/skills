---
name: dd-prompt-to-table
description: Order food on DoorDash end to end from a vibe and a budget using DoorDash's official dd-cli - set up and verify the CLI, pick a restaurant and items, preview the all-in price, place the order without further check-ins, and ping Byron on Telegram with the arrival time. Use when Byron gives food vibes and a budget and wants it ordered ("order me dinner", "something light under $25", "prompt to table", "surprise me with food"), or asks to install, set up, or test dd-cli / DoorDash CLI. Placing an order spends money - only submit when Byron has explicitly asked for an order in the current request and given a budget.
---

# DoorDash: prompt to table

Byron gives vibes and a budget; you turn that into a delivered meal with `dd-cli`, DoorDash's
official CLI (github.com/doordash-oss/doordash-cli). The first run (2026-09-30) went from
"not that hungry, had sushi for lunch, ideally NZ$25" to a NZ$20.18 meal (plus a NZ$3 tip,
which is no longer allowed - see below) and a Telegram ping in about ten minutes.

## Authorization

- The request itself is the authorization: vibes + budget + "order it" means place the order
  without checking back, within budget. `dd-cli`'s own help text says to confirm tip and card
  with the consumer before submit - Byron's upfront request satisfies that. Still name the card
  in your narration.
- **Never tip.** Byron's standing instruction: always `--tip-cents 0`. That is his explicit
  decline, so don't ask about or suggest a tip, and don't add one to use up spare budget.
- Research, menus, carts and previews are free. `order submit` is the only command that spends.
- No budget, no clear ask to order, or the best option is over budget: stop and ask.
- Never submit twice for one request. Submit has no idempotency; a retry is a second order.

## Setup (first run on a machine)

1. **Install.** Download the macOS arm64 tarball from the latest GitHub release with `gh release
   download`, compare its SHA256 with the release digest, then check the binary before running
   `install.sh`:
   ```sh
   codesign -dv --verbose=2 dd-cli-v*-darwin-arm64 2>&1 | rg 'Authority|TeamIdentifier'
   ```
   Require `Developer ID Application: DoorDash, Inc. (W44ZWC57TC)`. v0.2.5 shipped ad-hoc signed
   (no team ID, Gatekeeper rejects it) while v0.2.4 was properly signed - if the latest release
   is not DoorDash-signed, install the newest one that is and tell Byron why.
   Run `bash install.sh </dev/null`: it copies `dd-cli` and `_internal/` into `~/.local/bin` and
   skips its interactive agent-skill prompt (skills here are Skillfold-managed; don't install it).
2. **Login.** Browser OAuth, so Byron runs it: ask him to type `! dd-cli login`. The token lands
   in the macOS keychain.
3. **Smoke test.** `address list` (below). `Error: The user is forbidden.` on every command means
   the account is not yet off the waitlist (https://forms.gle/gvCQZvu9C1EKA6aM6) - stop and say
   so. It cleared for Byron a few days after first login.

## CLI conventions

- `--json-output` goes before the subcommand; data is under `.structuredContent`.
- Every service command needs `--intent`, two lines, and **DoorDash stores it**. Keep it to the
  food goal and Byron's words; nothing personal beyond the order. Write it once to a temp file:
  ```sh
  cat > "$TMP/intent.txt" <<'EOF'
  Summary: Order the user a light, non-sushi dinner within a NZ$25-30 all-in budget
  user prompt/purpose: "<Byron's request verbatim>"
  EOF
  INTENT=$(cat "$TMP/intent.txt")
  ```
- Each subcommand's `--help` has long agent guidance; read it when a call fails.

## Ordering flow

1. **Ask** (only if missing): vibes (cuisine or feeling, hunger level, who it's for), budget in
   local currency, allergies. Treat the budget as all-in: food + delivery + fees (no tip).
2. **Address.** `dd-cli --json-output address list --intent "$INTENT"` - use the entry with
   `is_default: true` and pass its `address_id` everywhere.
3. **Search wide.** Several queries that fit the vibe, not one:
   ```sh
   for q in pho "banh mi" thai dumplings; do
     dd-cli --json-output search -q "$q" --address-id "$A" --limit 4 --intent "$INTENT" \
       | jq -r '.structuredContent.stores[] | "\(.store_id) | \(.name) | \(.rating) (\(.review_count)) | \(.distance)"'
   done
   ```
   Prefer high rating with many reviews, within about 2 mi, and a store that shows up for
   several queries. Check the local time: late evening, avoid stores that close soon.
4. **Menu.** `dd-cli --json-output menu --store-id <id> --intent "$INTENT"` gives `menu_id`,
   `store_is_open`, and `items[]` with `item_id`, `name`, `price`, `description`,
   `has_required_modifiers`, `is_orderable`. Budget roughly NZ$5-9 for delivery and fees
   (delivery fee varies by store: NZ$2.99 to NZ$5.99 seen), so a NZ$25 budget means about
   NZ$15-18 of food.
5. **Cart.** First `cart list --store-id <id>`. Items append to an existing cart, so if one
   exists: delete it only if you created it earlier in this session; otherwise it may be
   Byron's own, so pick another store or ask. Menu IDs look like `i_12972110570`; pass them **without** the `i_` prefix:
   ```sh
   dd-cli --json-output cart add-items --store-id <id> --menu-id <menu_id> \
     --items-json '[{"item_id":"12972110570","item_name":"Lemongrass Chicken Roll","quantity":1}]' \
     --intent "$INTENT"
   ```
   Keep the returned `cart_uuid`; check `item_errors` is empty. Required modifiers: see
   `restaurant-item-details --help`.
6. **Preview.** `dd-cli order preview --cart-uuid <uuid> --beautify --intent "$INTENT"` shows
   subtotal, delivery fee, fees, "Total before tip", and delivery options with an ETA. Read-only
   unless `--fulfillment` is passed.
7. **Card.** No tip (see Authorization), so the preview's "Total before tip" is the final
   total and must be within budget. Name the card: `payment-method list`, the
   `cards[]` entry whose `payment_method_id` equals `default_payment_method_id` (brand + last4).
   An empty `cards[]` means the default may be a wallet - stop and ask.
8. **Submit once.**
   ```sh
   dd-cli --json-output order submit --cart-uuid <uuid> --tip-cents 0 --yes --intent "$INTENT"
   ```
   Without `--yes`, a non-TTY call hits `Proceed? [y/N]: Aborted!` (nothing charged). Success
   returns `success: true` and an `order_uuid`. On any error or ambiguous result, check
   `order status` / `order history` - never resubmit blind.
9. **Status and ETA.** `order status --order-uuid <uuid>` returns `status` (`placed` then
   `store_confirmed`), `delivery_window_start/end` and `quoted_delivery_time` in **UTC** -
   convert to local time before reporting.
10. **Ping.** Send Byron a Telegram message per the telegram rule: store, items, arrival
    window, all-in total and card. Then give the same summary in chat.

## Cleanup

Delete carts you won't order: `cart delete --cart-uuid <uuid>`. `cart list` should be empty
afterwards unless Byron is mid-order himself.
