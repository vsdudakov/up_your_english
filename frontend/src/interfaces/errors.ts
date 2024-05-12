export interface IFieldError {
  loc: string[];
  msg: string;
  type: string;
}

export interface IQueryError {
  detail?: IFieldError[] | string;
  description?: string;
}

export interface IError {
  response?: {
    status?: number;
    data?: IQueryError;
  };
}
