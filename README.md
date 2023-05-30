# Speech2Text-WSS PoC
Exposing Azure Speech to Text Cognitive Service via a Web Socket Server Example.

## Approach
Some Commercial Off The Shelf (COTS) products integrate with WSS endpoints for Speech-to-Text (S2T) services. Since Azure Cognitive Service for S2T does not expose a WSS endpoint, this PoC contains code for standing up a WSS endpoint that leverages [Azure Speech SDK](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-sdk) to transcribe audio. 

COTS -> WSS Endpoint (Azure Speech SDK) -> Azure Cognitive Services (S2T)
