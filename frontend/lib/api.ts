import axios from 'axios';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000/api';

export type RecommendRequest = {
  lat: number;
  lon: number;
  max_time_min: number;
  preferences: string[];
  context: Record<string, any>;
  response_count: number;
};

export type Recommendation = {
  name: string;
  distance_m: number;
  why: string;
  visit_min: number;
  actions: string;
  confidence: 'high' | 'medium' | 'low';
  source: 'POI' | 'LLM' | 'RULE';
};

export async function getPOIs() {
  const res = await axios.get(`${API_BASE}/poi`);
  return res.data;
}

export async function recommend(req: RecommendRequest) {
  const res = await axios.post(`${API_BASE}/recommend`, req);
  return res.data as { items: Recommendation[] };
}

export function mapsRouteLink(lat: number, lon: number, name?: string) {
  const label = name ? encodeURIComponent(name) : '';
  return `https://www.google.com/maps/dir/?api=1&destination=${lat},${lon}&destination_place_id=${label}`;
}


