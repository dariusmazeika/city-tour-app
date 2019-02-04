import typescriptFsa from 'typescript-fsa';
import { NavigationActionPayload } from './navigation.types';

const actionCreator = typescriptFsa();

export const locationChange = actionCreator<NavigationActionPayload>('LOCATION_CHANGE');
