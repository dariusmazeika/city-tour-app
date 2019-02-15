import { RootState } from '../reducers';

export const getCurrentLanguage = (state: RootState): string => state.localization.currentLanguage;
