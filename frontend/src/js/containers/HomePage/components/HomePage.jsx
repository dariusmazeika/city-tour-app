import React, { Component } from 'react';
import PropTypes from 'prop-types';

export class HomeView extends Component {
    static propTypes = {
        testRq: PropTypes.func,
        success: PropTypes.bool
    };

    test() {
        this.props.testRq();
    }

    render() {
        return (
            <div>
                VALUE - {this.props.success ? 'Fetched' : 'Not fetched'}
                <div>
                    <button onClick={this.test.bind(this)}>test</button>
                </div>
            </div>
        );
    }
}

export default HomeView;
