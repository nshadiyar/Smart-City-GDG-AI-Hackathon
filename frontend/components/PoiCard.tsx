import React from 'react';
import { Recommendation } from '../lib/api';

type Props = {
  item: Recommendation;
};

export default function PoiCard({ item }: Props) {
  const openRoute = () => {
    const url = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(item.name + ' Astana')}`;
    window.open(url, '_blank');
  };
  return (
    <div className="border rounded-lg p-4 flex flex-col gap-2 shadow-sm">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">{item.name}</h3>
        <span className="text-sm text-gray-500">{item.distance_m} м</span>
      </div>
      <p className="text-sm text-gray-700">{item.why}</p>
      <div className="flex justify-between text-sm text-gray-600">
        <span>~{item.visit_min} мин</span>
        <span>confidence: {item.confidence}</span>
        <span>source: {item.source}</span>
      </div>
      {item.actions && (
        <p className="text-sm text-gray-700">Совет: {item.actions}</p>
      )}
      <button
        onClick={openRoute}
        className="mt-1 inline-flex items-center justify-center rounded-md bg-blue-600 text-white px-3 py-2 text-sm hover:bg-blue-700"
      >
        Показать маршрут
      </button>
    </div>
  );
}


