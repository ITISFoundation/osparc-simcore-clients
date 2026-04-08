---
name: debug-e2e-tests
description: Debug failing e2e tests by analyzing pytest error logs and querying Grafana Loki for server-side logs
argument-hint: Paste the pytest failure output directly, including HTTP status code, response body, trace ID, and timestamp.
---

# Debug Failing E2E Tests

Follow this workflow to diagnose why an e2e test failed.

## Step 1: Extract key details from the pasted error logs

The user will paste the pytest failure output directly. From it, extract:
- The **HTTP status code** and **reason** (e.g. `502 Bad Gateway`)
- The **response body** JSON (e.g. `{"errors": ["Production_wb-api-server service unexpectedly failed"]}`)
- The **`X-Osparc-Trace-Id`** header value from the HTTP response headers (e.g. `028e864cbe26f8147ad0e83f86852fbb`)
- The **timestamp** from the `Date` response header (e.g. `Mon, 30 Mar 2026 10:12:41 GMT`) — use this to set the Loki query time range

## Step 2: Query Grafana Loki for server-side logs

Use the Grafana MCP tools to query Loki. First discover the Loki datasource UID:

1. Call `list_datasources` with `type=loki`
2. Use the returned `uid` for all subsequent Loki queries

### Services

Focus on simcore services. These are characterized by having `simcore` in their `service_name`.

### Key container names

The relevant services are:
- `*api-server*` — the API gateway (FastAPI) that receives client HTTP requests
- `*wb-api-server*` — the webserver backend that handles project/study operations
- `*webserver*` — another webserver instance
- `*director-v2*` — orchestrates computational pipelines
- `*catalog*` — handles data storage and retrieval

### JSON log fields available for filtering

Loki logs are JSON-structured. After `| json` in a LogQL query, these fields are available:

