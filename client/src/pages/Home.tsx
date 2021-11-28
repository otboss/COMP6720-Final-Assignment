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
  const [queryCompleted, setQueryCompleted] = useState<boolean>(true);
  const [lastLockingQueryExecuted, setLastLockingQueryExecuted] = useState<boolean>(true);
  const [lockingQueries, setLockingQueries] = useState<Array<string>>([]);
  
  useEffect(() => {
    connection.onmessage = (message) => {
      console.log(message);
      setQueryCompleted(true);
      setQuery("");
      try{
        const parsedMessage = JSON.parse(message.data);
        if(typeof(parsedMessage) != "object" || parsedMessage == null){
          throw "invalid json";
        }
        setLastLockingQueryExecuted(true);
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
  
  const runQuery = async (action: QueryActions) => {
    setQueryCompleted(false);
    await new Promise((resolve) => setTimeout(resolve, 500));
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
        setMessage("Unable to commit query");
        setQueryCompleted(true);
        // setQuery("");
        return;
      }

      for(let x = 0; x < lockingQueries.length; x++){
        while(!lastLockingQueryExecuted){
          await new Promise((resolve) => setTimeout(resolve, 1000));
        }
        connection.send(JSON.stringify({
          query: lockingQueries[x],
          token,
          database,
        }));
        setLastLockingQueryExecuted(false);
      }
      setLockingQueries([]);
      setQueryCompleted(true);
      setQuery("");
      return;
    }
    
    if((splittedQuery[0].toUpperCase() == "CREATE" && splittedQuery[1].toUpperCase() == "DATABASE") == false && splittedQuery[0].toUpperCase() != "USE" && database == null){
      setMessage("ERROR 1046 (3D000): No database selected");
      setQueryCompleted(true);
      setQuery("");
      return;
    }
    if(splittedQuery[0].toUpperCase() == "USE"){
      setDatabase(splittedQuery[1].replaceAll(";", ""));
      setMessage("Database changed");
      setQueryCompleted(true);
      setQuery("");
      return;
    }

    if(isLockingQuery){
      setLockingQueries([
        ...lockingQueries,
        query,
      ]);
      setMessage("Query stored, commit to persist changes to remote database");
      setQueryCompleted(true);
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
            <input className="container--input-field" value={query} disabled={!queryCompleted} onChange={(e) => setQuery(e.target.value)}></input>
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
          <button className={queryCompleted ? "container--footer-button" : "container--footer-button-disabled"} disabled={!queryCompleted} onClick={() => {runQuery(QueryActions.EXECUTE);}}>EXECUTE</button>
          <button className={queryCompleted ? "container--footer-button" : "container--footer-button-disabled"} disabled={!queryCompleted} onClick={() => {runQuery(QueryActions.COMMIT);}}>COMMIT</button>
        </div>
      </footer>
    </IonPage>
  );
};

export default Home;
