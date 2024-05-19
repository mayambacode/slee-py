"use client";

import { useState } from 'react';
import styles from './page.module.css';

import LandingScreen from "./components/LandingScreen/LandingScreen.jsx"

export default function Home() {
  const [step, setStep] = useState(2);
  const [heartRateTime, setHeartRateTime] = useState(null)
  const [heartRate, setHeartRate] = useState(null);
  const [restingHR, setRestingHR] = useState(65)
  const [selectedSong, setSelectedSong] = useState(null);

  const getHeartRateData = async () => {
    try {
      const response = await fetch(
        'https://api.fitbit.com/1/user/-/activities/heart/date/today/today/1min.json',
        {
          headers: {
            Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1JTQ0ciLCJzdWIiOiI2TDZYV1YiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJlY2cgcnNldCByb3h5IHJudXQgcnBybyByc2xlIHJjZiByYWN0IHJyZXMgcmxvYyByd2VpIHJociBydGVtIiwiZXhwIjoxNzE2MTI2OTc2LCJpYXQiOjE3MTYwOTgxNzZ9.pRy6Iu5dqbLBEYSF7yNHfF5YO3xcjviXpwJr_A_KHLU'
          }
        }
      );
      if (!response.ok) {
        throw new Error('Failed to get heart rate data');
      }
      const data = await response.json();
      // Extract heart rate from data
      const mostRecentHeartRate = data["activities-heart-intraday"].dataset.slice(-1)[0];

      // console.log(mostRecentHeartRate)

      setHeartRate(mostRecentHeartRate.value);
      setHeartRateTime(mostRecentHeartRate.time)
      setStep(step + 1);
    } catch (error) {
      console.error('Could not get heart rate data:', error);
    }
  };


  const fetchTargetSong = async () => {
    let apiUrl = "http://127.0.0.1:5000?heartRate=" + heartRate + "&restingHR=" + restingHR
    try {
      const response = await fetch(apiUrl);
      if (!response.ok) {
        throw new Error('Failed to fetch target song');
      }
      const data = await response.json();
      console.log(data.returnedSong)
      setSelectedSong(data.returnedSong)
      setStep(step + 1)
    } catch (error) {
      console.error('Error fetching target song data:', error);
    }
  };

  const handleSubmitInput = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setStep(step + 1);
  };

  return (
    <div className={styles.mainContent}>
      <header className={styles.header}>
        <h1>sleePy</h1>
      </header>
      <main>
        {/* {step === 1 && (
          <LandingScreen />
          
        )} */}
        {step === 2 && (
          <div>
            <h2>sleePy?</h2>
            <form onSubmit={handleSubmitInput}>
              <p>Make sure your <strong>Fitbit</strong> device is on</p>
              <button type="submit" onClick={getHeartRateData}>Get started</button>
            </form>
            {heartRate && (
              <div className="heart-rate-display">
                <div className="heart-animation"></div>
                <p>Your heart rate: <strong>{heartRate}</strong> at <strong>{heartRateTime}</strong></p>
              </div>
            )}
          </div>
        )}

        {step === 3 && (
          <div>
            {heartRate && (
              <div className="heart-rate-display">
                <div className="heart-animation"></div>
                <h2>Your heart rate: <strong>{heartRate}</strong> at <strong>{heartRateTime}</strong></h2>
                <h2>Your resting heart rate: <strong>{restingHR}</strong></h2>
                
            <button onClick={fetchTargetSong}>Next</button>
              </div>
            )}
          </div>
        )}
        {step === 4 && !selectedSong && (
          <div>
            <h2>Loading...</h2>
            <p>The neural network is selecting a song for you</p>
            {/* You can add a loading animation here if desired */}
            <button onClick={getHeartRateData}>Skip</button>
          </div>
        )}
        {selectedSong && (
          <div>
            <h2>Music</h2>
            <p>Filename: {selectedSong}</p>
            <audio controls>
              <source src={`./assets/${decodeURIComponent(selectedSong)}`} type="audio/mpeg" />
              Your browser does not support the audio element.
            </audio>
          </div>
        )}
      </main>
      <footer className={styles.footer}>
        settings ⚙️ {/* react router link to settings */}
      </footer>
    </div>
  );
}