| Field | Description | Example |
|---|---|---|
| `log_trace_id` | Distributed trace ID (matches `X-Osparc-Trace-Id` header) | `028e864cbe26f8147ad0e83f86852fbb` |
| `log_span_id` | Span ID within the trace | `c83f7597d365e6fd` |
| `log_level` | Log severity | `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| `log_msg` | The actual log message / traceback | free text |
| `log_timestamp` | Timestamp of the log entry | `2026-03-30 10:12:45,569` |
| `log_source` | Source module and function | `rpc.access:_wrapper(51)` |
| `log_oec` | Operation error code | `None` or an OEC string |
| `log_uid` | User ID | `None` or numeric |
| `log_service` | Service name | `production-simcore_production_api-server` |
| `container_name` | Full container name | `production-simcore_production_api-server.2.id7qh3h95h3ceq3pnlyp0wcx8` |

### Recommended LogQL queries

**Find errors for a specific trace ID across all simcore services:**
```logql
{service_name=~".*simcore.*"} | json | log_trace_id = `<TRACE_ID>` | log_level = `ERROR`
```

**Find errors for a specific trace ID across all api-server containers:**
```logql
{container_name=~".*api-server.*"} | json | log_trace_id = `<TRACE_ID>` | log_level = `ERROR`
```

**Find errors and warnings in wb-api-server for a trace:**
```logql
{container_name=~".*wb-api-server.*"} | json | log_trace_id = `<TRACE_ID>` | log_level =~ `ERROR|WARNING|CRITICAL`
```

**Broad search for errors in wb-api-server around a time window (no trace ID):**
```logql
{container_name=~".*wb-api-server.*"} | json | log_level =~ `ERROR|CRITICAL`
```

**Search for crashes, OOM kills, or restarts:**
```logql
{container_name=~".*wb-api-server.*"} |= `error` or `killed` or `OOM` or `SIGTERM` or `SIGKILL`
```

**Search for errors in catalog service:**
```logql
{container_name=~".*catalog.*"} | json | log_level =~ `ERROR|CRITICAL`
```

### Query workflow

1. **Start with the `api-server`** — filter by trace ID and `ERROR` level. This shows the immediate error the gateway saw.
2. **Then check `wb-api-server`** — filter by the same trace ID and `ERROR|WARNING` levels. If empty, the service may have crashed without logging.
3. **If no trace-correlated errors**, broaden the time window and look for `ERROR|CRITICAL` logs without trace filtering — the service may have crashed and the error was logged under a different (or no) trace.
4. **Check for infrastructure issues** — look for `TimeoutError`, `RemoteProtocolError`, `Server disconnected` in the logs which indicate upstream service pressure.

## Step 3: Classify the failure

- **Server-side infrastructure issue**: 502/503/504 errors, `RemoteProtocolError`, `TimeoutError`, service disconnects. These are transient and not a client bug.
- **Client-side bug**: 400/422 errors with validation messages, incorrect request body, wrong API version.
- **Test environment issue**: Authentication failures (401/403), missing test fixtures, study/solver not found (404).

## Step 4: Check the simcore/Services Grafana dashboard

Find the dashboard dynamically:

1. Call `search_dashboards` with query `Services`
2. Look for a dashboard titled **"Services"** in the **"simcore"** folder
3. Use the returned `uid` for all subsequent dashboard queries
4. Call `get_dashboard_summary` to confirm panels and variables

This dashboard has two template variables:
- **`service`** — the simcore service to inspect. Relevant values for e2e debugging: `api-server`, `wb-api-server`, `webserver`, `director-v2`, `catalog`
- **`deployment`** — `staging`, `production`, or `master` (this must match the environment where the test ran - ask the user if unsure which value to use)

### Available panels

**Resource utilization:**
| Panel | ID | What it shows |
|---|---|---|
| CPU usage | 2 | CPU usage per container — look for spikes correlating with the failure time |
| Throttled CPU Time Rate | 22 | CPU throttling (seconds/second) — indicates the service is hitting its CPU limit |
| Memory usage | 3 | Memory per container — look for OOM patterns (memory climbing to limit then dropping) |
| Asyncio event loop lag | 19 | Per-container event loop lag — values >10ms consistently indicate event loop saturation |
| Asyncio event loop tasks | 20 | Total asyncio tasks (including done/cancelled) |
| Service logs | 21 | Aggregated service logs with health-check noise filtered out |

**HTTP server metrics (Prometheus-based):**
| Panel | ID | What it shows |
|---|---|---|
| HTTP request duration heatmap | 1 | Heatmap of request durations — look for a band of slow requests at the failure time |
| HTTP requests in progress | 8 | In-flight requests per container — high values suggest the service is overloaded |
| Avg HTTP request duration (5min) | 5 | Average request latency — look for spikes |
| HTTP requests count per status (5min) | 4 | Request counts by HTTP status code — look for 5xx spikes |
| HTTP request count per endpoint (5min) | 11 | Per-endpoint request volume |

**RPC server metrics (OpenTelemetry-based):**
| Panel | ID | What it shows |
|---|---|---|
| RPC request duration heatmap | 18 | Heatmap of RPC call durations |
| Avg RPC request duration (5min) | 12 | Average RPC latency |
| Sampled RPC request count per endpoint (5min) | 14 | RPC call volume per endpoint |

### How to use in debugging

Use `get_dashboard_panel_queries` or `get_panel_image` with the discovered dashboard UID and panel IDs above to inspect specific metrics. Set the time range to a window around the failure.

Key signals to look for:
- **Memory OOM**: Memory climbing to limit then abrupt drop in the Memory usage panel (ID 3) — explains `Server disconnected without sending a response`
- **CPU starvation**: High throttled CPU time (ID 22) — causes request timeouts
- **Event loop saturation**: Asyncio lag >10ms (ID 19) — causes the service to stop responding
- **5xx spike**: HTTP status panel (ID 4) showing a burst of 500/502/503 errors
- **Request pile-up**: In-progress requests (ID 8) climbing without draining


## Step 5:
If you cannot determine the cause of the failure from logs and metrics and there is a specific request which is failing, consider trying to reproduce the issue by making a request to that endpoint.
In order to do so you might need to ask the user for credentials to access the api-server.
