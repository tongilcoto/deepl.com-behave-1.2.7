# DOWNLOAD FEATURES

## typescript code
```
import * as dotenv from 'dotenv';
import * as fs from 'fs';
import * as path from 'path';
import { chromium, Browser, request } from 'playwright';
//const AdmZip = require('adm-zip');
import AdmZip from 'adm-zip';
dotenv.config()

// Try to use env variable REQUESTS_CA_BUNDLE=/opt/homebrew/etc/ca-certificates/cert.pem
// You can place it in your .bash_profile or .zshrc
// If not, uncomment this other line
// process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

const browserProxyOptions = {
  server: process.env.PROXY_SERVER || '',
  bypass: process.env.PROXY_BYPASSED_HOSTS,
  username: process.env.PROXY_USERNAME,
  password: process.env.PROXY_PASSWORD,
};

export async function jiraLogin() {
  // Decide environment
  const isCiCd = !!process.env[process.env.CI_CD_ENV_VARIABLE || ''];
  const needsProxy = isCiCd ? process.env.CI_CD_NEEDS_PROXY : process.env.LOCAL_NEEDS_PROXY;
  const proxyOptions = needsProxy ? browserProxyOptions : undefined;

  // Credentials
  const username = isCiCd ? process.env.CI_CD_JIRA_USERNAME : process.env.LOCAL_JIRA_USERNAME;
  const password = isCiCd ? process.env.CI_CD_JIRA_PASSWORD : process.env.LOCAL_JIRA_PASSWORD;

  // User keys
  const jiraUserKey = isCiCd ? process.env.CI_CD_JIRA_USER_KEY : process.env.LOCAL_JIRA_USER_KEY;
  const jiraUserName = isCiCd ? process.env.CI_CD_JIRA_USER_NAME : process.env.LOCAL_JIRA_USER_NAME;
  process.env.JIRA_USER_KEY = jiraUserKey || '';
  process.env.JIRA_USER_NAME = jiraUserName || '';

  const browser = await chromium.launch({headless: false, slowMo: 100, proxy: proxyOptions});
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.goto('https://jira.XXXX.com/');
  await page.fill('#identifierInput', username || '');
  await page.click('#postButton button');
  await page.waitForSelector('#password');
  await page.fill('#password', password || '');
  await page.click('#signOnButton');
  await page.waitForSelector('#logo');
  // eslint-disable-next-line ui-testing/no-hard-wait
  await page.waitForTimeout(2000);
  const cookies = await context.cookies();
  // Find the specific cookie
  const loginCookie = cookies.find(c => c.name === process.env.LOGIN_COOKIE);

  if (!loginCookie) {
    await browser.close();
    return `Login has failed. ${process.env.LOGIN_COOKIE} cookie not found!`;
  }

  const apiContext = await request.newContext({
      baseURL: "https://jira.axa.com",
      extraHTTPHeaders: { "Content-Type": "application/json" },
      ignoreHTTPSErrors: true,
      storageState:  {
        cookies,
        origins: [] // mandatory
      }
  });
  console.log("Logged in successfully");
  return { browser, apiContext };
}

async function downloadFeatureFile(apiContext: any, testSet: string) {
  const response = await apiContext.get(`/jira/rest/raven/1.0/export/test?keys=${testSet}`)
  if (response.status() !== 200) {
    return `Error downloading ${testSet} feature file: ${response.status()}`;
  }
  const content = await response.body();
  const headers = await response.headers();
  const disposition = headers['content-disposition'] || '';
  let fileFormat: 'zip' | 'text' = 'text';
  if (disposition.includes('.zip')) {
    fileFormat = 'zip';
  } else if (disposition.includes('.feature')) {
    fileFormat = 'text';
  }
  const dir = 'features';
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  const fileBaseName = path.join(dir, `${testSet}`);
  const fileName = `${fileBaseName}.feature`;
  if (fileFormat === 'zip') {
    // Save the buffer as a zip file
    const zipFilePath = `${fileBaseName}.zip`;
    fs.writeFileSync(zipFilePath, content);
    // Extract the zip file
    const zip = new AdmZip(zipFilePath);
    zip.extractAllTo(dir, true);
  } else {
    let text = content.toString('utf-8');
    text = text.split('\n').map((line: string) => line.trimEnd()).join('\n');
    fs.writeFileSync(fileName, text, { encoding: 'utf-8' });
  }
  console.log(`Saved ${fileName}`);
  return 'OK';
}
  

function parseTestSetArg() {
  const args = process.argv.slice(2); // Skip 'node' and script path
  const testSetIndex = args.findIndex(arg => arg === '-t' || arg === '--test-set');
  if (testSetIndex !== -1 && args[testSetIndex + 1]) {
    return args[testSetIndex + 1]
  }
  console.error('Usage: ts-node download_features.ts -t|--test-set <test-set>');
  process.exit(1);
}

async function main() {
  const testSet = parseTestSetArg();
  const loginResult = await jiraLogin();
  if (typeof loginResult === 'string') {
    console.error(loginResult);
    process.exit(1);
  }
  const { browser, apiContext } = loginResult;
  await downloadFeatureFile(apiContext, testSet);
  browser.close();
}

if (require.main === module) {
  main().catch(error => {
    console.error('Error in main function:', error);
    process.exit(1);
  });
}
```

