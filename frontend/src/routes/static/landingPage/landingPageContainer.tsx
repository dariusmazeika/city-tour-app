import * as React from 'react';
import { Link } from 'react-router-dom';

const landingPageContainer: React.FunctionComponent = () => {
  return (
    <div>
      <h2>Hello, welcome to CCT seed</h2>
      <ol>
        <Link to="/login">Login</Link>
      </ol>
    </div>
  );
};

export default landingPageContainer;
