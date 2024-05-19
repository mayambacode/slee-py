import { useEffect, useState } from 'react';
import styles from './LandingScreen.css';

const LandingScreen = () => {
  const [fade, setFade] = useState(styles.fadeIn);

  useEffect(() => {
    const timer = setTimeout(() => {
      setFade(styles.fadeOut);
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className={`${styles.landingScreen} ${fade}`}>
      <span className={styles.logo}>🌒</span>
    </div>
  );
};

export default LandingScreen;
