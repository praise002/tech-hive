import { PaginatedResponse } from './types';

export interface Category {
  id: string;
  name: string;
  desc: string;
  slug: string;
}

export type CategoriesResponse = PaginatedResponse<Category>;

// ============================================================================
// JOBS
// ============================================================================

export enum JobType {
  FULL_TIME = 'full_time',
  PART_TIME = 'part_time',
  CONTRACT = 'contract',
  INTERNSHIP = 'internship',
  FREELANCE = 'freelance',
}

export enum WorkMode {
  REMOTE = 'remote',
  ONSITE = 'onsite',
  HYBRID = 'hybrid',
}

export interface Job {
  id: string;
  title: string;
  company: string;
  desc: string;
  requirements: string;
  responsibilities: string;
  url: string;
  salary: string | null;
  location: string;
  job_type: JobType;
  work_mode: WorkMode;
  category: string;
}

export type JobsResponse = PaginatedResponse<Job>;

// ============================================================================
// EVENTS
// ============================================================================

export interface Event {
  id: string;
  title: string;
  desc: string;
  start_date: string;
  end_date: string;
  location: string;
  agenda: string;
  ticket_url: string;
  category: string;
}

export type EventsResponse = PaginatedResponse<Event>;

// ============================================================================
// RESOURCES
// ============================================================================

export interface Resource {
  id: string;
  name: string;
  image_url: string;
  body: string;
  url: string;
  category: string;
  is_featured: boolean;
}

export type ResourcesResponse = PaginatedResponse<Resource>;

// ============================================================================
// TOOLS
// ============================================================================

export interface ToolTag {
  id: string;
  name: string;
}

export interface Tool {
  id: string;
  name: string;
  desc: string;
  url: string;
  image_url: string;
  call_to_action: string;
  tags: ToolTag[];
  category: string;
  is_featured: boolean;
}

export type ToolsResponse = PaginatedResponse<Tool>;

// ============================================================================
// MISCELLANEOUS
// ============================================================================

export interface ContributorGuidelinesRequest {
  terms_accepted: boolean;
}

