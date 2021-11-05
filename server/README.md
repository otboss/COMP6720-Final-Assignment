<h1>Server</h1>

For production environment place .env file in the server folder

<h3>Getting Started</h3>
<ol>
  <li>
    Install dependencies
    <pre>pip install -r requirements.txt</pre>
  </li>
  <li>
    Run web socket server
    <pre>python3 main.py</pre>
  </li>
</ol>


<h3>Connecting</h3>
Connecting to the server using a JavaScript web socket client
<pre>const client = new WebSocket("ws://localhost:5001/")</pre>

<h3>Logging in</h3>
Generating a new session token:
<pre>{
  "username": "root",
  "password": "root"
}</pre>

sample response: 
<pre>e56776d804ec9ded366b71aa6f196b954bf7d2da1837a95a66ec3a6e3eea9e02</pre>

<br>
<h3>Executing SQL query</h3>
Running an SQL query:
<pre>{
  "query": "SELECT * FROM accounts",
  "token": "e56776d804ec9ded366b71aa6f196b954bf7d2da1837a95a66ec3a6e3eea9e02"
}</pre>

sample response:
<pre>[
  {
    "id": 1,
    "user": "Alice",
    "account_no": 12345
  },
  {
    "id": 2,
    "user": "Blake",
    "account_no": 54321
  }
]</pre>

Select queries are truncated to 10000 results