# threat_intel_ingestion
<b>Project Objective:</b> A python program that automates pipeline of collecting latest threat intelligence feed from platforms like OTX and directing it to Splunk for IOC co-relation.
<br><br>

<b>Workflow:</b><br>
```
Threat Feeds APIs
     ↓
Python Collector
     ↓
Normalization + Deduplication
     ↓
Optional Enrichment
     ↓
Send to Splunk HEC
     ↓
Splunk Index + Dashboard
```
