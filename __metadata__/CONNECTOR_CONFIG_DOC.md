# Connector Configurations

Below is an exhaustive enumeration of all configurable parameters available, each accompanied by detailed explanations of their purposes, default behaviors, and usage guidelines to help you understand and utilize them effectively.

### Type: `object`

| Property | Type | Required | Possible values | Default | Description |
| -------- | ---- | -------- | --------------- | ------- | ----------- |
| OPENCTI_URL | `string` | ✅ | Format: [`uri`](https://json-schema.org/understanding-json-schema/reference/string#built-in-formats) |  | The OpenCTI platform URL. |
| OPENCTI_TOKEN | `string` | ✅ | string |  | The token of the user who represents the connector in the OpenCTI platform. |
| CONNECTOR_NAME | `string` |  | string | `"FSTEC BDU"` | Name of the connector. |
| CONNECTOR_SCOPE | `array` |  | string | `["bdu"]` | The scope or type of data the connector is importing, either a MIME type or Stix Object (for information only). |
| CONNECTOR_TYPE | `string` |  | string | `"EXTERNAL_IMPORT"` | Should always be set to EXTERNAL_IMPORT for this connector. |
| CONNECTOR_LOG_LEVEL | `string` |  | `debug` `info` `warn` `warning` `error` | `"error"` | Determines the verbosity of the logs. |
| BDU_BASE_URL | `string` |  | string | `"https://bdu.fstec.ru/files/documents/vulxml.zip"` | URL for the BDU XML. |
| BDU_INTERVAL | `integer` |  | `0 < x ` | `6` | Interval in hours to check and import new BDUs. Must be strictly greater than 1, advice from NIST minimum 2 hours. |
| BDU_PAGE_SIZE | `integer` | | | `0 < x ` | `1000` | Process page_size vulns at on time. |