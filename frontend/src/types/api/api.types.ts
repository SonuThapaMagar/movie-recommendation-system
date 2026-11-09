export interface IApiErrorResponse {
  success: boolean;
  message: string;
  code: string;
  statusCode: number;
}

export interface IAxiosRes<T> {
  data: {
    message: string;
    success: boolean;
    data: T;
  };
}

export interface IApiResponse<T> {
  statusCode: number;
  message: string;
  data: T;
  error?: string;
  errorCode?: string;
  timestamp?: string;
  path?: string;
}
