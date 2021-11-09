import { IonButton, IonContent, IonHeader, IonInput, IonPage, IonTitle, IonToolbar } from '@ionic/react';
import { useEffect, useState } from 'react';
import ExploreContainer from '../components/ExploreContainer';
import './Home.css';


const connection = new WebSocket("ws://localhost:5001");

const Home: React.FC = () => {

  const [lastMessage, setMessage] = useState<string>("hello world");

  useEffect(() => {
    connection.onmessage = (message) => setMessage(message.data);
    connection.onclose = () => {
      // console.log("Disconnected. Retrying...")
      // setTimeout(() => {
      //   connection = new WebSocket("ws://localhost:5001");
      // }, 5000);
    }
  });

  return (
    <IonPage className="container">
      <header className="container--header">
          <div className="container--row-label">
            <span>SQL</span>
          </div>
          <div className="container--input-field-parent">
            <input className="container--input-field"></input>
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
          <button className="container--footer-button">EXECUTE</button>
          <button className="container--footer-button">COMMIT</button>
        </div>
      </footer>
    </IonPage>
  );
};

export default Home;
