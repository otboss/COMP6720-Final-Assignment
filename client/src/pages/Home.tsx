import { IonPage } from '@ionic/react';
import { useEffect, useState } from 'react';
import { Queries } from '../model/Queries';
import { QueryActions } from '../model/QueryActions';
import './Home.css';

const username = prompt("Enter Username:");
const password = prompt("Enter Password:");
const connection = new WebSocket("ws://localhost:5000");

const Home: React.FC = () => {

  const [query, setQuery] = useState<string>("");
  const [lastMessage, setMessage] = useState<string>("");
  const [token, setToken] = useState<string>("");
  const [database, setDatabase] = useState<string | null>(null);
  const [lockingQueries, setLockingQueries] = useState<Array<string>>([]);
  
  useEffect(() => {
    connection.onmessage = (message) => {
      try{
        const parsedMessage = JSON.parse(message.data);
        if(typeof(parsedMessage) != "object" || parsedMessage == null){
          throw "invalid json";
        }
        setMessage(message.data);
      }
      catch(err){
        if(token == ""){
          setToken(message.data);
        }
      }
    };
    connection.onerror = () => connection.close();
    connection.onclose = () => {
      setMessage("connection closed. Refresh page to reconnect");
    }

    (async () => {
      while(connection.readyState != 1){
        await new Promise((resolve) => setTimeout(resolve, 1000));
      }
      connection.send(JSON.stringify({
        username,
        password,
      }));      
    })();

  }, [token]);
  
  const runQuery = (action: QueryActions) => {
    const splittedQuery = query.split(" ");
    const isLockingQuery: boolean =
      splittedQuery[0].toUpperCase() == Queries.INSERT ||
      splittedQuery[0].toUpperCase() == Queries.UPDATE ||
      splittedQuery[0].toUpperCase() == Queries.DELETE;

    if(action == QueryActions.COMMIT){
      if(lockingQueries.length == 0){
        if(isLockingQuery){
          connection.send(JSON.stringify({
            query,
            token,
            database,
          }));
          setMessage(`Changes commited successfully`);
          setQuery("");
          return;
        }
        setMessage("No changes to commit");
        setQuery("");
        return;
      }

      const commitQuery = lockingQueries.join(";");
      connection.send(JSON.stringify({
        query: commitQuery,
        token,
        database,
      }));
      setLockingQueries([]);
      setMessage(`Changes commited successful`);
      setQuery("");
      return;
    }
    
    if(splittedQuery[0].toUpperCase() != "USE" && database == null){
      setMessage("ERROR 1046 (3D000): No database selected");
      setQuery("");
      return;
    }
    if(splittedQuery[0].toUpperCase() == "USE"){
      setDatabase(splittedQuery[1].replaceAll(";", ""));
      setMessage("Database changed");
      setQuery("");
      return;
    }

    if(isLockingQuery){
      setLockingQueries([
        ...lockingQueries,
        query,
      ]);
      setMessage("Query stored, commit to apply changes");
      setQuery("");
      return;
    }

    connection.send(JSON.stringify({
      query,
      token,
      database,
    }));
  };

  return (
    <IonPage className="container">
      <header className="container--header">
          <div className="container--row-label">
            <span>SQL</span>
          </div>
          <div className="container--input-field-parent">
            <input className="container--input-field" value={query} onChange={(e) => setQuery(e.target.value)}></input>
          </div>
      </header>
      <div className="container--result-container">
        <div className="container--row-label">
          <span>RESULT</span>
        </div>
        <textarea readOnly className="container--output-container" value={lastMessage}></textarea>
      </div>
      <footer className="container--footer">
        <div className="container--row-label">
          
        </div>
        <div className="container--button-container">
          <button className="container--footer-button" onClick={() => {runQuery(QueryActions.EXECUTE);}}>EXECUTE</button>
          <button className="container--footer-button" onClick={() => {runQuery(QueryActions.COMMIT);}}>COMMIT</button>
        </div>
      </footer>
    </IonPage>
  );
};

export default Home;
