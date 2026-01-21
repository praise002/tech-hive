export interface DeviceDistribution {
  name: string;
  value: number;
  percentage: number;
}

export interface ActiveUserTimeline {
  date: string;
  day: string;
  registered_users: number;
  visitors: number;
  total_active_users: number;
}

export interface Metric {
  value: number;
  change: number;
  trend: 'up' | 'down' | 'neutral';
}

export interface TopPost {
  id: string;
  title: string;
  views: number;
  avg_time: number; // in seconds
}

export interface DashboardMetricsResponse {
  period: string;
  date_range: {
    start: string;
    end: string;
  };
  metrics: {
    total_users: Metric;
    active_users: Metric;
    total_sessions: Metric;
    avg_session_duration: Metric;
    bounce_rate: Metric;
    page_load_time: Metric;
  };
  device_types: DeviceDistribution[];
  active_users: ActiveUserTimeline[];
  top_performing_posts: {
    [category: string]: TopPost[];
  };
  cached: boolean;
}
