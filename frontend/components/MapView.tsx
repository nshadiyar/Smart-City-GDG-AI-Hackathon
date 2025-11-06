import React, { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';

const MapContainer = dynamic(() => import('react-leaflet').then(m => m.MapContainer), { ssr: false });
const TileLayer = dynamic(() => import('react-leaflet').then(m => m.TileLayer), { ssr: false });
const Marker = dynamic(() => import('react-leaflet').then(m => m.Marker), { ssr: false });
const Popup = dynamic(() => import('react-leaflet').then(m => m.Popup), { ssr: false });

type Props = {
  lat?: number;
  lon?: number;
};

export default function MapView({ lat, lon }: Props) {
  const [pos, setPos] = useState<{ lat: number; lon: number } | null>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    // Fix Leaflet icon issue
    if (typeof window !== 'undefined') {
      import('leaflet').then((L) => {
        delete (L.default.Icon.Default.prototype as any)._getIconUrl;
        L.default.Icon.Default.mergeOptions({
          iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
          iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
          shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
        });
      });
    }
    if (lat && lon) {
      setPos({ lat, lon });
      return;
    }
    if (typeof window !== 'undefined' && navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((p) => {
        setPos({ lat: p.coords.latitude, lon: p.coords.longitude });
      }, () => {
        setPos({ lat: 51.128, lon: 71.453 });
      });
    } else {
      setPos({ lat: 51.128, lon: 71.453 });
    }
  }, [lat, lon]);

  if (!mounted || !pos) {
    return <div className="leaflet-container bg-gray-100 flex items-center justify-center">Загрузка карты...</div>;
  }

  return (
    <MapContainer center={[pos.lat, pos.lon]} zoom={14} scrollWheelZoom={false} className="leaflet-container" style={{ height: '300px', width: '100%' }}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Marker position={[pos.lat, pos.lon]}>
        <Popup>Вы здесь</Popup>
      </Marker>
    </MapContainer>
  );
}


