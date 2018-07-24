import { combineReducers } from 'redux';
import homeReducer from '../containers/HomePage/modules/home-page-reducer';

export default combineReducers({
    home: homeReducer,
});
