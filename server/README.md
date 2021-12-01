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
<pre>const client = new WebSocket("ws://localhost:5000/")</pre>

<br>
<h3>Executing SQL query</h3>
Here are some sample queries. The format of queries are strict. Follow the format exactly as seen in the sample queries provided

<pre>SHOW DATABASES</pre>

sample response:
<pre>["forrest", "company"]</pre>
<br>
<br>
<pre>USE company</pre>

sample response:
<pre>Database changed</pre>
<br>
<br>
<pre>SHOW TABLES</pre>

sample response:
<pre>["students"]</pre>

<br>
<br>

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

<br>
<br>


<pre>INSERT INTO students VALUES ( 1, 'Pam', 'The University of the West Indies' )</pre>

sample response:
<pre>{"message": "Query is being processed"}</pre>


