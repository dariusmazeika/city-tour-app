import { combineReducers } from 'redux';
import homeReducer from '../routes/home/modules/home-page-reducer';

export default combineReducers({
    home: homeReducer,
});
