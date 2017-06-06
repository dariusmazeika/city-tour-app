/**
 * Created by tomasgobionis on 6/5/17.
 */
import {homeSagas} from '../routes/home/modules/sagas';

export default function* RootSaga() {
    yield [
        homeSagas()
    ]
}
