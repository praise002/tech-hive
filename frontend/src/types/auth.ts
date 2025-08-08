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
