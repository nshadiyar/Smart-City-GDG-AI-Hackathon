import React, { useEffect, useState } from 'react';
import ChatPanel from '../components/ChatPanel';

export default function ChatPage() {
  const [lat, setLat] = useState<number | undefined>(undefined);
  const [lon, setLon] = useState<number | undefined>(undefined);

  useEffect(() => {
    if (typeof window !== 'undefined' && navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((p) => {
        setLat(p.coords.latitude);
        setLon(p.coords.longitude);
      });
    }
  }, []);

  return (
    <div className="max-w-3xl mx-auto p-4 flex flex-col gap-4">
      <h1 className="text-2xl font-bold">Чат</h1>
      <ChatPanel userLat={lat} userLon={lon} />
    </div>
  );
}


