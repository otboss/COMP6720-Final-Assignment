import { IonPage } from '@ionic/react';
import { useEffect, useState } from 'react';
import { QueryActions } from '../model/QueryActions';
import './Home.css';

const username = prompt("Enter Username:");
const password = prompt("Enter Password:");
const connection = new WebSocket("ws://localhost:5000");

const Home: React.FC = () => {

  const [query, setQuery] = useState<string>("");
  const [lastMessage, setMessage] = useState<string>("");
  const [token, setToken] = useState<string>("");
  
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
        setToken(message.data);
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
    connection.send(JSON.stringify({
      query,
      token,
      action: action,
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
