import { IonPage } from '@ionic/react';
import { useEffect, useState } from 'react';
import { Queries } from '../model/Queries';
import { validate } from 'mysql-query-validator'
import './Home.css';
import { QueryActions } from '../model/QueryActions';

const username = prompt("Enter Username:");
const password = prompt("Enter Password:");
const connection = new WebSocket("ws://localhost:5000");

const Home: React.FC = () => {

  const [query, setQuery] = useState<string>("");
  const [lastMessage, setMessage] = useState<string>("");
  const [token, setToken] = useState<string>("");
  const [database, setDatabase] = useState<string | null>(null);

  const [lockingQueries, setLockingQueries] = useState<Array<string>>([]);
  const [databaseMap, setDatabaseMap] = useState<any>({});
  
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
        // TODO: Correct behaviour here
        // setToken(message.data);
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

  }, []);
  
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
          setMessage(`Changes commited successful`);
          return;
        }
        setMessage("No changes to commit");
        return;
      }

      const commitQuery = lockingQueries.join(";");
      connection.send(JSON.stringify({
        query: commitQuery,
        token,
        database,
      }));
      setDatabaseMap({});
      setLockingQueries([]);
      setMessage(`Changes commited successful`);
      return;
    }

    try{
      validate(query)
    }
    catch(err){
      setMessage("Check query syntax and try again");
      return;
    }
    
    if(splittedQuery[0].toUpperCase() != "USE" && database == null){
      setMessage("ERROR 1046 (3D000): No database selected");
      return;
    }
    if(splittedQuery[0].toUpperCase() == "USE"){
      setDatabase(splittedQuery[1].replaceAll(";", ""));
      setMessage("Database changed");
      return;
    }

    let tableName: string = ""
    let records: Array<Record<string, string>> = [];
    
    switch (splittedQuery[0].toUpperCase()) {
      case Queries.INSERT:
        tableName = splittedQuery[2];
        // TODO: Parse query for records
        const columnsStartDelimiter: number = query.indexOf("(");
        const columnsEndDelimiter: number = query.indexOf(")");

        // RESULT: ["fname", "lname"]
        const columns: Array<string> = query
          .substring(columnsStartDelimiter + 1, columnsEndDelimiter)
          .replaceAll("', ", "',")
          .split(",");


        const valuesStartDelimiter: number = query.indexOf("(", columnsStartDelimiter + 1);
        const valuesEndDelimiter: number = query.lastIndexOf(")", columnsEndDelimiter + 1);

        // RESULT: [["john", "brown"],["john", "brown"],["john", "brown"]]
        records = query
          .substring(valuesStartDelimiter + 1, valuesEndDelimiter)
          .replaceAll("', ", "',")
          .replaceAll("), ", "),")
          .split(",(")
          .map(param => {
            const val: Array<any> = eval(`[${param.replaceAll("(", "").replaceAll(")", "")}]`);
            const result: Record<string, any> = {};
            for(let x = 0; x < val.length; x++){
              result[columns[x]] = val[x]; 
            }
            return result;
          });

        break;
      case Queries.UPDATE:
        tableName = splittedQuery[1];
        // TODO: Parse query for records
        break;
      case Queries.DELETE:
        tableName = splittedQuery[2];
        // TODO: Parse query for records
        break;
    }

    if(isLockingQuery){
      setLockingQueries([
        ...lockingQueries,
        query,
      ]);
      setDatabaseMap({
        ...databaseMap,
        [tableName]: [
          ...databaseMap[tableName],
          ...records,
        ],
      });
      setMessage("Query exection successful");
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
            <input className="container--input-field" onChange={(e) => setQuery(e.target.value)}></input>
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
