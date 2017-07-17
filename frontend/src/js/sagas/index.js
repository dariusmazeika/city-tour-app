import {homeSagas} from '../routes/home/modules/home-page-sagas';
export default function* RootSaga() {
    yield [
        homeSagas()
    ];
}
