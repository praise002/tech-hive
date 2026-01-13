export interface CreateCommentData {
  article_id: string;
  body: string;
  thread_id?: string; // Optional - if provided, creates a reply
}
