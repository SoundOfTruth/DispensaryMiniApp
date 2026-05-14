export interface JWTResponse {
  access_token: string;
  token_type: string;
}

export interface LoginSchema {
  email: string;
  password: string;
}
