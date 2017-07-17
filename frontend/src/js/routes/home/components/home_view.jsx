import React from 'react';

export class home_view extends React.Component {

    constructor(props) {
        super(props);

    }

    test = () => {
        this.props.testRq();
    };

    render() {
        console.log(this.props)
        return (
            <div >
                VALUE - {this.props.success ? 'dfsdfsd' : '12312'}
                <div>
                    <button onClick={this.test}>test</button>
                </div>
            </div>
        )
    }
}

export default home_view
