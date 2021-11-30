<h1>Server</h1>

For production environment place .env file in the server folder

<h3>Getting Started</h3>
Usage of a virtual environment (venv) is recommended.
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
Here are some sample queries. The format of queries are strict. Follow the format exactly as seen in the sample queries provided

<pre>SHOW DATABASES</pre>

sample response:
<pre>["forrest", "company"]</pre>

<pre>USE company</pre>

sample response:
<pre>Database changed</pre>

<pre>SHOW TABLES</pre>

sample response:
<pre>["students"]</pre>


<pre>SELECT name , school FROM students WHERE name = 'pam'" "Select name from student where n > b</pre>

sample response:
<pre>[
  {
    "name": "Alice",
    "school": 12345
  },
  {
    "name": "Blake",
    "school": 54321
  }
]</pre>



<pre>INSERT INTO students VALUES ( 1, 'Pam', 'The University of the West Indies' )</pre>

sample response:
<pre>{"message": "Query is being processed"}</pre>


