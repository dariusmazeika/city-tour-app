import { RootState } from '../reducers';
import { UserAuth } from './auth.types';

export const getUser = (state: RootState): UserAuth | null => state.auth.user;
export const getUserIsLogged = (state: RootState): boolean => state.auth.user != null;
