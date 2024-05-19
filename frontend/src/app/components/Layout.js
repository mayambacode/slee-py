// components/Layout.js

import { useRouter } from 'next/router';

function Layout({ children }) {
  const router = useRouter();

  return (
    <div className="page-transition">
      {children}
    </div>
  );
}

export default Layout;