## python code
```
import argparse
import os
import zipfile
from playwright.sync_api import sync_playwright, Browser, APIRequestContext
from dotenv import load_dotenv


load_dotenv()
load_dotenv(os.getenv('RAMP_DOT_ENV'))

browser_proxy_options = {
    "server": os.getenv('PROXY_SERVER'),
    "bypass": os.getenv('PROXY_BYPASSED_HOSTS'),
    "username": os.getenv('PROXY_USERNAME'),
    "password": os.getenv('PROXY_PASSWORD')
}

def jira_login(p) -> tuple[Browser | None, APIRequestContext | None]:
    """
    Login en Jira usando un objeto Playwright (p), devuelve el browser y el api_context autenticado.
    """
    if os.getenv(os.getenv('CI_CD_ENV_VARIABLE')):
        proxy_options = browser_proxy_options if os.getenv('CI_CD_NEEDS_PROXY') else None
        browser = p.chromium.launch(headless=False, slow_mo=100, proxy=proxy_options)
        username = os.getenv('CI_CD_JIRA_USERNAME')
        password = os.getenv('CI_CD_JIRA_PASSWORD')
    else:
        proxy_options = browser_proxy_options if os.getenv('LOCAL_NEEDS_PROXY') else None
        browser = p.chromium.launch(headless=False, slow_mo=100, proxy=proxy_options)
        username = os.getenv('LOCAL_JIRA_USERNAME')
        password = os.getenv('LOCAL_JIRA_PASSWORD')
    page = browser.new_page()
    page.goto('https://jira.XXX.com/')

    page.fill('#identifierInput', username)
    page.click('#postButton button')
    page.wait_for_selector('#password', timeout=60000)
    page.fill('#password', password)
    page.click('#signOnButton')
    page.wait_for_selector('#logo', timeout=60000)
    cookies = page.context.cookies()

    login_cookie = next((c['value'] for c in cookies if c['name'] == os.getenv("LOGIN_COOKIE")), None)
    if login_cookie:
        print(f"{os.getenv('LOGIN_COOKIE')} cookie found and saved to env: {login_cookie}")
    else:
        print(f"{os.getenv('LOGIN_COOKIE')} cookie not found!")
        browser.close()
        return None, None

    # Create the API context with browser cookies
    api_context = p.request.new_context(
        base_url="https://jira.axa.com",
        extra_http_headers={"Content-Type": "application/json"},
        ignore_https_errors=True,
        storage_state={"cookies": cookies, "origins": []},
    )
    return browser, api_context

def download_feature_file(test_set: str, api_context: APIRequestContext):
    url = f"/jira/rest/raven/1.0/export/test?keys={test_set}"
    response = api_context.get(url)
    disposition = response.headers.get('content-disposition', '')
    dir = 'features'
    os.makedirs(dir, exist_ok=True)
    file_base_name = os.path.join(dir, test_set)

    if '.zip' in disposition:
        zip_file_path = f"{file_base_name}.zip"
        data: bytes = response.body()
        with open(zip_file_path, 'wb') as f:
            f.write(data)
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(dir)
        print(f"Saved and extracted {zip_file_path} in {dir}")
    else:
        file_name = f"{file_base_name}.feature"
        text = response.body().decode('utf-8')
        text = '\n'.join(line.rstrip() for line in text.splitlines())
        with open(file_name, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
        print(f"Saved features/{test_set}.feature")

def main(test_set: str):
    with sync_playwright() as p:
        browser, api_context = jira_login(p)
        if not browser or not api_context:
            print("Login failed. Exiting.")
            return
        download_feature_file(parser.parse_args().test_set, api_context)
        browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download features from JIRA for RAMP tests")
    parser.add_argument('-t', '--test-set', help="Jira issue id for Test Set", required=True)
    main(parser.parse_args().test_set)

```




