import {homeSagas} from '../routes/home/modules/sagas';
export default function* RootSaga() {
    yield [
        homeSagas()
    ];
}
