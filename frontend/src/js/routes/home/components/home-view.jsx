import React from 'react';

export class HomeView extends React.Component {

    test() {
        this.props.testRq();
    }

    render() {
        return (
            <div >
                VALUE - {this.props.success ? 'Fetched' : 'Not fetched'}
                <div>
                    <button onClick={this.test.bind(this)}>test</button>
                </div>
            </div>
        );
    }
}

export default HomeView;