# UPLOAD REPORT

## typescript code (cucumber)
```
import * as dotenv from 'dotenv';
import * as fs from 'fs';
import * as path from 'path';
import { chromium, APIRequestContext, request } from 'playwright';
const AdmZip = require('adm-zip');
import { JIRA_PROJECT_ID, JIRA_PROJECT_KEY, JIRA_MAIN_COMPONENT_ID, JIRA_MAIN_COMPONENT_NAME, JIRA_TEST_EXECUTION_ISSUE_TYPE_ID } from "./sut/constants";

dotenv.config()

process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

const browserProxyOptions = {
  server: process.env.PROXY_SERVER || '',
  bypass: process.env.PROXY_BYPASSED_HOSTS,
  username: process.env.PROXY_USERNAME,
  password: process.env.PROXY_PASSWORD,
};

function getTestExecutionPayload(execComment: string) {
  return {
    "fields": {
      "assignee":
      {
        "key": process.env.JIRA_USER_KEY,
        "name": process.env.JIRA_USER_NAME,
        "active": true,
      },
      "reporter":
      {
        "key": process.env.JIRA_USER_KEY,
        "name": process.env.JIRA_USER_NAME,
        "active": true,
      },
		  "project": {
        "id": JIRA_PROJECT_ID,
        "key": JIRA_PROJECT_KEY,
		  },
		  "summary": `RAMP E2E - ${execComment}`,
		  "issuetype": {
        "id": JIRA_TEST_EXECUTION_ISSUE_TYPE_ID,
        "name": "Test Execution",
		  },
		  "components" : 
      [
        {
          "id": JIRA_MAIN_COMPONENT_ID,
          "name": JIRA_MAIN_COMPONENT_NAME
        }
      ],
  		// "customfield_10032" : [ // It is in the official doc example, I cannot guess the real field name
	  	// 	"TES-38"
		  // ]
	  }
  }
}

function getIssueLinkPayload(testExecution: string, testSet: string) {
  return {
    "type": {
        "name": "Tests",
    },
    "inwardIssue": {
        "key": testExecution
    },
    "outwardIssue": {
        "key": testSet
    },
    "comment": {
        "body": `Test Execution created by E2E RAMP testing framework! Linked to ${testSet}`,
    }
  }
}

export async function jiraLogin() {
  // Decide environment
  const isCiCd = !!process.env[process.env.CI_CD_ENV_VARIABLE || ''];
  const needsProxy = isCiCd ? process.env.CI_CD_NEEDS_PROXY : process.env.LOCAL_NEEDS_PROXY;
  const proxyOptions = needsProxy ? browserProxyOptions : undefined;

  // Credentials
  const username = isCiCd ? process.env.CI_CD_JIRA_USERNAME : process.env.LOCAL_JIRA_USERNAME;
  const password = isCiCd ? process.env.CI_CD_JIRA_PASSWORD : process.env.LOCAL_JIRA_PASSWORD;

  // User keys
  const jiraUserKey = isCiCd ? process.env.CI_CD_JIRA_USER_KEY : process.env.LOCAL_JIRA_USER_KEY;
  const jiraUserName = isCiCd ? process.env.CI_CD_JIRA_USER_NAME : process.env.LOCAL_JIRA_USER_NAME;
  process.env.JIRA_USER_KEY = jiraUserKey || '';
  process.env.JIRA_USER_NAME = jiraUserName || '';

  const browser = await chromium.launch({headless: false, slowMo: 100, proxy: proxyOptions});
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.goto('https://jira.XXXX.com/');
  await page.fill('#identifierInput', username || '');
  await page.click('#postButton button');
  await page.waitForSelector('#password');
  await page.fill('#password', password || '');
  await page.click('#signOnButton');
  await page.waitForSelector('#logo');
  // eslint-disable-next-line ui-testing/no-hard-wait
  await page.waitForTimeout(2000);
  const cookies = await context.cookies();
  // Find the specific cookie
  const loginCookie = cookies.find(c => c.name === process.env.LOGIN_COOKIE);

  if (!loginCookie) {
    await browser.close();
    return `Login has failed. ${process.env.LOGIN_COOKIE} cookie not found!`;
  }

  const apiContext = await request.newContext({
      baseURL: "https://jira.axa.com",
      ignoreHTTPSErrors: true,
      storageState:  {
        cookies,
        origins: [] // mandatory
      }
  });
  console.log("Logged in successfully");
  return { browser, apiContext };
}

async function upload_json_report(apiContext: APIRequestContext, json_report_file: string, exec_comment: string) {
  const test_exec_payload = getTestExecutionPayload(exec_comment)
  console.log(test_exec_payload)
  console.log("Checking file ...", fs.existsSync(json_report_file));
  console.log(`requesting ${json_report_file} with ${exec_comment}`)
  const resultBuffer = fs.readFileSync(json_report_file);
  const infoBuffer = Buffer.from(JSON.stringify(test_exec_payload), 'utf-8');
  const response = await apiContext.post('/jira/rest/raven/1.0/import/execution/cucumber/multipart',{
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
  console.log(response.status())
  if (response.status() !== 200) {
    return `Error uploading ${json_report_file} report: ${response.status()} ${await response.body()}`;
  }
  console.log(await response.json());
  return (await response.json()).testExecIssue.key;
}

async function link_execution_to_test_set(apiContext: APIRequestContext, testExecution: string, testSet: string) {
  const data = getIssueLinkPayload(testExecution, testSet);
  console.log(data)
  const response = await apiContext.post('/jira/rest/api/2/issueLink', {
    headers: { 'Content-Type': 'application/json' },
    data: JSON.stringify(data)
  });
  console.log(response.status())
  if (response.status() !== 201) {
    console.log((await response.body()).toString())
    return `Error linking ${testExecution} to ${testSet}: ${response.status()} ${await response.body()}`;
  }
}

function parseTestSetArg() {
  const args = process.argv.slice(2); // Skip 'ts-node' and script path
  const reportIndex = args.findIndex(arg => arg === '-r' || arg === '--report');
  const commentIndex = args.findIndex(arg => arg === '-c' || arg === '--comment');
  const testSetIndex = args.findIndex(arg => arg === '-t' || arg === '--test-set');
  if (reportIndex !== -1 && args[reportIndex + 1] && commentIndex !== -1 && args[commentIndex + 1] && testSetIndex !== -1 && args[testSetIndex + 1]) {
    return [args[reportIndex + 1], args[commentIndex + 1], args[testSetIndex + 1]];
  }
  console.error('Usage: ts-node upload_json_report.ts -r|--report <report-file> -c|--comment <comment> -t|--test-set <test-set>');
  process.exit(1);
}

async function main() {
  const [reportFile, execComment, testSet] = parseTestSetArg();
  const loginResult = await jiraLogin();
  if (typeof loginResult === 'string') {
    console.error(loginResult);
    process.exit(1);
  }
  console.log("Logged")
  const { browser, apiContext } = loginResult;
  const testExecution = await upload_json_report(apiContext, reportFile, execComment);
  await link_execution_to_test_set(apiContext, testExecution, testSet);
  console.log("Linked")
  browser.close();
}

if (require.main === module) {
  main().catch(error => {
    console.error('Error in main function:', error);
    process.exit(1);
  });
}

```

