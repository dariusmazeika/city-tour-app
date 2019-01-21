import { PayloadWithPromises } from '../../utils/types';

export interface LoginActionPayload extends PayloadWithPromises  {
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
