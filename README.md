# jaeger

### Search reporting span
```sh
GET _search
{
  "query": {
    "match": {"traceID": "fc0312c1fd806a27" }
  }
}
```