## python code (behave)
```
import argparse
import os
import json
from src.config.config import Config
from playwright.sync_api import sync_playwright, APIRequestContext, Browser
from dotenv import load_dotenv
import playwright.sync_api as pw

load_dotenv()
load_dotenv(os.getenv('RAMP_DOT_ENV'))

browser_proxy_options = {
    "server": os.getenv('PROXY_SERVER'),
    "bypass": os.getenv('PROXY_BYPASSED_HOSTS'),
    "username": os.getenv('PROXY_USERNAME'),
    "password": os.getenv('PROXY_PASSWORD')
}

def get_test_execution_payload(exec_comment: str) -> dict:
    return {
        "fields": {
            "assignee": {
                "key": os.getenv("JIRA_USER_KEY"),
                "name": os.getenv("JIRA_USER_NAME"),
                "active": True,
            },
            "reporter": {
                "key": os.getenv("JIRA_USER_KEY"),
                "name": os.getenv("JIRA_USER_NAME"),
                "active": True,
            },
            "project": {
                "id": Config.JIRA_PROJECT_ID,
                "key": Config.JIRA_PROJECT_KEY,
            },
            "summary": f"RAMP API - {exec_comment}",
            "issuetype": {
                "id": Config.JIRA_TEST_EXECUTION_ISSUE_TYPE_ID,
                "name": "Test Execution",
            },
            "components": [
                {
                    "id": Config.JIRA_MAIN_COMPONENT_ID,
                    "name": Config.JIRA_MAIN_COMPONENT_NAME,
                }
            ],
            # Puedes añadir campos personalizados aquí si lo necesitas
        }
    }

def get_issue_link_payload(test_execution: str, test_set: str) -> dict:
  return {
    "type": {
        "name": "Tests",
    },
    "inwardIssue": {
        "key": test_execution
    },
    "outwardIssue": {
        "key": test_set
    },
    "comment": {
        "body": f"Test Execution created by API RAMP testing framework! Linked to {test_set}",
    }
  }

def jira_login(p) -> tuple[Browser | None, APIRequestContext | None]:
    is_ci_cd = bool(os.getenv(os.getenv('CI_CD_ENV_VARIABLE', '')))
    needs_proxy = os.getenv('CI_CD_NEEDS_PROXY') if is_ci_cd else os.getenv('LOCAL_NEEDS_PROXY')
    proxy_options = browser_proxy_options if needs_proxy else None
    username = os.getenv('CI_CD_JIRA_USERNAME') if is_ci_cd else os.getenv('LOCAL_JIRA_USERNAME')
    password = os.getenv('CI_CD_JIRA_PASSWORD') if is_ci_cd else os.getenv('LOCAL_JIRA_PASSWORD')
    jira_user_key = os.getenv('CI_CD_JIRA_USER_KEY') if is_ci_cd else os.getenv('LOCAL_JIRA_USER_KEY')
    jira_user_name = os.getenv('CI_CD_JIRA_USER_NAME') if is_ci_cd else os.getenv('LOCAL_JIRA_USER_NAME')
    os.environ['JIRA_USER_KEY'] = jira_user_key or ''
    os.environ['JIRA_USER_NAME'] = jira_user_name or ''

    browser = p.chromium.launch(headless=False, slow_mo=100, proxy=proxy_options)
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://jira.XXXXX.com/')
    page.fill('#identifierInput', username or '')
    page.click('#postButton button')
    page.wait_for_selector('#password')
    page.fill('#password', password or '')
    page.click('#signOnButton')
    page.wait_for_selector('#logo')
    page.wait_for_timeout(2000)
    cookies = context.cookies()
    login_cookie = next((c['value'] for c in cookies if c['name'] == os.getenv("LOGIN_COOKIE")), None)
    if not login_cookie:
        browser.close()
        return None, None
    api_context = p.request.new_context(
        base_url="https://jira.axa.com",
        ignore_https_errors=True,
        storage_state={"cookies": cookies, "origins": []}
    )
    return browser, api_context

def filter_skipped_tests(report: list) -> list:
    for feature in report:
        feature['elements'] = [
            scenario for scenario in feature.get('elements', [])
            if any('result' in step for step in scenario.get('steps', []))
        ]
    return report

def upload_json_report(api_context: pw.APIRequestContext, json_report_file: str, exec_comment: str) -> str:
    if not os.path.exists(json_report_file):
        return f"Report file {json_report_file} does not exist."
    with open(json_report_file, 'rb') as f:
        result_buffer = f.read()
    cleaned_report = json.dumps(filter_skipped_tests(json.loads(result_buffer))).encode('utf-8')
    info_buffer = json.dumps(get_test_execution_payload(exec_comment)).encode('utf-8')
    multipart = {
        "info": {
            "name": "info.json",
            "mimeType": "application/json",
            "buffer": info_buffer
        },
        "result": {
            "name": "result.json",
            "mimeType": "application/json",
            "buffer": cleaned_report
        }
    }
    response = api_context.post('/jira/rest/raven/1.0/import/execution/behave/multipart',
        multipart=multipart,  # type: ignore
        timeout=120_000 )
    print("Response status:", response.status)
    print("Response text:", response.text())
    if response.status != 200:
        return f"Error uploading {json_report_file} report: {response.status} {response.text()}"
    return response.json()['testExecIssue']['key']

def link_execution_to_test_set(apiContext: APIRequestContext, test_execution: str, test_set: str) -> str | None:
    data = get_issue_link_payload(test_execution, test_set)
    response = apiContext.post('/jira/rest/api/2/issueLink',
        headers={ 'Content-Type': 'application/json' },
        data=json.dumps(data)
    )
    print("Response status:", response.status)
    print("Response text:", response.text())
    if response.status != 201:
        return f"Error linking {test_execution} to {test_set}: {response.status} {response.text()}"
    return "OK"

def main(report_file: str, exec_comment: str):
    with sync_playwright() as p:
        browser, api_context = jira_login(p)
        if not browser or not api_context:
            print("Login failed. Exiting.")
            return
        test_execution = upload_json_report(api_context, report_file, exec_comment)
        print(test_execution)
        result = link_execution_to_test_set(api_context, test_execution, args.test_set)
        print(result)
        browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload Cucumber JSON report to Jira")
    parser.add_argument('-r', '--report', help="Path to Cucumber JSON report file", required=True)
    parser.add_argument('-c', '--comment', help="Jira Test Execution title", required=True)
    parser.add_argument('-t', '--test-set', help="Test Set of the execution", required=True)
    args = parser.parse_args()
    main(args.report, args.comment)

```

