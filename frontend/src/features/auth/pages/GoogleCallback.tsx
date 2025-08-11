// import { useLocation } from 'react-router-dom';
// import { fetchTokens } from '../services/apiAuth';
// import { useGoogleCallback } from '../hooks/useAuth';

// TODO: FIX LATER
function GoogleCallback() {
  // const location = useLocation();

  // const params = new URLSearchParams(location.search);
  // const state = params.get('state');
  // const fullUrl = window.location.href; // full url for backend
  // if (!state) return;

  // const wrappedFetchTokens = async () => fetchTokens(state, fullUrl);

  // const {isLoading} = useGoogleCallback(wrappedFetchTokens);
  
  // if (isLoading) {
  //   return <div>Loading... Please wait.</div>;
  // }

  return <div>Processing authentication</div>;
}

export default GoogleCallback;
