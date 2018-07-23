import { homeSagas } from '../containers/HomePage/modules/home-page-sagas';
export default function* RootSaga() {
    yield [
        homeSagas()
    ];
}