# UPDATE TEST SCENARIO

## typescript code (cucumber)
```
async function updateTestWithComment(jiraId: string, newGherkin: string) {
    if (!apiContext) {
        console.log("Error: Not logged in. Please login first.");
        return;
    }
    if (jiraId.startsWith('@')) {
        jiraId = jiraId.substring(1);
    }
    const url = `/jira/rest/api/2/issue/${jiraId}`;
    const payload = {
        fields: {
            customfield_12622: newGherkin
        }
    };

    let response = await apiContext.put(url, { data: JSON.stringify(payload) });
    if (response.status() !== 204) {
        const text = await response.text();
        console.log(`Error updating ${jiraId} test scenario: ${response.status()} ${text}`);
        return;
    }

    const commentPayload = { body: "This is a comment added by the RAMP E2E Automation Framework." };
    response = await apiContext.post(`${url}/comment`, { data: JSON.stringify(commentPayload) });
    if (response.status() !== 201) {
        const text = await response.text();
        console.log(`Error adding comment to ${jiraId} test: ${response.status()} ${text}`);
        return;
    }
    console.log(`${jiraId} updated with new scenario`);
}

function getScenarioText(pickle: any): string {
  const filename = pickle.uri;
  const mainTag = pickle.tags[0]?.name.replace(/^@/, ''); // Remove leading @ if present

  if (!filename || !mainTag) return "error";

  // Read file lines
  const content = fs.readFileSync(filename, 'utf-8');
  content.replace(/\r\n/g, '\n'); // Normalize line endings
  const lines = content.split('\n');

  // Find the main tag in the file
  let tagStartIdx: number | null = null;
  for (let i = 0; i < lines.length; i++) {
    if (new RegExp(`@${mainTag}\\b`).test(lines[i])) {
      tagStartIdx = i;
      break;
    }
  }
  if (tagStartIdx === null) return "error";

  // Extract scenario text
  const scenarioText: string[] = [];
  let startIdx = tagStartIdx + 2; // As in Python: line after tag + "Scenario: ..." line

  for (let i = startIdx; i < lines.length; i++) {
    const line = lines[i];
    if (/^\s*@/.test(line) && scenarioText.length > 0) break;
    if (/^\s*Scenario/.test(line) && scenarioText.length > 0) break;
    if (line.length > 0) {
      scenarioText.push(line.replace(/^\t+/, '').replace(/\r$/, '').trimEnd());
    }
  }

  return scenarioText.join('\n');
}
```


