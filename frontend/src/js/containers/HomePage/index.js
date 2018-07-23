import { connect } from 'react-redux';
import HomeView from './components/HomePage';
import { testRequest } from '../../actions/actions';

const mapDispatchToProps = {
    testRq: testRequest
};

const mapStateToProps = (state) => ({
    success: state.home.testSuccess
});

export default connect(mapStateToProps, mapDispatchToProps)(HomeView);
