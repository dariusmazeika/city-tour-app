import typescriptFsa from 'typescript-fsa';
import { ChangeLanguagePayload } from './localization.types';

const actionCreator = typescriptFsa();

export const changeLanguage = actionCreator<ChangeLanguagePayload>('CHANGE_LANGUAGE');
