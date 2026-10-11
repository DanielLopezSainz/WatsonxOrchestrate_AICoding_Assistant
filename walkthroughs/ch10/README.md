# Chapter 10 walkthrough: CivicPulse on WhatsApp

This folder holds what chapter 10 produced: the exported definition of the Orchestrate Channel, `channels/whatsapp-channel.yaml`, with the Account SID replaced by a placeholder and the token empty, as the platform returns it.

There is nothing to import to skip this chapter: no later chapter depends on the Channel, and a Channel needs your own Twilio account. To create the Channel without following the chapter, put your Twilio values in `.env` as `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN` and send Bob, in Agent mode, the structured prompt of section 10.5; then set the event URL in Twilio as section 10.7 describes.

The command that creates the Channel, as Bob adds it to the import script:

```
orchestrate channels create \
  --agent-name civic_info_agent \
  --env live \
  --type twilio_whatsapp \
  --name "CivicPulse WhatsApp" \
  --description "Residents reach CivicPulse on WhatsApp." \
  --field account_sid="$TWILIO_ACCOUNT_SID" \
  --field twilio_authentication_token="$TWILIO_AUTH_TOKEN"
```
