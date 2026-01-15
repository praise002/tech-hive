// ============================================================================
// ENUMS
// ============================================================================

export enum EventType {
  PAGE_VIEW = 'page_view',
  PAGE_LOAD = 'page_load',
  SHARE = 'share',
}

export enum DeviceType {
  DESKTOP = 'Desktop',
  MOBILE = 'Mobile',
  TABLET = 'Tablet',
}

// ============================================================================
// TRACK ACTIVITY
// ============================================================================

export interface TrackActivityRequest {
  event_type: EventType;
  session_id: string;
  page_url: string;
  referrer?: string;
  device_type?: DeviceType;
  browser?: string;
  browser_version?: string;
  os?: string;
  os_version?: string;
  screen_resolution?: string;
  duration_seconds?: number;
  load_time_ms?: number;
  metadata?: {
    content_type?: string;
    content_id?: string;
    share_platform?: string;
    [key: string]: any;
  };
}

export interface TrackActivityResponse {
  activity_id: string;
}

// ============================================================================
// DASHBOARD METRICS
// ============================================================================

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

export interface MetricWithTrend {
  current: number;
  previous: number;
  trend: number;
  trend_direction: 'up' | 'down';
}

export interface DashboardMetrics {
  avg_time_on_page: MetricWithTrend;
  bounce_rate: MetricWithTrend;
  avg_load_speed: MetricWithTrend;
}

export interface TopPerformingPost {
  id: string;
  title: string;
  views: number;
  shares: number;
  avg_time: number;
}

export interface TopPerformingPosts {
  tutorials: TopPerformingPost[];
  news: TopPerformingPost[];
  events: TopPerformingPost[];
}

export interface DashboardMetricsResponse {
  period: 'weekly' | 'monthly';
  date_range: {
    current_start: string;
    current_end: string;
    previous_start: string;
    previous_end: string;
  };
  metrics: DashboardMetrics;
  device_types: DeviceDistribution[];
  active_users: ActiveUserTimeline[];
  top_performing_posts: TopPerformingPosts;
  cached: boolean;
}

// ============================================================================
// ARTICLE PERFORMANCE
// ============================================================================

export interface ArticlePerformanceResponse {
  article_id: string;
  title: string;
  total_views: number;
  unique_visitors: number;
  total_shares: number;
  avg_time_on_page: number; // in minutes
  bounce_rate: number; // percentage
  period: 'weekly' | 'monthly';
  date_range: {
    start: string;
    end: string;
  };
  cached: boolean;
}
