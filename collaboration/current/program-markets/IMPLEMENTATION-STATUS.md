# Portfolio Market Launch Schedule — implementation checkpoint

Status updated 2026-09-14: Existing-program Market Launch Schedule is configured, verified and PUBLISHED. The earlier implementation notes below are historical; remaining-work statements in them are superseded by this update.

- 152 Programs, 760 market rows, 760 unique Program/Market keys; five rows per Program.
- All 20 source Lookups and four channel display formulas exist and are valid. Display formulas use LEFT(ARRAYJOIN(source),10) within SWITCH(Market,...) for YYYY-MM-DD text, preserving blanks.
- Full comparison: 3,040 channel values checked against original Program dates, including 2,652 blanks; zero differences.
- Existing Portfolio Program detail contains read-only Market Launch Schedule: Market / DTC / Amazon / Rcom / In Store; sorted by Market Order. User-facing Lily page verified after publication.
- Original dates remain maintained in Program; no second writable date copy.
- New Program automatic five-row creation is NOT implemented. Single-record link enforcement, isolated edit/clear test and broader role verification remain pending.
- Later compact layout changes and removal of the duplicate standalone EU date widget are DRAFT ONLY; source fields were not deleted.
- Full continuation checkpoint: ../interface-implementation/2026-09-14-HANDOFF.md

## Completed in Airtable

- Base: appOMWiK4CTOH7iQu
- Table: Program Markets (tblVXMjT7vWeJwthB)
- Market: fldjM7TfaYvPteNFf
- Program link: fldkjCFcOei2JeqYN
- Reverse field on Programs: fldnYmBmrPrx5cKTM
- Market Order: fldXL2tSqISHFqtKX
- Program Market Key: fldM2nTtnpPvBRIzT
- Readback: {"rows":760,"programs":152,"uniqueKeys":760,"errors":[],"allProgramsHaveFive":true}
- Original source dates were not changed.

## Remaining

1. In browser restrict Program link to one record (connector rejected that option).
2. Create 20 lookup fields using Program link and the source field mapping below.
3. Create four display formulas selecting the corresponding lookup by Market. Preserve blank source dates. Format YYYY-MM-DD.
4. Configure Portfolio Program record detail: related Program Markets grid, only Market/DTC/Amazon/Rcom/In Store, sorted by Market Order; disallow adding/removing/unlinking/editing records.
5. Configure new-Program automation to create missing US/CA/MX/UK/EU rows keyed by Program record ID + Market. Check existing rows before create; serialize backfills. Not deployed yet.
6. Isolated date-change/clear tests and Interface tests, then publish only intended changes.

No placeholder date fields were created: supported connector create_field schema does not expose lookup creation. Do not replace live lookups with manual copied dates.

## Source mapping

| Lookup name | Source field | Source ID |
|---|---|---|
| US_DTC_Source | US_DTC_Launch_Date | fldSSQr6Ibi6XhXFY |
| US_Amazon_Source | US_Amazon_Launch_Date | fldWZbiM3EvHtacO5 |
| US_Rcom_Source | US_Rcom_Launch_Date | fldzJHFD5w803ORkr |
| US_InStore_Source | US_InStore_Launch_Date | fldeCCU8Ct0dtt4s2 |
| CA_DTC_Source | CA_DTC_Launch_Date | fldr4VAWjuOV7HonN |
| CA_Amazon_Source | CA_Amazon_Launch_Date | fldpsgNbpSyjiypm1 |
| CA_Rcom_Source | CA_Rcom_Launch_Date | fld2D3jhWC2mLX51k |
| CA_InStore_Source | CA_InStore_Launch_Date | fld9VhoDUUcsbW5ph |
| MX_DTC_Source | MX_DTC_Launch_Date | fldoa9itX3O0XDUEw |
| MX_Amazon_Source | MX_Amazon_Launch_Date | fldQce80LsDjnr6Qj |
| MX_Rcom_Source | MX_Rcom_Launch_Date | fldDJsJ5c8krCV5GF |
| MX_InStore_Source | MX_InStore_Launch_Date | fldql37hsF0SuWMCq |
| UK_DTC_Source | UK_DTC_Launch_Date | fldwtDg4lyh9Vn7It |
| UK_Amazon_Source | UK_Amazon_Launch_Date | fldiKyg13vvnH4bkh |
| UK_Rcom_Source | UK_Rcom_Launch_Date | fld5Le5kBAqgI26Gy |
| UK_InStore_Source | UK_InStore_Launch_Date | fldvzUycD3ofGujRu |
| EU_DTC_Source | EU_DTC_Launch_Date | fld6e1aQjJlWIFIi7 |
| EU_Amazon_Source | EU_Amazon_Launch_Date | fldbpYiEBp9DhWkPv |
| EU_Rcom_Source | EU_Rcom_Launch_Date | fldOrzVQJ7pPUFzFQ |
| EU_InStore_Source | EU_InStore_Launch_Date | fldVg3UwHeKU3Pidy |

## Display formulas (create after lookups)

### DTC

```text
SWITCH({Market},"US",ARRAYJOIN({US_DTC_Source}),"CA",ARRAYJOIN({CA_DTC_Source}),"MX",ARRAYJOIN({MX_DTC_Source}),"UK",ARRAYJOIN({UK_DTC_Source}),"EU",ARRAYJOIN({EU_DTC_Source}),"")
```

Check actual lookup date formatting before finalizing the display formula; do not claim it verified until inspected.
### Amazon

```text
SWITCH({Market},"US",ARRAYJOIN({US_Amazon_Source}),"CA",ARRAYJOIN({CA_Amazon_Source}),"MX",ARRAYJOIN({MX_Amazon_Source}),"UK",ARRAYJOIN({UK_Amazon_Source}),"EU",ARRAYJOIN({EU_Amazon_Source}),"")
```

Check actual lookup date formatting before finalizing the display formula; do not claim it verified until inspected.
### Rcom

```text
SWITCH({Market},"US",ARRAYJOIN({US_Rcom_Source}),"CA",ARRAYJOIN({CA_Rcom_Source}),"MX",ARRAYJOIN({MX_Rcom_Source}),"UK",ARRAYJOIN({UK_Rcom_Source}),"EU",ARRAYJOIN({EU_Rcom_Source}),"")
```

Check actual lookup date formatting before finalizing the display formula; do not claim it verified until inspected.
### In Store

```text
SWITCH({Market},"US",ARRAYJOIN({US_InStore_Source}),"CA",ARRAYJOIN({CA_InStore_Source}),"MX",ARRAYJOIN({MX_InStore_Source}),"UK",ARRAYJOIN({UK_InStore_Source}),"EU",ARRAYJOIN({EU_InStore_Source}),"")
```

Check actual lookup date formatting before finalizing the display formula; do not claim it verified until inspected.
