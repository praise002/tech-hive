export interface RegisterUserData {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
}

export interface RegisterResponse {
  status: string;
  message: string;
  data: {
    email: string;
  };
}

export interface LoginUserData {
  email: string;
  password: string;
}

export interface UpdateUserData {
  first_name: string;
  last_name: string;
}

export interface ChangePasswordData {
  old_password: string;
  new_password: string;
  confirm_password: string;
}

export interface VerifyOtpData {
  email: string;
  otp: string;
}

export interface PasswordResetCompleteData {
  email: string;
  new_password: string;
  confirm_password: string;
}

export enum ApiMethod {
  GET = 'GET',
  PUT = 'PUT',
  POST = 'POST',
  PATCH = 'PATCH',
  DELETE = 'DELETE',
}

export interface UpdateArticleData {
  title: string;
  content: string;
}

export interface SaveArticleData {
  articleId: string;
}

export interface CreateArticleData {
  title: string;
  content: string;
}

export interface UsernamesResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: {
    username: string;
    first_name: string;
    last_name: string;
    avatar: string;
  }[];
}
