import { LoadableItem, PayloadWithPromises } from '../../utils/types';

export interface LoginActionPayload extends PayloadWithPromises {
  email: string;
  password: string;
}

export interface LoginActionSuccess {
  params: LoginActionPayload;
  result: UserAuth;
}

export type UserAuth = {
  token: string,
};

export interface UserData extends LoadableItem {
  item: {
    email: string;
    first_name: string;
    last_name: string;
  } | null;
}
