import {connect} from 'react-redux';
import {testRequest} from '../../../actions/actions';
import HomeView from '../components/home-view';
import {withRouter} from 'react-router-dom';

const mapDispatchToProps = {
    testRq: testRequest
};

const mapStateToProps = (state) => ({
    success: state.home.testSuccess
});

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(HomeView));
