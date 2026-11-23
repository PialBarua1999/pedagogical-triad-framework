"""Fetch publicly accessible World Bank WDI API observations; never impute missing values."""
import csv
import json
import urllib.request
from datetime import datetime,timezone
from pathlib import Path

INDICATORS = {
    "SE.SEC.ENRR": "Secondary gross enrolment (%)",
    "SE.SEC.TCHR": "Secondary teachers (number)",
    "SE.SEC.TCHR.FE.ZS": "Female secondary teachers (%)",
    "SE.SEC.ENRL": "Secondary pupils (number)",
}
BASE="https://api.worldbank.org/v2/country/BGD/indicator/"

def fetch(target:Path):
    target.mkdir(parents=True,exist_ok=True)
    records=[]; failures=[]
    for code,label in INDICATORS.items():
        url=f"{BASE}{code}?format=json&per_page=2000"
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"PedagogicalTriadResearch/0.1 (educational research)"})
            with urllib.request.urlopen(req,timeout=25) as response:
                data=json.load(response)
            if not isinstance(data,list) or len(data)<2 or not isinstance(data[1],list):
                raise ValueError("World Bank API returned no observations")
            for r in data[1]:
                if r.get("value") is not None:
                    records.append({"indicator_code":code,"indicator":label,"country":"Bangladesh","year":r.get("date"),"value":r.get("value"),"source_url":url,"retrieved_utc":datetime.now(timezone.utc).isoformat()})
        except Exception as e:
            failures.append({"indicator":code,"error":str(e)})
    if records:
        with (target/"worldbank_bgd_secondary.csv").open("w",newline="",encoding="utf-8") as f:
            writer=csv.DictWriter(f,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    with (target/"fetch_log.json").open("w",encoding="utf-8") as f:
        json.dump({"records":len(records),"failures":failures,"indicators":INDICATORS},f,indent=2)
    return len(records),failures
