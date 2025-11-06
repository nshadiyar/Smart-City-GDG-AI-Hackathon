import React, { useState } from 'react';
import { recommend, Recommendation } from '../lib/api';

type Props = {
  defaultText?: string;
  userLat?: number;
  userLon?: number;
};

export default function ChatPanel({ defaultText = '', userLat, userLon }: Props) {
  const [input, setInput] = useState(defaultText);
  const [items, setItems] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(false);

  const onSend = async () => {
    setLoading(true);
    try {
      // Simple parse: not full NLP, just a demo
      const lat = userLat ?? 51.128;
      const lon = userLon ?? 71.453;
      const max_time_min = 60;
      const preferences = input.length ? input.split(',').map((s) => s.trim()) : [];
      const res = await recommend({ lat, lon, max_time_min, preferences, context: {}, response_count: 3 });
      setItems(res.items);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-3">
      <div className="flex gap-2">
        <input
          className="flex-1 border rounded-md px-3 py-2"
          placeholder="Я возле Mega Silk Way, что советуешь на 1 час?"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button
          onClick={onSend}
          className="rounded-md bg-blue-600 text-white px-4 py-2 hover:bg-blue-700"
          disabled={loading}
        >
          {loading ? '...' : 'Отправить'}
        </button>
      </div>
      <div className="grid gap-3">
        {items.map((it, i) => (
          <div key={i} className="border rounded-md p-3">
            <div className="font-semibold">{it.name}</div>
            <div className="text-sm text-gray-700">{it.why}</div>
            <div className="text-xs text-gray-500">~{it.visit_min} мин · {it.distance_m} м</div>
          </div>
        ))}
      </div>
    </div>
  );
}


