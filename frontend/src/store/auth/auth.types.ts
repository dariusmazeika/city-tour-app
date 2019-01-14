import { PayloadWithPromises } from '../../utils/types';

export interface LoginActionPayload extends PayloadWithPromises  {
  email: string;
  password: string;
}

export type UserAuth = {
  token: string,
};
