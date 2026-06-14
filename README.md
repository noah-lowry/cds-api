# Common Data Set (CDS) API

A structured schema and REST API (with FastAPI) for the Common Data Set.

The [Common Data Set](https://commondataset.org/) is a data specification including extremely detailed information on college and university enrollment, admissions, and costs, and is provided by the majority of universities. Unfortunately, this data is usually distributed in crappy PDFs on university websites, making it impractical to analyze in bulk.

This project is an interface for the 1600+ CDS data sources I have obtained and parsed through non-trivial methods. The API is by no means complete, and there is much more data than currently exposed.

## Usage/examples
cds-api is currently available at [nolow.dev/api/cds](https://nolow.dev/api/cds).


### Get institution info
```python
import httpx

api_url = "https://nolow.dev/api/cds"
inst_id = "carnegie_mellon_university"

resp = httpx.get(f"{api_url}/v1/institutions/{inst_id}").raise_for_status()
resp.json()
```

```json
{
    "id": "carnegie_mellon_university",
    "year": "co25",
    "identity": {
        "name": "Carnegie Mellon University",
        "city": "Pittsburgh",
        "state": "PA",
        "control": "private_nonprofit",
        "calendar": "semester",
        "website": "http://www.cmu.edu"
    },
    "enrollment": {
        "undergraduate": 7824,
        "graduate": 8852,
        "total": 16676
    },
    "cost": {
        "tuition": 67020.0,
        "required_fees": 1076.0,
        "food_and_housing": 21698.0,
        "total": 89794.0
    },
    "financial_aid": {
        "receiving_aid": 0.3948,
        "need_met": 1.0,
        "average_aid": 60909.0
    }
}
```

### Get admissions statistics

```python
import httpx

api_url = "https://nolow.dev/api/cds"
inst_id = "carnegie_mellon_university"

resp = httpx.get(f"{api_url}/v1/institutions/{inst_id}/admissions").raise_for_status()
resp.json()
```

```json
{
    "id": "carnegie_mellon_university",
    "year": "co25",
    "identity": {
        "name": "Carnegie Mellon University",
        "city": "Pittsburgh",
        "state": "PA",
        "control": "private_nonprofit",
        "calendar": "semester",
        "website": "http://www.cmu.edu"
    },
    "admissions": {
        "applied": 33941,
        "admitted": 3843,
        "enrolled": 1754,
        "acceptance_rate": 0.1132,
        "yield_rate": 0.4564,
        "test_optional": false,
        "sat_range": [1510, 1560],
        "act_range": [34, 36]
    }
}
```

### List institutions

```python
import httpx

api_url = "https://nolow.dev/api/cds"

resp = httpx.get(f"{api_url}/v1/institutions").raise_for_status()
resp.json()
```

```json
[
    {
        "id": "carnegie_mellon_university",
        "identity": {
            "name": "Carnegie Mellon University",
            "city": "Pittsburgh",
            "state": "PA",
            "control": "private_nonprofit",
            "calendar": "semester",
            "website": "http://www.cmu.edu"
        },
        "available_years": ["co19", "co20", "co21", "co22", "co23", "co24", "co25"],
        "latest_year": "co25"
    },
    ...
]
```

## Data notes
There is no guarentee that data provided by this API is 100% accurate all the time, although it is generally high quality. Some data is unavailable or partially available from the API. If you would like the full raw dataset, contact me.