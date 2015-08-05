<H1>Project2</H1>

Project2 is a module which uses the PostgreSQL database to keep track of players and matches in a game tournament using the Swiss tournament model.

<H2>Quick start</H2>
<ul>
<li>
<a href="https://github.com/Afowler2k/udacity-fullstack-project2/archive/master.zip">Download the latest release</a>
</li>
<li>
Clone the repo: 
<code>
git clone https://github.com/Afowler2k/udacity-fullstack-project2.git
</code>
</li>
</ul>

<h3>What's included</h3>

Within the download you'll find the following directories and files.
<pre>
<code>
tournament.sql
tournament.py
tournament_test.py
</code>
</pre>

<h3>Running the project</h3>

These files will need to be run inside the Vagrant VM provided by Udacity for this project.<br/>
For additional setup information refer to <a href="https://docs.google.com/document/d/16IgOm4XprTaKxAa8w02y028oBECOoB1EI1ReddADEeY/pub?embedded=true">this document</a></br>
Once setup, you will need to run the tournament.sql file inside psql to initialize the database.<br/>
To launch PostgresSQL run:<br/>
psql<br/>
This will launch the postgres command line. <br/>
Now initialize the database by typing:<br/>
\i tournament.sql<br/>
\q<br/>
<br/>
You will now be back at the command line where you can run the unit tests, type:<br/>
python tournament_test.py<br/>
<br/>
You should see the successful completion on 9 unit tests.<br/>




