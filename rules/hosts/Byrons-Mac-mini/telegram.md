# Telegram notifications

A bot reaches Byron directly. Use it when something needs his attention (a long task finished, input needed), not for routine output. Token: Doppler `global/home` `TELEGRAM_BOT_TOKEN`, never hardcoded. Chat id: `8851680837`.

```sh
doppler run --project global --config home -- bash -c \
  'curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
    -d chat_id=8851680837 --data-urlencode text="your message here"'
```
