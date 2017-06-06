import {connect} from 'react-redux'
import {testRequest} from '../../../actions/actions'
import HomeView from '../components/home_view'

const mapDispatchToProps = {
    testRq: testRequest
};

const mapStateToProps = (state) => ({
    success: state.home.testSuccess
});

import {withRouter} from 'react-router-dom'
export default withRouter(connect(mapStateToProps, mapDispatchToProps)(HomeView))
