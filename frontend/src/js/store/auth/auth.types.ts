import { LoadableItem, PayloadWithPromises } from '@Utils/types';

export interface LoginFormData {
  email: string;
  password: string;
}
export interface LoginActionPayload extends LoginFormData, PayloadWithPromises {}


export interface LoginActionSuccess {
  params: LoginActionPayload;
  result: UserAuth;
}

export type UserAuth = {
  token: string;
};

export interface UserData extends LoadableItem {
  item: {
    email: string;
    first_name: string;
    last_name: string;
  } | null;
}