## python code

```
def update_test_with_comment(api_context: APIRequestContext, jira_id: str, new_gherkin: str):
    url = f"/jira/rest/api/2/issue/{jira_id}"
    data = {
        "fields": {
            Config.JIRA_GHERKIN_FIELD: new_gherkin,
        }
    }
    response = api_context.put(url, data=json.dumps(data))
    if response.status != 204:
        text = response.text()
        return f"Error updating {jira_id} test scenario: {response.status} {text}"
    data = {"body": "Test Scenario updated (comment added by the API Automation Framework.)"}
    response = api_context.post(f"{url}/comment", data=json.dumps(data))
    if response.status != 201:
        text = response.text()
        return f"Error adding comment to {jira_id} test: {response.status} {text}"
    return f"{jira_id} updated with new scenario"


# Needed because of Scenario Outline with multiple examples.
# "scenario" object in before_scenario hook is already instantiated with examples
def get_scenario_text(scenario) -> str|None:
    filename = scenario.filename
    main_tag = scenario.tags[0]
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Looking for the main tag in the file
    tag_start_idx = None
    for i, line in enumerate(lines):
        if re.search(rf'@{main_tag}\b', line):
            tag_start_idx = i
            break
    if tag_start_idx is None:
        return None

    # Extracting the scenario text
    scenario_text = []
    start_idx = tag_start_idx + 2
    for line in lines[start_idx:]:
        if re.match(r'^\s*@', line) and len(scenario_text) > 0:
            break
        if re.match(r'^\s*Scenario', line) and len(scenario_text) > 0:
            break
        if len(line) > 1:
            if "Examples:" in line:
                scenario_text.append('')
            scenario_text.append(line.lstrip('\t').rstrip())

    return '\n'.join(scenario_text)
```






