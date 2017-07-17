import { combineReducers } from 'redux';
import homeReducer from '../routes/home/modules/reducer';

export default combineReducers({
    home: homeReducer,
});
