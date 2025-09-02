typescript code
```
async function upload_json_report(apiContext: APIRequestContext, json_report_file: string, exec_comment: string) {
  const test_exec_payload = getTestExecutionPayload(exec_comment)
  console.log(test_exec_payload)
  console.log("Checking file ...", fs.existsSync(json_report_file));
  console.log(`requesting ${json_report_file} with ${exec_comment}`)
  const resultBuffer = fs.readFileSync(json_report_file);
  const infoBuffer = Buffer.from(JSON.stringify(test_exec_payload), 'utf-8');
  const response = await apiContext.post('/jira/rest/raven/1.0/import/execution/behave/multipart',{
    multipart: {
      info: {
        name: 'info.json',
        mimeType: 'application/json',
        buffer: infoBuffer
      },
      result: {
        name: 'result.json',
        mimeType: 'application/json',
        buffer: resultBuffer
      }
    }
  });
```

python code
```
def upload_json_report(api_context: APIRequestContext, json_report_file: str, exec_comment: str) -> str:
    if not os.path.exists(json_report_file):
        return f"Report file {json_report_file} does not exist."
    with open(json_report_file, 'rb') as f:
        result_buffer = f.read()
    test_exec_payload = get_test_execution_payload(exec_comment)
    info_buffer = json.dumps(test_exec_payload).encode('utf-8')
    print("Tamaño del result_buffer:", len(result_buffer))
    response = api_context.post('/jira/rest/raven/1.0/import/execution/behave/multipart',
        multipart={
            "info": FilePayload(name="info.json", mime_type="application/json", buffer=info_buffer),
            "result": FilePayload(name="result.json", mime_type="application/json", buffer=result_buffer)
        }
    )
    if response.status != 200:
        print("Respuesta completa:", response.text())
        return f"Error uploading {json_report_file} report: {response.status} {response.text()}"
    return "OK"
```




