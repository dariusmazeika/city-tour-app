import { changeLanguage } from './localization.actions';
import { ChangeLanguagePayload } from './localization.types';

describe('Localization actions', () => {

  describe('Change language action', () => {

    const actionPayload: ChangeLanguagePayload = {
      lang: 'be',
    };

    it('should create an action to change language', () => {
      const dispatch = jest.fn();
      const expected = { payload: actionPayload, type: 'CHANGE_LANGUAGE' };
      expect(typeof (changeLanguage(actionPayload))).toEqual('object');
      dispatch(changeLanguage(actionPayload));
      expect(dispatch).toBeCalledWith(expected);
    });

  });

});
