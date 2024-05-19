"use client"; 

import { useState } from 'react';
//import styles from './page.module.css'; // Include your CSS file for styling
import reactElementToJSXString from "react-element-to-jsx-string";
// import { ButtonsCard } from "../ui/tailwindcss-buttons";

export default function Home() {
  const [step, setStep] = useState(1);
  const [heartRateTime, setHeartRateTime] = useState(null)
  const [heartRate, setHeartRate] = useState(null);
  const [targetHeartRate, setTargetHeartRate] = useState('');
  const [selectedSong, setSelectedSong] = useState(null);

  const fetchHeartRateData = async () => {
    try {
      const response = await fetch(
        'https://api.fitbit.com/1/user/-/activities/heart/date/today/today/1min.json',
        {
          headers: {
            Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1JTQ0ciLCJzdWIiOiI2TDZYV1YiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJlY2cgcnNldCByb3h5IHJwcm8gcm51dCByc2xlIHJjZiByYWN0IHJsb2MgcnJlcyByd2VpIHJociBydGVtIiwiZXhwIjoxNzE2MDk2NDc4LCJpYXQiOjE3MTYwNjc2Nzh9.6oCPE-30sWgD6loaNwC9AbGRlwH3AP3Yr6k6zcDHYbo'
          }
        }
      );
      if (!response.ok) {
        throw new Error('Failed to fetch heart rate data');
      }
      const data = await response.json();
      // Extract heart rate from data
      const mostRecentHeartRate = data["activities-heart-intraday"].dataset.slice(-1)[0];

      // console.log(mostRecentHeartRate)

      setHeartRate(mostRecentHeartRate.value);
      setHeartRateTime(mostRecentHeartRate.time)
      setStep(step + 1);
    } catch (error) {
      console.error('Error fetching heart rate data:', error);
    }
  };

  
  const fetchTargetSong = async () => {
    let apiUrl = "http://127.0.0.1:5000?heartRate=" + heartRate + "&targetHeartRate=" + targetHeartRate
    try {
      const response = await fetch(apiUrl);
      if (!response.ok) {
        throw new Error('Failed to fetch target song');
      }
      const data = await response.json();
      // console.log(data.returnedSong)
        setSelectedSong(data.returnedSong)
    } catch (error) {
      console.error('Error fetching target song data:', error);
    }
  };

  const handleSubmitInput = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setStep(step + 1);
  };

  return (
    <div >
      <header>
        <h1 className='underline'>sleePy</h1>     
      </header>
      <main>
        {step === 1 && (
          <div>
            <h2>sleePy?</h2>
            <form onSubmit={handleSubmitInput}>
              <p>Make sure your <strong>Fitbit</strong> device is on</p>
              <button type="submit" onClick={fetchHeartRateData}  className="shadow-[0_4px_14px_0_rgb(0,118,255,39%)] hover:shadow-[0_6px_20px_rgba(0,118,255,23%)] hover:bg-[rgba(0,118,255,0.9)] px-8 py-2 bg-[#0070f3] rounded-md text-white font-light transition duration-200 ease-linear">Get started</button>
            </form>
            {heartRate && (
              <div className="heart-rate-display">
                <div className="heart-animation"></div>
                <p>Your heart rate: <strong>{heartRate}</strong> at <strong>{heartRateTime}</strong></p>
              </div>
            )}
          </div>
        )}
        
        {step === 2 && (
          <div>
            <h2>Target Heart Rate</h2>
            {heartRate && (
              <div className="heart-rate-display">
                <div className="heart-animation"></div>
                <p>Your heart rate: <strong>{heartRate}</strong> at <strong>{heartRateTime}</strong></p>
              </div>
            )}
            <form onSubmit={handleSubmitInput}>
              <label>
                Enter your target heart rate:
                <input
                  type="number"
                  value={targetHeartRate}
                  onChange={(e) => setTargetHeartRate(e.target.value)}
                />
              </label>
              <button type="submit" onClick={fetchTargetSong}>Next</button>
            </form>
          </div>
        )}
        {step === 3 && !selectedSong && (
          <div>
            <h2>Loading...</h2>
            <p>The neural network is selecting a song for you</p>
            {/* You can add a loading animation here if desired */}
            {/* <button onClick={handleSubmitInput}>Skip</button> */}
          </div>
        )}
        {step === 3 && selectedSong && (
          <div>
            <h2>Music</h2>
            <p>Filename: {selectedSong}</p>
            <audio controls>
              <source src={"/assets/" + selectedSong} type="audio/mpeg" />
              Your browser does not support the audio element.
            </audio>
          </div>
        )}
      </main>
      <footer>
        <p>HawkHacks 2024: Kelly, May, Mayamba, Rachelle</p>
      </footer>
    </div>
  );
}
