import React from 'react';

function Error({ statusCode }: { statusCode?: number }) {
  return (
    <div>
      <h1>{statusCode ? `Error ${statusCode}` : 'An error occurred'}</h1>
      <p>{statusCode ? 'A server-side error occurred' : 'A client-side error occurred'}</p>
    </div>
  );
}

Error.getInitialProps = ({ res, err }: any) => {
  const statusCode = res ? res.statusCode : err ? err.statusCode : 404;
  return { statusCode };
};

export default Error;

